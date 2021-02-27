import asyncio
from collections import defaultdict, deque
from datetime import timedelta
import random
import string
from typing import Optional, List
import cv2

import discord
from discord.ext.commands import Bot

import d3dshot
import easyocr

from ingameleader import config as cfg
from ingameleader.game import Game
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
        # If there is a winner we are between rounds
        for winner, pixel_signature in cfg.ROUND_WINNER_PIXEL_SIGNATURES.items():
            if match_signature(frame, pixel_signature):
                return Context.BETWEEN_ROUNDS

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
        if current_context in [Context.DEAD, Context.BETWEEN_ROUNDS, Context.UNKNOWN]:
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
        if current_context in [Context.DEAD, Context.BETWEEN_ROUNDS, Context.UNKNOWN, Context.WARM_UP]:
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
        if current_context in [Context.DEAD, Context.BETWEEN_ROUNDS, Context.UNKNOWN, Context.WARM_UP]:
            return None

        round_time = self.get_round_time(frame, text_results, current_context)
        location = self.get_location(frame, text_results, current_context)
        if round_time is None or location is None:
            return None

        if round_time < timedelta(seconds=110):
            return None

        return Side.from_location(location)

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


client = discord.Client()
bot = Bot(client)
game = Game()
GAME_LOCK = asyncio.Lock()


async def edit_or_create_messages(new_text, messages=None):
    print(f"{'EDITING' if messages is not None else 'CREATING'} MESSAGES: '{new_text}'")

    if messages is None:
        messages = []
        for guild in bot.guilds:
            if guild.name == 'Foreskins + the help':
                continue
            for channel in guild.text_channels:
                message_handle = await channel.send(new_text)
                messages.append(message_handle)
    else:
        for message in messages:
            await message.edit(content=new_text)

    return messages


async def monitor_game():
    await bot.wait_until_ready()
    screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
    parser = FrameParser()
    while True:
        frame = screenshotter.screenshot(region=cfg.META_REGION)
        observation = parser.frame_to_observation(frame)
        print(observation)
        async with GAME_LOCK:
            game.update(observation)
        await asyncio.sleep(1)


def observations_to_route(observations: List[Observation]) -> List[str]:
    route = []
    for observation in observations:
        if not route:
            route.append(observation.location)
        else:
            if route[-1] != observation.location:
                route.append(observation.location)
    return route


def route_to_strategy(route):
    return random.choice(STRATEGIES)


GOOD_MESSAGE_TEMPLATE = """```diff
+ [{}]
```"""
BAD_MESSAGE_TEMPLATE = """```diff
- [{}]
```"""
NEUTRAL_MESSAGE_TEMPLATE = """```fix
  [{}]
```"""
COMMAND_MESSAGE_TEMPLATE = """```ini
  [{}]
```"""
MESSAGE_TEMPLATE = """
```json
  {{"Counter Terrorist": {}, "Terrorist": {}}}
```"""
STRATEGIES = [
    "Rush B!".ljust(26) + "W/R 53%",
    "Rush A!".ljust(26) + "W/R 56%",
    "Take it slow..".ljust(26) + "W/R 51%",
    "Split A".ljust(26) + "W/R 45%",
]


async def log_game_progress():
    logging_history = defaultdict(
        lambda: {"logged_start": False, "logged_end": False, "logged_recommendation": False}
    )
    message_handles = None
    message_history = deque([], 3)
    last_message = None
    while True:
        await asyncio.sleep(5)

        async with GAME_LOCK:
            for round_number, round in game.rounds.items():
                progress = logging_history[round_number]

                if not progress["logged_start"]:
                    message_history.appendleft(
                        NEUTRAL_MESSAGE_TEMPLATE.format(f"Starting round {round_number}".ljust(33))
                    )
                    progress["logged_start"] = True

                if not progress["logged_recommendation"]:
                    message_history.appendleft(
                        COMMAND_MESSAGE_TEMPLATE.format(random.choice(STRATEGIES))
                    )
                    progress["logged_recommendation"] = True

                if round.complete and not progress["logged_end"]:
                    if round.ct_win and round.side == Side.CT:
                        message_history.appendleft(
                            GOOD_MESSAGE_TEMPLATE.format(f"We won! Strategy: {' -> '.join(observations_to_route(round.observations))}".ljust(33))
                        )
                    elif round.ct_win and round.side != Side.CT:
                        message_history.appendleft(
                            BAD_MESSAGE_TEMPLATE.format(f"We lost! Strategy: {' -> '.join(observations_to_route(round.observations))}".ljust(33))
                        )
                    elif round.t_win and round.side == Side.T:
                        message_history.appendleft(
                            GOOD_MESSAGE_TEMPLATE.format(
                                f"We won! Strategy: {' -> '.join(observations_to_route(round.observations))}".ljust(33))
                        )
                    elif round.t_win and round.side != Side.T:
                        message_history.appendleft(
                            BAD_MESSAGE_TEMPLATE.format(
                                f"We lost! Strategy: {' -> '.join(observations_to_route(round.observations))}".ljust(33))
                        )
                    progress["logged_end"] = True

                logging_history[round_number] = progress

            a = list(message_history)
            a.reverse()
            full_message = MESSAGE_TEMPLATE.format(game.ct_score, game.t_score) + "".join(a)
            if full_message != last_message:
                message_handles = await edit_or_create_messages(full_message, message_handles)
                last_message = full_message


bot.loop.create_task(monitor_game())
bot.loop.create_task(log_game_progress())


if __name__ == "__main__":
    # screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
    # reader = easyocr.Reader(["en"])
    #
    # while True:
    #     obs = make_observation(screenshotter, reader)
    #     print(obs)
    bot.run(cfg.DISCORD_TOKEN)
