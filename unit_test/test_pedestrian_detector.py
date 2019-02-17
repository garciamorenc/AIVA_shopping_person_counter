import unittest
import numpy as np
from pedestrian.pedestrian_detector import PedestrianDetector


class TestPedestrianDetector(unittest.TestCase):

    def test_detect_news(self):
        detector = PedestrianDetector()
        image = np.zeros((10, 10))
        detections = detector.detect_news(image)
        self.assertEqual(detections, detector.detections)
        self.assertIsNotNone(detections)
        self.assertIsInstance(detections, list)


if __name__ == '__main__':
    unittest.main()
