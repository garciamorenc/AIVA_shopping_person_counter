import cv2


class Drawer:
    """
    Helper class to draw Pedestrians, ROIs and all the needed information to debug de application
    """

    @staticmethod
    def __draw_rectangles(image, list_rectangles, color):
        """
        Given a set of rectangles and an image this allows to paint them on the image with the desired color
        :param image: Image on which the rectangles will be drawn
        :param list_rectangles: list with rectangles, a rectangle is a tuplE of two points which are tuples.
            Eg = ((x0, y0), (x1, y1)) Being the first point the left-top and the second point the right-bottom 
            of the bbox.
        :param color: Color of the rectangle that will be drawn
        """
        if len(list_rectangles) > 0:
            for rectangle in list_rectangles:
                cv2.rectangle(image, (rectangle.x0, rectangle.y0), (rectangle.x1, rectangle.y1), color, thickness=2)

    @staticmethod
    def draw_pedestrians(image, list_pedestrians, color):
        """
        Given a list of pedestrians, the bbox and the id for that pedestrian is draw
        :param image: Image on which the rectangles will be drawn
        :param list_pedestrians: list pedestrians to draw it
        :param color: Color of the rectangle that will be drawn
        """
        bbox_list = [pedestrian.bbox for pedestrian in list_pedestrians]
        Drawer.__draw_rectangles(image, bbox_list, color)

        red_color = (0, 0, 255)

        for pedestrian in list_pedestrians:
            id = str(pedestrian.id)
            bottom_left_corner_text = pedestrian.bbox.x0, pedestrian.bbox.y0 - 5
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.65
            font_color = red_color
            thickness = 2

            cv2.putText(image, id, bottom_left_corner_text, font, font_scale, font_color, thickness)

            # Centroid show
            x = round((pedestrian.bbox.x0 + pedestrian.bbox.x1) / 2)
            y = round((pedestrian.bbox.y0 + pedestrian.bbox.y1) / 2)
            centroid = (x, y)

            fill_circle = -1
            cv2.circle(image, centroid, 3, red_color, fill_circle)

    @staticmethod
    def draw_shop_boundary(image, boundary):
        """
        Given a image and a shop boundary to draw it
        :param image: camera image
        :param boundary: shop boundary
        """
        cv2.rectangle(image, (boundary.x0, boundary.y0), (boundary.x1, boundary.y1), (255, 0, 255), thickness=2)
