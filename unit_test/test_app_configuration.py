import unittest
from configuration.app_configuration import AppConfiguration
from utils.bounding_box import Bbox
import os.path


class TestAppConfiguration(unittest.TestCase):

    def test_load(self):
        conf = AppConfiguration()
        conf.load()
        self.assertEqual(214, conf.shop_bbox.x0)
        self.assertEqual(135, conf.shop_bbox.y0)
        self.assertEqual(360, conf.shop_bbox.x1)
        self.assertEqual(200, conf.shop_bbox.y1)
        self.assertEqual('resources/background.png', conf.background)

    def test_save(self):
        x0 = 214
        y0 = 135
        x1 = 360
        y1 = 200
        conf = AppConfiguration(Bbox(x0, y0, x1, y1), 'resources/background.png')
        result = conf.save()
        self.assertTrue(os.path.isfile('./config.xml'))
        self.assertTrue(result)

    def test_set_configuration(self):
        conf = AppConfiguration()
        x0 = 214
        y0 = 135
        x1 = 360
        y1 = 200
        background = 'resources/background.png'
        conf.set_configuration(x0, y0, x1, y1, background)
        self.assertEqual(conf.shop_bbox.x0, x0)
        self.assertEqual(conf.shop_bbox.y0, y0)
        self.assertEqual(conf.shop_bbox.x1, x1)
        self.assertEqual(conf.shop_bbox.y1, y1)
        self.assertEqual(conf.background, background)


if __name__ == '__main__':
    unittest.main()
