import os
from pathlib import Path
import tempfile
from typing import List, Optional

from filestack import Client as FileStackClient
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
from scipy import interpolate

from ingameleader.model.dao import Strategy


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
    "size": 24
}
UNSELECTED_TEXT_KWARGS = {
    "alpha": 0.4,
    "fontname": "Arial",
    "size": 12
}
client = FileStackClient(os.getenv("FILESTACK_APIKEY"))


def plot_strategies(strategies: List[Strategy], selected_strategy: Optional[Strategy] = None):
    fig, axes = plt.subplots(
        2, 1,
        figsize=(7, 7 + (2 * len(strategies))),
        facecolor=(54 / 255, 57 / 255, 63 / 255)
    )

    x = np.linspace(0, 1, 50)
    colours = ["teal", "orange", "green", "yellow", "darkslateblue", "crimson"]
    for i in range(len(strategies) - 1, -1, -1):
        y = i * GAP_PER_STRATEGY
        strategy = strategies[i]
        if selected_strategy is not None:
            selected = strategy == selected_strategy
        else:
            selected = True
        c = colours[i]
        line_kwargs = SELECTED_PDF_LINE_KWARGS if selected else UNSELECTED_PDF_LINE_KWARGS
        text_kwargs = SELECTED_TEXT_KWARGS if selected else UNSELECTED_TEXT_KWARGS

        dist = beta(
            strategy.alpha + strategy.wins,
            strategy.beta + strategy.losses
        )

        axes[0].plot(x, dist.pdf(x) + y, c=c, **line_kwargs)
        axes[0].text(1.1, y, f'{strategy.name} ({dist.stats()[0] * 100:.0f}%)', c=c, **text_kwargs)

    axes[0].axvline(0.5, 0, 5, c="grey", linestyle="--", alpha=1, linewidth=2)
    axes[0].axis("off")

    if selected_strategy is not None:
        map = selected_strategy.map
        # TODO Get path from map
        overview_path = Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\resource\\overviews")
        de_dust2_radar = overview_path / Path("de_dust2_radar.dds")
        image = Image.open(de_dust2_radar)

        axes[1].imshow(np.array(image))

        for route in selected_strategy.exemplar_routes:
            locations = [rtl.location for rtl in route.route_to_locations]
            xs = np.array([location.x for location in locations])
            ys = np.array([location.y for location in locations])

            f, u = interpolate.splprep([xs, ys], k=2)
            xs, ys = interpolate.splev(np.linspace(0, 1, 100), f)

            axes[1].plot(xs, ys, "--", linewidth=4, c=colours[strategies.index(selected_strategy)])
            axes[1].scatter(xs[-1], ys[-1], s=150, c=colours[strategies.index(selected_strategy)])

        axes[1].axis("off")

    tmp = tempfile.TemporaryFile()
    plt.tight_layout()
    plt.savefig(tmp.name)
    plt.savefig("testing.png")
    # TODO Replace with AWS / GCP / Azure
    image_link = client.upload(filepath=tmp.name + ".png")
    return image_link.url
