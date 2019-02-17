from pedestrian.pedestrian import Pedestrian
from utils.bounding_box import Bbox


class PedestrianDetector:

    def __init__(self):
        self.detections = []

    def detect_news(self, image):
        """
        Detects new pedestrians without duplicating information with those detected in the previous iteration
        :param image: new image to detect pedestrians
        :return: <list<Pedestrian>> Pedestrian list with the previous and news detections
        """
        id = 1
        bbox = Bbox(10, 10, 50, 50)
        p = Pedestrian(id, bbox)
        self.detections.append(p)

        id = 2
        bbox = Bbox(10, 10, 50, 50)
        p = Pedestrian(id, bbox)
        self.detections.append(p)

        id = 3
        bbox = Bbox(10, 10, 50, 50)
        p = Pedestrian(id, bbox)
        self.detections.append(p)

        id = 4
        bbox = Bbox(10, 10, 50, 50)
        p = Pedestrian(id, bbox)
        self.detections.append(p)

        return self.detections

