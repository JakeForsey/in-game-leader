from PIL import Image
from unittest import TestCase

import numpy as np
import easyocr

from ingameleader.app import frame_to_observation, extract
from ingameleader import config as cfg

from tests.screenshots import expected


class TestFrameToObservation(TestCase):
    def test_expected_results_for_screenshots(self):
        reader = easyocr.Reader(["en"])
        for image_path, expected_observation in expected.EXPECTED_OBSERVATIONS.items():
            print(f"Running tests against {image_path}")
            img = Image.open(image_path)
            frame = extract(cfg.META_REGION, np.array(img), (0, 0) + img.size)
            actual_observation = frame_to_observation(frame, reader)
            assert actual_observation == expected_observation
