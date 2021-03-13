import numpy as np

from ingameleader import config as cfg


LETTER_TO_DIGIT = {
    "G": 6,
    "D": 0,
    "g": 9
}

LOCATION_LOOKUP = {
    "gtstart": "ctstart",
    "dutside": "outside",
    "dutsidelong": "outsidelong",
    "qutsidelong": "outsidelong",
    "dutsidetunnel": "outsidetunnel",
    "tapafmid": "topofmid",
    "ofmid": "topofmid",
    "top": "topofmid",
    "tstert": "tstart",
    "langdoors": "longdoors",
    "longdaors": "longdoors",
    "longdoprs": "longdoors",
    "gatwalk": "catwalk",
    "middbors": "middoors",
    "bambsitea": "bombsiteb",
}


def format_location(text):
    location = text.replace(" ", "").lower()
    return LOCATION_LOOKUP.get(location, location)


def mask_unused_regions(frame):
    frame = frame.copy()
    mask = np.zeros_like(frame, dtype=bool)
    for region in cfg.REGIONS:
        region = relative_to(region, cfg.META_REGION)
        mask[
            region[1]: region[3],
            region[0]: region[2],
        ] = True
    noise = np.random.normal(size=frame.shape) * 50
    noise = noise.astype(np.uint8)
    return np.where(mask, frame, noise)


def match_signature(frame, signature, meta_region=cfg.META_REGION):
    for position, colour, expectation in signature:
        position = relative_to(position, meta_region)
        value = frame[position[1], position[0]]
        if (np.abs(value - np.array(colour)) < 20).all() != expectation:
            return False
    return True


def extract(region, frame, meta_region=cfg.META_REGION):
    frame = frame.copy()
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
