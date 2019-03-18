class Pedestrian:

    def __init__(self, pedestrian_id, bbox):
        self.id = pedestrian_id
        self.bbox = bbox
        self.previous_bbox = None
        self.updated = True
        self.remove_counter = 0
        self.hasEnter = False  # Enter to shop

    def validate(self, boundary):
        """
        Check if a pedestrian is valid to take it into account as a pedestrian who has passed in front of the store
         and has not entered
        :param boundary: shop boundary
        :return Boolean about valid pedestrian who don't go inside shop
        """
        result = False
        if self.previous_bbox and not self.hasEnter:
            previous_point = int((self.previous_bbox.x0 + self.previous_bbox.x1) / 2)
            point = int((self.bbox.x0 + self.bbox.x1) / 2)

            self.__check_shop_boundary(boundary, previous_point)
            if not self.hasEnter:
                result = self.__check_valid_boundary(boundary, previous_point, point)

        return result

    def __check_valid_boundary(self, boundary, previous_point, actual_point):
        """
        Check if a pedestrian has passed in front of the store and has not entered
        :param boundary: shop boundary
        :param previous_point: previous point to check valid position
        :param actual_point: actual point to check valid position
        """
        previous = (boundary.x0 < previous_point < boundary.x1) and \
                   (boundary.y0 < self.previous_bbox.y1 < boundary.y1)

        now = (boundary.x0 > actual_point) or (boundary.x1 < actual_point)

        return previous and now

    def __check_shop_boundary(self, boundary, actual_point):
        """
        Check if the pedestrian has entered or left the store
        :param boundary: shop boundary
        :param actual_point: actual point to check valid position
        """
        self.hasEnter = (boundary.x0 <= actual_point <= boundary.x1) and (boundary.y0 >= self.bbox.y1)


