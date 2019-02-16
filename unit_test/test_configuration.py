import unittest
from mockup.mockup_methods import *
import os

class TestConfiguration(unittest.TestCase):

    def test_choose_entrance(self):
        image = []
        self.assertIsInstance(choose_entrance(image), Bbox)

    def test_save_entrance_configuration(self):
        self.assertTrue(save_entrance_configuration)
        self.assertTrue(os.path.isfile("filename.xml"))


    def test_configure_entrance(self):
        self.assertTrue(configure_entrance())

if __name__ == '__main__':
    unittest.main()