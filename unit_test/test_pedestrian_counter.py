import unittest
from pedestrian_counter import PedestrianCounter


class TestPedestrianCounter(unittest.TestCase):

    def test_count(self):
        counter = PedestrianCounter()
        total = counter.count('./dataset_2/ThreePastShop1front.mpg', False)
        self.assertTrue(total == 3)


if __name__ == '__main__':
    unittest.main()
