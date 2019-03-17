import random
from utils.bounding_box import Bbox


class Pedestrian:

    def __init__(self, id, bbox):
        self.id = id
        self.bbox = bbox
        self.previous_bbox = None
        self.matching_parameters = None
        self.updated = True
        self.remove_counter = 0
        self.hasEnter = False  # Enter to shop
        self.is_valid = False  # Passed in front of the store and has not entered

    def validate(self, boundary):
        """
        Tracking the pedestrian to know if he has entered the store or not
        :param boundary: shop boundary
        :return Boolean
        """
        if self.previous_bbox and not self.hasEnter:
            previous_point = int((self.previous_bbox.x0 + self.previous_bbox.x1) / 2)
            point = int((self.bbox.x0 + self.bbox.x1) / 2)

            self.__check_shop_boundary(boundary, previous_point)
            if not self.hasEnter:
                self.__check_valid_boundary(boundary, previous_point, point)

            return point, self.bbox.y1
        else:
            return 0, 0 #TODO borrar y devolver bool

    def __check_valid_boundary(self, boundary, previous_point, actual_point):
        """
        Check if a pedestrian has passed in front of the store and has not entered
        :param boundary: shop boundary
        """
        previous = (boundary.x0 < previous_point < boundary.x1) and \
                   (boundary.y0 < self.previous_bbox.y1 < boundary.y1)

        now = (boundary.x0 > actual_point) or (boundary.x1 < actual_point)

        self.is_valid = previous and now
        return previous and now

    def __check_shop_boundary(self, boundary, actual_point):
        """
        Check if the pedestrian has entered or left the store
        :param boundary: shop boundary
        """
        self.hasEnter = (boundary.x0 <= actual_point <= boundary.x1) and (boundary.y0 >= self.bbox.y1)


