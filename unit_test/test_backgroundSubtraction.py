import unittest
import cv2
import numpy as np
from pedestrian.backgroundSubtraction import BackgroundSubtraction


class TestBackgroundSubtraction(unittest.TestCase):

    def test_static_subtraction(self):
        background_subtraction = BackgroundSubtraction(cv2.imread('resources/background.png'), 30)

        mask = None
        cap = cv2.VideoCapture('dataset_2/ThreePastShop1front.mpg')
        ret, frame = cap.read()
        if ret:
            mask = background_subtraction.static_subtraction(frame)
        else:
            self.assertFalse(False)

        m, n = mask.shape
        self.assertIsNotNone(mask)
        self.assertTrue(m == 288)
        self.assertTrue(n == 384)
        self.assertTrue(np.count_nonzero(mask) > 0)

    def test_moving_average_exponential_subtraction(self):
        background_subtraction = BackgroundSubtraction(cv2.imread('resources/background.png'), 30)

        mask = None
        cap = cv2.VideoCapture('dataset_2/ThreePastShop1front.mpg')
        ret, frame = cap.read()
        if ret:
            mask = background_subtraction.moving_average_exponential_subtraction(frame, 0.05)
        else:
            self.assertFalse(False)

        m, n = mask.shape
        self.assertIsNotNone(mask)
        self.assertTrue(m == 288)
        self.assertTrue(n == 384)
        self.assertTrue(np.count_nonzero(mask) > 0)


if __name__ == '__main__':
    unittest.main()
