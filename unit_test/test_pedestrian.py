import unittest
from pedestrian.pedestrian import Pedestrian
from utils.bounding_box import Bbox


class TestPedestrian(unittest.TestCase):

    def test_validate_ok(self):
        bbox = Bbox(50, 150, 60, 170)
        p = Pedestrian(1, bbox)
        p.previous_bbox = Bbox(101, 150, 190, 170)

        boundary = Bbox(100, 100, 200, 200)
        result = p.validate(boundary)

        self.assertIsInstance(p.bbox, Bbox)

        self.assertFalse(p.hasEnter)
        self.assertTrue(result)

    def test_validate_fail(self):
        bbox = Bbox(101, 150, 190, 170)
        p = Pedestrian(1, bbox)
        p.previous_bbox = Bbox(101, 150, 190, 170)

        boundary = Bbox(100, 100, 200, 200)
        result = p.validate(boundary)

        self.assertIsInstance(p.bbox, Bbox)

        self.assertFalse(p.hasEnter)
        self.assertFalse(result)

    def test_validate_enter(self):
        bbox = Bbox(101, 50, 190, 50)
        p = Pedestrian(1, bbox)
        p.previous_bbox = Bbox(101, 150, 190, 170)

        boundary = Bbox(100, 100, 200, 200)
        result = p.validate(boundary)

        self.assertIsInstance(p.bbox, Bbox)

        self.assertTrue(p.hasEnter)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
