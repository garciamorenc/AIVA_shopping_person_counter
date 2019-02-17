import unittest
from pedestrian_counter import count


class TestPedestrianCounter(unittest.TestCase):

    def test_count(self):
        total = count(None)
        self.assertTrue(total >= 0)


if __name__ == '__main__':
    unittest.main()
