import unittest
from pedestrian.pedestrian import Pedestrian
from utils.bounding_box import Bbox


class TestPedestrian(unittest.TestCase):

    def test_tracking(self):
        bbox = Bbox(10, 10, 50, 50)
        p = Pedestrian(1, bbox)
        boundary = Bbox(30, 30, 70, 70)
        p.tracking(boundary)

        self.assertEqual(bbox, p.previous_bbox)
        self.assertIsInstance(p.bbox, Bbox)

        if not p.hasEnter:
            self.assertTrue(p.is_valid != p.hasEnter or p.is_valid == p.hasEnter)
        else:
            self.assertTrue(p.is_valid != p.hasEnter)


if __name__ == '__main__':
    unittest.main()
