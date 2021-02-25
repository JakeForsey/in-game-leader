ROUND_TEXT_REGION = (1211, 60, 1292, 87)
LOCATION_TEXT_REGION = (25, 38, 280, 77)
CT_SCORE_REGION = (1238, 42, 1274, 73)
T_SCORE_REGION = (1288, 42, 1324, 73)
TIME_REGION = (1242, 5, 1318, 38)
MINUTES_REGION = (1248, 7, 1264, 35)
SECONDS_REGION = (1282, 7, 1316, 35)
MONEY_REGION = (41, 480, 180, 522)

REGIONS = [
    LOCATION_TEXT_REGION,
    CT_SCORE_REGION,
    T_SCORE_REGION,
    ROUND_TEXT_REGION,     # Used to determine whether the player is alive or dead
    TIME_REGION,
    MONEY_REGION,
]
META_REGION = (
    min([r[0] for r in REGIONS]),
    min([r[1] for r in REGIONS]),
    max([r[2] for r in REGIONS]),
    max([r[3] for r in REGIONS]),
)

CT_SCORE_PIXEL_SIGNATURE = (
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
)

T_SCORE_PIXEL_SIGNATURE = (
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
)

DISCORD_TOKEN = "ODE0MjE2NjE5MjI4MjY2NTk2.YDaoUQ.EeruolfrNFItHV3UGYubqcbghNw"
