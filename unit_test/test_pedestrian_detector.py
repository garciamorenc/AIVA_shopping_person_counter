import unittest
import cv2
from pedestrian.pedestrian_detector import PedestrianDetectorBackgroundSubtraction


class TestPedestrianDetector(unittest.TestCase):

    def test_detect_news(self):
        detector = PedestrianDetectorBackgroundSubtraction('resources/background.png', False)
        cap = cv2.VideoCapture('dataset_2/ThreePastShop1front.mpg')
        pedestrians_bbox = []
        ret, frame = cap.read()
        if ret:
            pedestrians_bbox = detector.detect_news(frame=frame)
        else:
            self.assertFalse(False)

        self.assertIsNotNone(pedestrians_bbox)
        self.assertTrue(pedestrians_bbox.__len__() == 2)
        self.assertIsInstance(pedestrians_bbox, list)


if __name__ == '__main__':
    unittest.main()
