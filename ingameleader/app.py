import asyncio
from collections import deque
from datetime import timedelta, datetime
import os
import logging
import logging.config
import string
from typing import Optional, List, Tuple

import cv2
from PIL import Image
import discord
from discord.ext.commands import Bot
import dtw
import d3dshot
import easyocr
import numpy as np
from scipy.stats import beta
from scipy.spatial.distance import cdist

from ingameleader import config as cfg
from ingameleader.game import Game
from ingameleader.plot import plot_strategies
from ingameleader.utils import (
    relative_to,
    best_result,
    format_location,
    match_signature,
    text_to_score,
    mask_unused_regions,
    extract,
    LETTER_TO_DIGIT,
)
from ingameleader.model.observation import Observation
from ingameleader.model.side import Side
from ingameleader.model.context import Context
from ingameleader.model.round import Round
from ingameleader.model.dao import Map, Strategy, Location, create_session

logging.config.dictConfig(cfg.LOGGING_CONFIG)
logger = logging.getLogger(__name__)
client = discord.Client()
bot = Bot(client)
game = Game()
GAME_LOCK = asyncio.Lock()


class FrameParser:
    def __init__(self):
        self.reader = easyocr.Reader(["en"])

    def frame_to_observation(self, frame):
        frame = mask_unused_regions(frame)

        text_results = self.reader.readtext(
            frame,
            decoder="beamsearch",
            allowlist=string.ascii_letters + string.digits + ":" + " " + " $",
            batch_size=32,
        )
        current_context = self.get_current_context(frame, text_results)
        return Observation(
            current_context,
            self.get_location(frame, text_results, current_context),
            self.get_ct_score(frame, text_results, current_context),
            self.get_t_score(frame, text_results, current_context),
            self.get_round_time(frame, text_results, current_context),
            self.get_side(frame, text_results, current_context),
            self.get_money(frame, text_results, current_context),
            self.get_round_winner(frame, text_results, current_context),
        )

    def get_current_context(self, frame, text_results) -> Context:
        for winner, pixel_signature in cfg.ROUND_WINNER_PIXEL_SIGNATURES.items():
            if match_signature(frame, pixel_signature):
                return Context.ROUND_WINNER_SCREEN

        # If we have the playing on team text we are in the buy phase
        playing_on_team_text = best_result(
            text_results,
            relative_to(cfg.PLAYING_ON_TEAM_TEXT, cfg.META_REGION),
            0.2
        )
        if playing_on_team_text is not None:
            # TERRORIST is found for both Side.CT and Side.T
            for terrorist_text in ["terrorist", "terrdrist"]:
                if terrorist_text in playing_on_team_text.lower():
                    return Context.BUY_PHASE

        money_text = best_result(
            text_results,
            relative_to(cfg.MONEY_REGION, cfg.META_REGION),
            0.2,
        )
        # Some times (e.g. when you get a kill the money increments and the animation makes
        # the $ look like an S
        if money_text is not None and money_text.startswith("S"):
            money_text = money_text.replace("S", "$")
        if money_text is None or "$" not in money_text:
            return Context.UNKNOWN

        round_text = best_result(
            text_results,
            relative_to(cfg.ROUND_TEXT_REGION, cfg.META_REGION),
            0.5
        )
        if round_text is not None and "round" in round_text.lower():
            return Context.DEAD

        # TODO detect between rounds
        return Context.ALIVE

    def get_round_winner(self, frame, text_results, current_context) -> Optional[Side]:
        for winner, pixel_signature in cfg.ROUND_WINNER_PIXEL_SIGNATURES.items():
            if match_signature(frame, pixel_signature, cfg.META_REGION):
                return Side.from_initial(winner)

    def get_location(self, frame, text_results, current_context) -> Optional[str]:
        if current_context in [Context.DEAD, Context.ROUND_WINNER_SCREEN, Context.UNKNOWN]:
            return None

        score_frame = extract(cfg.LOCATION_TEXT_REGION, frame, cfg.META_REGION)
        score_frame = cv2.normalize(cv2.cvtColor(score_frame, cv2.COLOR_RGB2GRAY), None, 0, 255, cv2.NORM_MINMAX)

        text_results = self.reader.readtext(
            score_frame,
            allowlist=string.ascii_letters,
        )
        location_text = max(text_results, key=lambda r: r[2], default=(None, None))[1]

        return None if location_text is None else format_location(location_text)

    def _get_score(self, frame, text_results, current_context, region, pixel_signatures) -> Optional[int]:
        if current_context in [Context.DEAD, Context.UNKNOWN]:
            return None

        for score, pixel_signature in pixel_signatures.items():
            if match_signature(frame, pixel_signature, cfg.META_REGION):
                return score

        score_frame = extract(region, frame, cfg.META_REGION)
        score_frame = cv2.normalize(cv2.cvtColor(score_frame, cv2.COLOR_RGB2GRAY), None, 0, 255, cv2.NORM_MINMAX)

        text_results = self.reader.readtext(
            score_frame,
            allowlist=string.digits,
        )
        text_score = max(text_results, key=lambda r: r[2], default=(None, None))[1]

        if text_score is None:
            return None

        return text_to_score(text_score)

    def get_ct_score(self, frame, text_results, current_context) -> Optional[int]:
        return self._get_score(frame, text_results, current_context, cfg.CT_SCORE_REGION, cfg.CT_SCORE_PIXEL_SIGNATURES)

    def get_t_score(self, frame, text_results, current_context) -> Optional[int]:
        return self._get_score(frame, text_results, current_context, cfg.T_SCORE_REGION, cfg.T_SCORE_PIXEL_SIGNATURES)

    def get_round_time(self, frame, text_results, current_context) -> Optional[timedelta]:
        if current_context in [Context.DEAD, Context.ROUND_WINNER_SCREEN, Context.UNKNOWN, Context.WARM_UP]:
            return None

        # Try and get mins and seconds together
        round_time_text = best_result(
            text_results,
            relative_to(cfg.TIME_REGION, cfg.META_REGION),
            0.5
        )
        try:
            mins, secs = round_time_text.split(":")
        except Exception as e:
            # Try and get mins and seconds separately
            mins = best_result(
                text_results,
                relative_to(cfg.MINUTES_REGION, cfg.META_REGION),
                0.2
            )
            secs = best_result(
                text_results,
                relative_to(cfg.SECONDS_REGION, cfg.META_REGION),
                0.2
            )

        if mins is None or secs is None:
            return None

        try:
            time = timedelta(seconds=int(secs), minutes=int(mins))
        except ValueError:
            return None

        if time > timedelta(minutes=2):
            return None

        return time

    def get_side(self, frame, text_results, current_context) -> Optional[Side]:
        if current_context in [Context.DEAD, Context.ROUND_WINNER_SCREEN, Context.UNKNOWN, Context.WARM_UP]:
            return None

        # Try and get a side by parsing the "PLAYING ON TEAM <TEAM>" text
        if current_context == Context.BUY_PHASE:
            playing_on_team_text = best_result(
                text_results,
                relative_to(cfg.PLAYING_ON_TEAM_TEXT, cfg.META_REGION),
                0.2
            )
            if playing_on_team_text is not None:
                side = Side.from_playing_on_team(playing_on_team_text)
                if side is not None:
                    return side

        # Get the players location
        location = self.get_location(frame, text_results, current_context)
        if location is None:
            return None

        # If we are in the buy phase and we have found a location
        # use the location to infer the side
        if current_context == Context.BUY_PHASE:
            side = Side.from_location(location)
            if side is not None:
                return side

        # If we are very early in the round, use the location to
        # infer the side
        round_time = self.get_round_time(frame, text_results, current_context)
        if round_time is None:
            return None

        if round_time > timedelta(seconds=110):
            return Side.from_location(location)

        return None

    def get_money(self, frame, text_results, current_context) -> Optional[float]:
        if current_context == current_context.UNKNOWN:
            return None

        money_text = best_result(
            text_results,
            relative_to(cfg.MONEY_REGION, cfg.META_REGION),
            0.3,
        )
        # Some times (e.g. when you get a kill the money increments and the animation makes
        # the $ look like an S
        if money_text is not None and money_text.startswith("S"):
            money_text = money_text.replace("S", "$")
        if money_text is None or "$" not in money_text:
            return None
        # Remove $ sign
        money_text = money_text.replace("$", "")
        # Replace letters that commonly get mixed up with digits
        for l, d in LETTER_TO_DIGIT.items():
            money_text = money_text.replace(l, str(d))
        try:
            return int(money_text)
        except:
            return None


async def edit_or_create_messages(title, footer, image_url, message_handles=None):
    logger.debug("Updating message")
    embed = discord.Embed(
        title=title,
        # colour=discord.Color.blue()
        colour=0x3498db,
    )
    embed.set_footer(text=footer)
    if image_url is not None:
        embed.set_image(url=image_url)
    if message_handles is None:
        message_handles = []
        for guild in bot.guilds:
            if guild.name == 'Foreskins + the help':
                logger.warning(f"Skipping %s", guild.name)
                continue
            for channel in guild.text_channels:
                message_handle = await channel.send(embed=embed)
                message_handles.append(message_handle)
    else:
        for message in message_handles:
            await message.edit(embed=embed)

    return message_handles


async def monitor_game():
    await bot.wait_until_ready()
    screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
    parser = FrameParser()
    while True:
        frame = screenshotter.screenshot(region=cfg.META_REGION)
        if cfg.LOGGING_LEVEL <= logging.DEBUG:
            Image.fromarray(frame).save(f"screenshots/log/{datetime.now().timestamp()}.png")
        observation = parser.frame_to_observation(frame)
        logger.debug(observation)
        async with GAME_LOCK:
            game.update(observation)
        await asyncio.sleep(1)


def location_to_point(location: str, session) -> Optional[Tuple[int, int]]:
    location = session.query(Location).filter(Location.name == location).first()
    if location is None:
        return None
    return location.x, location.y


def observations_to_points(observations: List[Observation], session) -> List[Tuple[int, int]]:
    points = []
    for observation in observations:
        point = location_to_point(observation.location, session)
        if point is not None:
            if not points or points[-1] != point:
                points.append(point)
    return points


TITLE_TEMPLATE = """Counter-Terrorist [ {} ]      [ {} ] Terrorist        """
EXECUTE_TEMPLATE = """[ ROUND {} ] [ EXECUTE ] {}"""
STRATEGY_TEMPLATE = """[ ROUND {} ] [ STRATEGY ] {}"""
MUTINY_TEMPLATE = """[ ROUND {} ] [ MUTINY ] {}"""
RESULT_TEMPLATE = """[ ROUND {} ] [ RESULT ] {}"""


def select_strategy(strategies: List[Strategy]) -> Optional[Strategy]:
    logger.debug("Selecting strategy")
    return max(
        strategies,
        key=lambda strat: beta.rvs(
            strat.alpha + strat.wins,
            strat.beta + strat.losses,
            size=1,
        )
    )


def identify_strategy(
        strategies: List[Strategy],
        points: List[Tuple[int, int]],
        selected_strategy: Optional[Strategy] = None
) -> Optional[Strategy]:
    # Insert the selected strategy first, we want to stop fast if the strategy is selected
    # and if there are multiple strategies with compatible routes we also want to bias
    # towards the one we selected.
    strategies_with_selected_strategy_first = [selected_strategy] + strategies
    logger.debug("Expected strategy: %s", selected_strategy)
    for strategy in strategies_with_selected_strategy_first:
        for exemplar_route in strategy.exemplar_routes:
            exemplar_points = [(rtl.location.x, rtl.location.y) for rtl in exemplar_route.route_to_locations]
            index = min(len(exemplar_points), len(points))
            sub_points = np.array([(idx, x, y) for idx, (x, y) in enumerate(points[:index])])
            exemplar_points = np.array([(idx, x, y) for idx, (x, y) in enumerate(exemplar_points[:index])])
            alignment = dtw.dtw(cdist(sub_points, exemplar_points))
            logger.debug("%s DTW: %s", strategy.name, alignment.normalizedDistance)
            if alignment.normalizedDistance < 60:
                return strategy
    return None


def edit_distance(str1, str2):
    a, b = len(str1), len(str2)
    string_matrix = [[0 for i in range(b + 1)] for i in range(a + 1)]
    for i in range(a + 1):
        for j in range(b + 1):
            if i == 0:
                # If first string is empty, insert all characters of second string into first.
                string_matrix[i][j] = j
            elif j == 0:
                # If second string is empty, remove all characters of first string.
                string_matrix[i][j] = i
            elif str1[i-1] == str2[j-1]:
                # If last characters of two strings are same, nothing much to do. Ignore the last
                # two characters and get the count of remaining strings.
                string_matrix[i][j] = string_matrix[i-1][j-1]
            else:
                string_matrix[i][j] = 1 + min(
                    string_matrix[i][j-1],         # insert operation
                    string_matrix[i-1][j],         # remove operation
                    string_matrix[i-1][j-1]        # replace operation
                )
    return string_matrix[a][b]


def update_strategy(played_strategy: Optional[Strategy], round: Round, session):
    if played_strategy is None:
        logger.info("Unable to update strategy because a strategy was not identified")
        return None
    if round.won is None:
        logger.info("Unable to update strategy because who won was not identified")
        return None

    if round.won:
        played_strategy.wins += 1
    else:
        played_strategy.losses += 1
    session.commit()


class Message:
    def __init__(self):
        self.text_messages = deque(maxlen=5)
        self.game = None
        self.round = None
        self.selected_strategy = None
        self.url = None
        self.message_handles = None

    def set_game(self, game: Game):
        self.game = game

    def append_description(self, string: str):
        self.text_messages.append(string)

    def set_round(self, round: Round):
        self.round = round

    def set_selected_strategy(self, strategy: Strategy):
        self.selected_strategy = strategy
        self.append_description(
            EXECUTE_TEMPLATE.format(
                self.round.number,
                self.selected_strategy.name
            )
        )

    def set_url(self, url: str):
        self.url = url

    async def update(self):
        self.message_handles = await edit_or_create_messages(
            TITLE_TEMPLATE.format(self.game.ct_score, self.game.t_score) if game.rounds else "Waiting for game to start",
            "\n".join(self.text_messages),
            self.url,
            self.message_handles
        )


async def game_loop(message: Message, map: Map, session):
    async with GAME_LOCK:
        side = game.side
        rounds = game.rounds
        if game.complete:
            return None

    strategies = session \
        .query(Strategy) \
        .filter_by(map_id=map.id, side=side) \
        .all()

    if not rounds or not strategies:
        if not rounds:
            logger.info("No rounds found yet")
        if not strategies:
            logger.info("No strategies found yet")
        # Game has not started (or we have not figured out the side we are
        # on yet)
        await asyncio.sleep(1)
        return None

    round = rounds[max(rounds)]
    message.set_round(round)

    selected_strategy = select_strategy(strategies)
    message.set_selected_strategy(selected_strategy)

    url = plot_strategies(strategies, selected_strategy)
    message.set_url(url)

    await message.update()

    while not round.complete:
        await asyncio.sleep(1)

    points = observations_to_points(round.observations, session)
    logger.debug("Route points: %s", points)
    played_strategy = identify_strategy(strategies, points, selected_strategy)
    if played_strategy is None:
        logger.info("Unable to identify strategy for route: %s", points)
    else:
        if played_strategy != selected_strategy:
            message.append_description(
                MUTINY_TEMPLATE.format(
                    round.number,
                    f"You were meant to play {selected_strategy.name} but played {played_strategy.name}"
                )
            )
        logger.debug("Updating strategy: %s", played_strategy)

        update_strategy(played_strategy, round, session)
        if round.won is not None:
            message.append_description(
                RESULT_TEMPLATE.format(round.number, f"We {'won' if round.won else 'lost'}")
            )
            url = plot_strategies(strategies, selected_strategy)
            message.set_url(url)

    await message.update()


async def log_game_progress():
    await bot.wait_until_ready()

    map_name = "Dust 2"
    logger.debug("Creating a new message")
    message = Message()

    async with GAME_LOCK:
        message.set_game(game)
        await message.update()

    with create_session() as session:
        map = session.query(Map).filter_by(name=map_name).first()
        logger.info("Playing on %s", map.name)

        while True:
            try:
                await game_loop(message, map, session)
            except Exception as e:
                logger.exception("Unhandled exception in game loop")
                logger.warning(e)


bot.loop.create_task(monitor_game())
bot.loop.create_task(log_game_progress())


if __name__ == "__main__":
    # screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
    # reader = easyocr.Reader(["en"])
    #
    # while True:
    #     obs = make_observation(screenshotter, reader)

    bot.run(os.getenv("DISCORD_API_TOKEN"))
