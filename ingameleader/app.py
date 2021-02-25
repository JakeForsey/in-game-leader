import asyncio
from collections import defaultdict, deque
from datetime import timedelta
import string
from typing import Optional, List

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
    LETTER_TO_DIGIT,
)
from ingameleader.model.observation import Observation
from ingameleader.model.side import Side
from ingameleader.model.context import Context


def get_current_context(frame, text_results) -> Context:
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


def get_location(frame, text_results, current_context) -> Optional[str]:
    if current_context in [Context.DEAD, Context.BETWEEN_ROUNDS, Context.UNKNOWN]:
        return None

    location_text = best_result(
        text_results,
        relative_to(cfg.LOCATION_TEXT_REGION, cfg.META_REGION),
        0.15
    )
    return None if location_text is None else format_location(location_text)


def get_ct_score(frame, text_results, current_context) -> Optional[int]:
    if current_context in [Context.DEAD, Context.UNKNOWN]:
        return None

    if match_signature(frame, cfg.CT_SCORE_PIXEL_SIGNATURE, cfg.META_REGION):
        return 0

    text_score = best_result(
        text_results,
        relative_to(cfg.CT_SCORE_REGION, cfg.META_REGION),
        0.15,
    )
    if text_score is None:
        return None

    return text_to_score(text_score)


def get_t_score(frame, text_results, current_context) -> Optional[int]:
    if current_context in [Context.DEAD, Context.UNKNOWN]:
        return None

    if match_signature(frame, cfg.T_SCORE_PIXEL_SIGNATURE, cfg.META_REGION):
        return 0

    text_score = best_result(
        text_results,
        relative_to(cfg.T_SCORE_REGION, cfg.META_REGION),
        0.15,
    )
    if text_score is None:
        return None

    return text_to_score(text_score)


def get_round_time(frame, text_results, current_context) -> Optional[timedelta]:
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


def get_side(frame, text_results, current_context) -> Optional[Side]:
    if current_context in [Context.DEAD, Context.BETWEEN_ROUNDS, Context.UNKNOWN, Context.WARM_UP]:
        return None

    round_time = get_round_time(frame, text_results, current_context)
    location = get_location(frame, text_results, current_context)
    if round_time is None or location is None:
        return None

    if round_time < timedelta(seconds=110):
        return None

    return Side.from_location(location)


def get_money(frame, text_results, current_context) -> Optional[float]:
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


def frame_to_observation(frame, reader):
    frame = mask_unused_regions(frame)
    text = reader.readtext(
        frame,
        decoder="beamsearch",
        allowlist=string.ascii_letters + string.digits + ":" + " " + " $",
        batch_size=32,
    )
    current_context = get_current_context(frame, text)
    return Observation(
        get_location(frame, text, current_context),
        get_ct_score(frame, text, current_context),
        get_t_score(frame, text, current_context),
        get_round_time(frame, text, current_context),
        get_side(frame, text, current_context),
        get_money(frame, text, current_context),
        current_context,
    )


def make_observation(screenshotter, reader):
    frame = screenshotter.screenshot(region=cfg.META_REGION)
    return frame_to_observation(frame, reader)


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
    reader = easyocr.Reader(["en"])
    while True:
        observation = make_observation(screenshotter, reader)
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


LOG_TEMPLATE = """
=============================
    CT {}   |    T {}
{}
{}
{}
=============================
"""

async def log_game_progress():
    logging_history = defaultdict(
        lambda: {"logged_start": False, "logged_end": False}
    )
    message_handles = None
    message_history = deque(["", "", ""], 3)
    while True:
        await asyncio.sleep(5)

        async with GAME_LOCK:
            for round_number, round in game.rounds.items():
                progress = logging_history[round_number]

                if not progress["logged_start"]:
                    message_history.appendleft(f"Starting round {round_number}")
                    progress["logged_start"] = True

                if round.complete and not progress["logged_end"]:
                    message_history.appendleft(f"{'CT won' if round.ct_win else 'T won'} round {round_number} with route: {' -> '.join(observations_to_route(round.observations))}")
                    progress["logged_end"] = True

                logging_history[round_number] = progress

            message_handles = await edit_or_create_messages(LOG_TEMPLATE.format(game.ct_score, game.t_score, *message_history), message_handles)


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
