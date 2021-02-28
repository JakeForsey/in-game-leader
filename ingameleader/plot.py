import os
import tempfile
from typing import List

from filestack import Client as FileStackClient
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

from ingameleader.model.strategy import Strategy

GAP_PER_STRATEGY = 1.5
SELECTED_PDF_LINE_KWARGS = {
    "linewidth": 5,
    "linestyle": "-",
    "alpha": 1.0,
}
UNSELECTED_PDF_LINE_KWARGS = {
    "linewidth": 5,
    "linestyle": "--",
    "alpha": 0.4,
}
SELECTED_TEXT_KWARGS = {
    "alpha": 1,
    "fontname": "Arial",
    "size": 28
}
UNSELECTED_TEXT_KWARGS = {
    "alpha": 0.4,
    "fontname": "Arial",
    "size": 18
}
client = FileStackClient(os.getenv("FILESTACK_APIKEY"))


def plot_strategies(strategies: List[Strategy], selected_strategy_index):
    plt.figure(figsize=(7, 4), facecolor=(54 / 255, 57 / 255, 63 / 255))

    x = np.linspace(0, 1, 50)
    colours = ["teal", "orange", "green", "yellow"]
    for i in range(len(strategies) - 1, -1, -1):
        y = i * GAP_PER_STRATEGY
        strategy = strategies[i]
        if selected_strategy_index is not None:
            selected = i == selected_strategy_index
        else:
            selected = True
        c = colours[i]
        line_kwargs = SELECTED_PDF_LINE_KWARGS if selected else UNSELECTED_PDF_LINE_KWARGS
        text_kwargs = SELECTED_TEXT_KWARGS if selected else UNSELECTED_TEXT_KWARGS

        dist = beta(
            strategy.alpha + strategy.wins,
            strategy.beta + strategy.losses
        )

        plt.plot(x, dist.pdf(x) + y, c=c, **line_kwargs)
        plt.text(1.1, y, f'{strategy.strategy_name} ({dist.stats()[0] * 100:.0f}%)', c=c, **text_kwargs)

    plt.axvline(0.5, 0, 5, c="grey", linestyle="--", alpha=1, linewidth=2)
    _ = plt.axis("off")
    plt.tight_layout()

    tmp = tempfile.TemporaryFile()
    plt.savefig(tmp.name)
    image_link = client.upload(filepath=tmp.name + ".png")
    return image_link.url

