from pedestrian.backgroundSubtraction import BackgroundSubtraction
import numpy as np
import cv2
from abc import ABC, abstractmethod
from utils.bounding_box import Bbox


class PedestrianBaseDetector(ABC):
    """
    Interface that represents a common pedestrian detector class.
    """
    @abstractmethod
    def detect_news(self, frame):
        """
        Abstract method that has to be implemented to detect pedestrian by the class that inherits the
        PedestrianBaseDetector.
        :param frame: The frame to apply the detection to
        :return: Raise NotImplementedError exception
        """
        raise NotImplementedError


class PedestrianDetectorBackgroundSubtraction(PedestrianBaseDetector):
    """
    Class that implements the interface PedestrianBaseDetector. This class uses background subtraction techniques to
    detect changes on the image, and then using morphological operations and some conditions retrieves the detections
    that are Pedestrians.
    """

    def __init__(self, background, debug=False):
        self.__backgroundSubtraction = BackgroundSubtraction(cv2.imread(background), 30)
        self.__min_area_threshold = 250  # The minimum area a contour must have in order to be considered a detection.
        self.__debug = debug

    def detect_news(self, frame):
        """
        Method that given an image (frame) returns the Bbox that are Pedestrians.
        :param frame: Image where the detections will be made
        :return: A list of Bbox, each Bbox represents a Pedestrian location.
        """
        detections_list = []
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
                area = cv2.contourArea(contour)
                if area > self.__min_area_threshold:
                    x, y, w, h = cv2.boundingRect(contour)
                    bbox = Bbox(x, y, x+w, y+h)
                    detections_list.append(bbox)

        return detections_list

