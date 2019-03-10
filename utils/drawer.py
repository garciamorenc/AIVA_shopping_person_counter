import cv2

def draw_rectangles(image, list_rectangles, color):
    '''
    Given a set of rectangles and an image this allows to paint them on the image with the desired color
    :param image: Image on which the rectangles will be drawn
    :param list_rectangles: list with rectangles, a rectangle is a tupla of two points which are tuplas.
    Eg = ((x0, y0), (x1, y1)) Being the first point the left-top and the second point the right-bottom of the bbox.
    :param color: Color of the rectangle that will be drawn
    :return: Empty.
    '''
    if (len(list_rectangles) > 0):
        for rectangle in list_rectangles:

            left_top_point = rectangle[0]
            right_bottom_point = rectangle[1]
            cv2.rectangle(image, left_top_point, right_bottom_point, color, thickness=2)


def draw_pedestrians(image, list_pedestrians, color):
    '''
    Given a list of pedestrians, the bbox and the id for that pedestrian is draw
    :param image:
    :param list_pedestrians:
    :param color:
    :return:
    '''
    bbox_list = [pedestrian.bbox for pedestrian in list_pedestrians]
    draw_rectangles(image, bbox_list, color)

    for pedestrian in list_pedestrians:
        id = str(pedestrian.id)
        bottomLeftCornerOfText = pedestrian.bbox[0][0], pedestrian.bbox[0][1] - 5
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.65
        fontColor = color
        thickness = 1

        cv2.putText(image, id, bottomLeftCornerOfText, font, fontScale, fontColor, thickness)
