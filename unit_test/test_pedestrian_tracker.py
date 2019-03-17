import unittest
from utils.bounding_box import Bbox
from pedestrian.pedestrian_tracker import CentroidTracker


class TestCentroidTracker(unittest.TestCase):

    def test_tracker_update(self):
        tracker = CentroidTracker()
        pedestrians_bbox = []

        x0 = 10
        y0 = 10
        x1 = 50
        y1 = 50
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)

        x0 = 20
        y0 = 20
        x1 = 70
        y1 = 70
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)

        pedestrian_list = tracker.tracker_update(pedestrians_bbox)

        self.assertTrue(pedestrian_list.__len__() == 2)

    def test_add_new_pedestrian(self):
        tracker = CentroidTracker()
        pedestrians_bbox = []

        x0 = 10
        y0 = 10
        x1 = 50
        y1 = 50
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)
        pedestrian_list = tracker.tracker_update(pedestrians_bbox)
        self.assertTrue(pedestrian_list.__len__() == 1)

        x0 = 20
        y0 = 20
        x1 = 70
        y1 = 70
        bbox = Bbox(x0, y0, x1, y1)
        tracker.add_new_pedestrian(bbox)
        self.assertTrue(tracker.pedestrian_list.__len__() == 2)

    def test_update_pedestrian(self):
        tracker = CentroidTracker()
        pedestrians_bbox = []

        x0 = 10
        y0 = 10
        x1 = 50
        y1 = 50
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)

        x0 = 20
        y0 = 20
        x1 = 70
        y1 = 70
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)
        pedestrian_list = tracker.tracker_update(pedestrians_bbox)
        self.assertTrue(pedestrian_list.__len__() == 2)

        x0 = 30
        y0 = 30
        x1 = 30
        y1 = 30
        bbox = Bbox(x0, y0, x1, y1)
        result = tracker.update_pedestrian(1, bbox)

        self.assertTrue(result)
        self.assertTrue(tracker.pedestrian_list[0].bbox.x0 == 30)
        self.assertTrue(tracker.pedestrian_list[0].bbox.y0 == 30)
        self.assertTrue(tracker.pedestrian_list[0].bbox.x1 == 30)
        self.assertTrue(tracker.pedestrian_list[0].bbox.y1 == 30)

    def test_remove_pedestrian(self):
        tracker = CentroidTracker()
        pedestrians_bbox = []

        x0 = 10
        y0 = 10
        x1 = 50
        y1 = 50
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)

        x0 = 20
        y0 = 20
        x1 = 70
        y1 = 70
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)
        pedestrian_list = tracker.tracker_update(pedestrians_bbox)
        self.assertTrue(pedestrian_list.__len__() == 2)

        result = tracker.remove_pedestrian(1)
        self.assertTrue(result)

    def test_get_centroids_pedestrians(self):
        tracker = CentroidTracker()
        pedestrians_bbox = []

        x0 = 10
        y0 = 10
        x1 = 50
        y1 = 50
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)

        x0 = 20
        y0 = 20
        x1 = 70
        y1 = 70
        bbox = Bbox(x0, y0, x1, y1)
        pedestrians_bbox.append(bbox)
        pedestrian_list = tracker.tracker_update(pedestrians_bbox)
        self.assertTrue(pedestrian_list.__len__() == 2)

        centroids_list = tracker.get_centroids_pedestrians(pedestrian_list)

        self.assertIsNotNone(centroids_list)
        self.assertTrue(centroids_list.__len__() == 2)
        self.assertTrue(centroids_list[0][0] == 30.0)
        self.assertTrue(centroids_list[0][1] == 30.0)
        self.assertTrue(centroids_list[1][0] == 45.0)
        self.assertTrue(centroids_list[1][1] == 45.0)


if __name__ == '__main__':
    unittest.main()
