import unittest
from mockup.mockup_methods import *

class TestPersonCounter(unittest.TestCase):

    def test_pedestrian_detector(self):
        image = []
        detected_pedestrians = pedestrian_detector(image)

        self.assertEqual(detected_pedestrians[0].x0, 0)
        self.assertEqual(detected_pedestrians[0].y0, 0)
        self.assertEqual(detected_pedestrians[0].x1, 10)
        self.assertEqual(detected_pedestrians[0].y1, 10)

        self.assertEqual(detected_pedestrians[1].x0, 20)
        self.assertEqual(detected_pedestrians[1].y0, 20)
        self.assertEqual(detected_pedestrians[1].x1, 100)
        self.assertEqual(detected_pedestrians[1].y1, 100)

    def test_pedestrian_detector(self):
        detected_pedestrian_previous = []
        detected_pedestrians = []
        tracked_pedestrians = pedestrian_tracking(detected_pedestrian_previous, detected_pedestrians)
        for idx, tracked_pedestrian in enumerate(tracked_pedestrians):
            self.assertEqual(tracked_pedestrian.id, idx)
            self.assertEqual(tracked_pedestrian.bbox.x0, 0)
            self.assertEqual(tracked_pedestrian.bbox.y0, 0)
            self.assertEqual(tracked_pedestrian.bbox.x1, 10)
            self.assertEqual(tracked_pedestrian.bbox.y1, 10)

    def test_hasEnterTheShop(self):
        detected_pedestrian_previous = []
        detected_pedestrians = []
        tracked_pedestrians = pedestrian_tracking(detected_pedestrian_previous, detected_pedestrians)
        for tracked_pedestrian in tracked_pedestrians:
            self.assertFalse(tracked_pedestrian.hasEnter)
        tracked_pedestrians = hasEnterTheShop(tracked_pedestrians)
        for tracked_pedestrian in tracked_pedestrians:
            self.assertTrue(tracked_pedestrian.hasEnter)


if __name__ == '__main__':
    unittest.main()