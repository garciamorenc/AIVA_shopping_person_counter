from pedestrian.backgroundSubtraction import BackgroundSubtraction
import numpy as np
import cv2
from abc import ABC, abstractmethod
from utils.bounding_box import Bbox


class PedestrianBaseDetector(ABC):
    @abstractmethod
    def detect_news(self, frame):
        pass


class PedestrianDetectorBackgroundSubtraction(PedestrianBaseDetector):

    def __init__(self, background, debug=False):
        self.__backgroundSubtraction = BackgroundSubtraction(cv2.imread(background), 30)
        self.__min_area_threshold = 250  # The minimum area a contour must have in order to be considered a detection.
        self.__debug = debug

    def detect_news(self, frame):
        rectangles = []
        background_mask = self.__backgroundSubtraction.moving_average_exponential_subtraction(frame, alpha=0.05)

        kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_OPEN, kernel_small)

        kernel_big = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_CLOSE, kernel_big)

        # Debug mode
        if self.__debug:
            cv2.imshow("win", background_mask)
            cv2.waitKey(1)

        background_mask = background_mask.astype(np.uint8)
        im2, contours, hierarchy = cv2.findContours(background_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                if area > self.__min_area_threshold:
                    bbox = Bbox(x, y, x+w, y+h)
                    rectangles.append(bbox)

        return rectangles

