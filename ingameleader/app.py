import asyncio
from dataclasses import dataclass
from datetime import timedelta
import enum
import string
from typing import Optional, Dict

import discord
import d3dshot
import easyocr
import numpy as np

from ingameleader import config as cfg


LOCK = asyncio.Lock()


class InGameLeaderDiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print("Running in:")
        for guild in self.guilds:
            print(f" * {guild}")

    async def send_message(self, message):
        print(f"SENDING MESSAGE: {message}")
        for guild in self.guilds:
            # if guild.name == 'Foreskins + the help':
            #     continue
            for channel in guild.text_channels:
                await channel.send(message)

    async def my_background_task(self):
        await self.wait_until_ready()

        screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
        reader = easyocr.Reader(["en"])

        game = Game()
        while not self.is_closed():
            await asyncio.sleep(1)

            async with LOCK:
                print("Making observation")
                observation = make_observation(screenshotter, reader)

            print(observation)
            await game.update(observation, self)

            if game.complete:
                await self.send_message(game)
                game = Game()


bot = InGameLeaderDiscordClient()


class Side(enum.Enum):
    CT = 0
    T = 1

    @staticmethod
    def from_location(location):
        if location == format_location("CT Start"):
            return Side.CT
        elif location == format_location("T Start"):
            return Side.T
        else:
            print(f"Unable to determine side from {location}")
            return None


class Context(enum.Enum):
    ALIVE = 0
    DEAD = 1
    BETWEEN_ROUNDS = 2
    WARM_UP = 3
    UNKNOWN = 4


@dataclass
class Observation:
    location: Optional[str]
    ct_score: Optional[int]
    t_score: Optional[int]
    time: Optional[timedelta]
    side: Optional[Side]
    money: Optional[int]
    context: Context

    @property
    def round_number(self):
        return self.ct_score + self.t_score if self.ct_score is not None and self.t_score is not None else None


@dataclass
class Round:
    number: int
    locations: list
    side: Optional[Side] = None
    win: Optional[bool] = None

    def __str__(self):
        locations = []
        for location in self.locations:
            if locations[-1] != location:
                locations.append(location)
        return f"Round({self.number}, {locations}, {self.side}, {self.win})"


class Game:
    def __init__(self):
        self.rounds: Dict[int, Round] = {}
        self.ct_score: int = 0
        self.t_score: int = 0

    async def update(self, observation: Observation, client: InGameLeaderDiscordClient):
        if observation.context != Context.ALIVE:
            return None

        current_round = self.rounds.get(observation.round_number, None)

        if current_round is not None:
            # Check that this observation is for the latest round
            if current_round.number != max(self.rounds.keys()):
                print("WARNING: Got an observation for an old round...")
                return None

            current_round.locations.append(observation.location)
            current_round.side = observation.side

        else:
            if observation.round_number is None:
                print("WARNING: Unable to create new round as observation did not have a round number")
                return None

            last_round = self.rounds.get(observation.round_number - 1, None)

            if last_round is not None:
                await client.send_message(
                    f"""
                    Round completed:
                    {self.rounds.get(observation.round_number, None)}
                    """
                )

            # If the current round is None, create a new one
            new_round = Round(
                observation.round_number,
                side=observation.side,
                locations=[observation.location],
            )
            self.rounds[new_round.number] = new_round
            await client.send_message(f"Starting round {new_round.number} on {new_round.side.name})")

            # Update the scores
            if new_round.number != 0:
                print("Need to update last round...")
                pass

    @property
    def complete(self):
        return self.ct_score > 15 or self.t_score > 15 or self.t_score + self.ct_score > 30

    def __str__(self):
        for round in [self.rounds[i] for i in range(len(self.rounds))]:
            print(round)


LETTER_TO_DIGIT = {
    "G": 6,
    "D": 0,
    "g": 9
}

LOCATION_LOOKUP = {
    "gtstart": "ctstart",
    "dutside": "outside",
    "dutsidelong": "outsidelong",
    "dutsidetunnel": "outsidetunnel",
}


def match_signature(frame, signature, meta_region=cfg.META_REGION):
    for position, colour, expectation in signature:
        position = relative_to(position, meta_region)
        value = frame[position[1], position[0]]
        if (np.abs(value - np.array(colour)) < 10).all() != expectation:
            return False
    return True


def format_location(text):
    return text.replace(" ", "").lower()


def extract(region, frame, meta_region=cfg.META_REGION):
    return frame[
        region[1] - meta_region[1]: region[3] - meta_region[1],
        region[0] - meta_region[0]: region[2] - meta_region[0],
    ]


def relative_to(region, meta_region):
    if len(region) == 2:
        return (
            region[0] - meta_region[0],
            region[1] - meta_region[1],
        )
    elif len(region) == 4:
        return (
            region[0] - meta_region[0],
            region[1] - meta_region[1],
            region[2],
            region[3],
        )
    else:
        raise ValueError("Expected region to have either 2 or 4 values")


def within(region, other_region):
    return region[0] >= other_region[0] and \
           region[1] >= other_region[1] and \
           region[2] <= other_region[2] and \
           region[3] <= other_region[3]


def text_to_score(text):
    try:
        for l, d in LETTER_TO_DIGIT.items():
            text = text.replace(l, str(d))
        return int(text)
    except:
        return None


def iou(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    width = (x2 - x1)
    height = (y2 - y1)
    if (width < 0) or (height < 0):
        return 0.0
    area_overlap = width * height

    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_combined = area_a + area_b - area_overlap

    return area_overlap / area_combined


def region_from_text_box(text_box):
    # left, top, right, bottom
    return (
        text_box[0][0],
        text_box[1][1],
        text_box[2][0],
        text_box[3][1],
    )


def filter_to_region(text_results, region, iou_threshold):
    return [
        r for r in text_results
        if iou(region_from_text_box(r[0]), region) > iou_threshold
    ]


def best_result(text_results, region, iou_threshold):
    if not text_results:
        return None
    text_results = filter_to_region(text_results, region, iou_threshold)
    if not text_results:
        return None
    return max(text_results, key=lambda r: r[2])[1]


def get_current_context(frame, text_results) -> Context:
    money_text = best_result(
        text_results,
        relative_to(cfg.MONEY_REGION, cfg.META_REGION),
        0.2,
    )
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

    time = timedelta(seconds=int(secs), minutes=int(mins))

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


def mask_unused_regions(frame):
    mask = np.zeros_like(frame, dtype=bool)
    for region in [cfg.TIME_REGION, cfg.MONEY_REGION, cfg.LOCATION_TEXT_REGION, cfg.ROUND_TEXT_REGION, cfg.CT_SCORE_REGION, cfg.T_SCORE_REGION]:
        region = relative_to(region, cfg.META_REGION)
        mask[
            region[1]: region[3],
            region[0]: region[2],
        ] = True
    noise = np.random.normal(size=frame.shape) * 50
    noise = noise.astype(np.uint8)
    return np.where(mask, frame, noise)


def frame_to_observation(frame, reader):
    frame = mask_unused_regions(frame)
    text = reader.readtext(
        frame,
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


if __name__ == "__main__":
    screenshotter = d3dshot.create(capture_output="numpy", frame_buffer_size=1)
    reader = easyocr.Reader(["en"])

    while True:
        obs = make_observation(screenshotter, reader)
        print(obs)
    # bot.run(cfg.DISCORD_TOKEN)
