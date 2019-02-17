import unittest
from configuration.app_configuration import AppConfiguration
from utils.bounding_box import Bbox
import os.path


class TestAppConfiguration(unittest.TestCase):

    def test_load(self):
        conf = AppConfiguration()
        conf.load()
        self.assertEqual(10, conf.shop_bbox.x0)
        self.assertEqual(10, conf.shop_bbox.x1)
        self.assertEqual(50, conf.shop_bbox.y0)
        self.assertEqual(50, conf.shop_bbox.y1)

    def test_save(self):
        conf = AppConfiguration()
        x0 = 10
        y0 = 50
        x1 = 10
        y1 = 50
        conf.shop = Bbox(x0, y0, x1, y1)
        result = conf.save()
        self.assertTrue(os.path.isfile('./config.xml'))
        self.assertTrue(result)

    def test_set_configuration(self):
        conf = AppConfiguration()
        x0 = 20
        y0 = 50
        x1 = 20
        y1 = 50
        conf.set_configuration(x0, y0, x1, y1)
        self.assertEqual(conf.shop_bbox.x0, x0)
        self.assertEqual(conf.shop_bbox.y0, y0)
        self.assertEqual(conf.shop_bbox.x1, x1)
        self.assertEqual(conf.shop_bbox.y1, y1)


if __name__ == '__main__':
    unittest.main()
