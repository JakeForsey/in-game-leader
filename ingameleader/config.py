ROUND_TEXT_REGION = (1211, 60, 1292, 87)  # Used to determine whether the player is alive or dead
ROUND_WINNER_ICON_REGION = (1220, 175, 1330, 285)
LOCATION_TEXT_REGION = (25, 38, 280, 77)
CT_SCORE_REGION = (1238, 43, 1274, 72)
T_SCORE_REGION = (1288, 43, 1324, 72)
TIME_REGION = (1242, 6, 1318, 37)
MINUTES_REGION = (1247, 7, 1265, 35)
SECONDS_REGION = (1280, 7, 1316, 35)
MONEY_REGION = (40, 479, 180, 523)

REGIONS = [
    ROUND_TEXT_REGION,
    ROUND_WINNER_ICON_REGION,
    LOCATION_TEXT_REGION,
    CT_SCORE_REGION,
    T_SCORE_REGION,
    TIME_REGION,
    MINUTES_REGION,
    SECONDS_REGION,
    MONEY_REGION,
]
META_REGION = (
    min([r[0] for r in REGIONS]),
    min([r[1] for r in REGIONS]),
    max([r[2] for r in REGIONS]),
    max([r[3] for r in REGIONS]),
)

ROUND_WINNER_PIXEL_SIGNATURES = {
    "T": (
        ((1280, 234), (200, 181, 123), True),
        ((1280, 210), (86, 76, 61), True),
    ),
    "CT": (
        ((1280, 225), (141, 155, 164), True),
        ((1256, 268), (141, 155, 164), True),
    )
}

CT_SCORE_PIXEL_SIGNATURES = {
    0: (
        # (x, y): (r, g, b),
        ((1238 + 14, 42 + 12), (181, 212, 238), True),
        ((1238 + 14, 42 + 21), (181, 212, 238), True),
        ((1238 + 22, 42 + 12), (181, 212, 238), True),
        ((1238 + 22, 42 + 21), (181, 212, 238), True),
        # Top / bottom tip
        ((1238 + 18, 42 + 6), (181, 212, 238), True),
        ((1238 + 18, 42 + 24), (181, 212, 238), True),
        # Middle
        ((1238 + 18, 42 + 15), (181, 212, 238), False),
    ),
    1: (
        ((1238 + 18, 42 + 6), (181, 212, 238), True),
        ((1238 + 18, 42 + 9), (181, 212, 238), True),
        ((1238 + 18, 42 + 12), (181, 212, 238), True),
        ((1238 + 18, 42 + 15), (181, 212, 238), True),
        ((1238 + 18, 42 + 18), (181, 212, 238), True),
        ((1238 + 18, 42 + 21), (181, 212, 238), True),
        ((1238 + 18, 42 + 24), (181, 212, 238), True),
        # Check against being a 4
        ((1238 + 14, 42 + 18), (181, 212, 238), False),

    )
}

T_SCORE_PIXEL_SIGNATURES = {
    0: (
        # (x, y): (r, g, b),
        # Left hand side
        ((1288 + 13, 42 + 12), (234, 209, 138), True),
        ((1288 + 13, 42 + 21), (234, 209, 138), True),
        # Right hand side
        ((1288 + 22, 42 + 12), (234, 209, 138), True),
        ((1288 + 22, 42 + 21), (234, 209, 138), True),
        # Top / bottom tip
        ((1288 + 18, 42 + 6), (234, 209, 138), True),
        ((1288 + 18, 42 + 24), (234, 209, 138), True),
        # Middle
        ((1288 + 18, 42 + 15), (234, 209, 138), False),
    ),
    1: (
        # Straight line down the middle
        ((1288 + 18, 42 + 6), (234, 209, 138), True),
        ((1288 + 18, 42 + 9), (234, 209, 138), True),
        ((1288 + 18, 42 + 12), (234, 209, 138), True),
        ((1288 + 18, 42 + 15), (234, 209, 138), True),
        ((1288 + 18, 42 + 18), (234, 209, 138), True),
        ((1288 + 18, 42 + 21), (234, 209, 138), True),
        ((1288 + 18, 42 + 24), (234, 209, 138), True),
        # Check against being a 4
        ((1288 + 13, 42 + 18), (234, 209, 138), False),

    )
}

DISCORD_TOKEN = "ODE0MjE2NjE5MjI4MjY2NTk2.YDaoUQ.EeruolfrNFItHV3UGYubqcbghNw"
