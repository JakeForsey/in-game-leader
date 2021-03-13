from datetime import datetime
import io
from pathlib import Path
from typing import List, Optional

from google.cloud import storage
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
from scipy import interpolate

from ingameleader import config as cfg
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
    "size": 26
}
UNSELECTED_TEXT_KWARGS = {
    "alpha": 0.7,
    "fontname": "Arial",
    "size": 22
}
client = storage.Client.from_service_account_json(
    json_credentials_path=cfg.GCP_SERVICE_ACCOUNT_JSON
)
bucket = client.get_bucket("in-game-leader-message")


def plot_strategies(strategies: List[Strategy], selected_strategy: Optional[Strategy] = None):
    image_ax_height = 7
    graph_ax_height = GAP_PER_STRATEGY * len(strategies)
    fig, axes = plt.subplots(
        2, 1,
        figsize=(12, image_ax_height + graph_ax_height),
        facecolor=(54 / 255, 57 / 255, 63 / 255),
        gridspec_kw={'height_ratios': [graph_ax_height, image_ax_height]}
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
        # TODO Split on spaces
        max_length = 15
        strategy_name = "\n".join([strategy.name[i: i + max_length] for i in range(0, len(strategy.name), max_length)])
        axes[0].text(1.1, y, f'{strategy_name} ({dist.stats()[0] * 100:.0f}%)', c=c, **text_kwargs)

    axes[0].axvline(0.5, 0, 5, c="grey", linestyle="--", alpha=1, linewidth=2)
    axes[0].axis("off")

    if selected_strategy is not None:
        map = selected_strategy.map
        map_path = cfg.CGSO_OVERVIEWS_PATH / Path(f"{map.ugly_name}_radar.dds")
        image = Image.open(map_path)

        axes[1].imshow(np.array(image))

        for route in selected_strategy.exemplar_routes:
            locations = [rtl.location for rtl in route.route_to_locations]
            xs = np.array([location.x for location in locations])
            ys = np.array([location.y for location in locations])

            if len(locations) >= 3:
                f, u = interpolate.splprep([xs, ys], s=2)
                xs, ys = interpolate.splev(np.linspace(0, 1, 100), f)

            axes[1].plot(xs, ys, "--", linewidth=4, c=colours[strategies.index(selected_strategy)])
            axes[1].scatter(xs[-1], ys[-1], s=150, c=colours[strategies.index(selected_strategy)])

        axes[1].axis("off")

    blob = bucket.blob(f"{str(datetime.now().timestamp()).replace('.', '_')}.png")

    with io.BytesIO() as f:
        plt.tight_layout()
        plt.savefig(f)
        f.seek(0)
        blob.upload_from_file(f, content_type="image/png")

    return blob.public_url
