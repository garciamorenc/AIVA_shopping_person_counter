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

    def tracking(self, boundary):
        """
        Tracking the pedestrian to know if he has entered the store or not
        :param boundary: shop boundary
        :return Boolean
        """
        self.previous_bbox = self.bbox
        self.bbox = Bbox(0, 0, 10, 10)

        self._check_shop_boundary(boundary)
        if not self.hasEnter:
            self._check_valid_boundary(boundary)

        return self.is_valid

    def _check_valid_boundary(self, boundary):
        """
        Check if a pedestrian has passed in front of the store and has not entered
        :param boundary: shop boundary
        """
        self.is_valid = bool(random.getrandbits(1))

    def _check_shop_boundary(self, boundary):
        """
        Check if the pedestrian has entered or left the store
        :param boundary: shop boundary
        """
        self.hasEnter = bool(random.getrandbits(1))


