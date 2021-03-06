from ingameleader.seed import dust2, inferno, mirage


MAPS = [
    dust2.MAP,
    inferno.MAP,
    mirage.MAP,
]

STRATEGIES = dust2.STRATEGIES \
             + inferno.STRATEGIES \
             + mirage.STRATEGIES
