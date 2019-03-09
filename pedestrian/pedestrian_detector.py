from pedestrian.pedestrian import Pedestrian
from utils.bounding_box import Bbox
from pedestrian.backgroundSubtraction import BackgroundSubtraction
import numpy as np

import os
import cv2
import sys
# Python 3.4+
from abc import ABC, abstractmethod


class PedestrianBaseDetector(ABC):
    @abstractmethod
    def load(self, app_configuration):
        pass

    @abstractmethod
    def detect_news(self):
        pass

class PedestrianDetectorSSD(PedestrianBaseDetector):
    '''
    Class to detect pedestrians.
    https://github.com/chuanqi305/MobileNet-SSD
    '''

    def __init__(self):
        self.detections = []
        self.__nn_graph = r"resources/MobileNetSSD_deploy.prototxt"
        self.__nn_weights = r"resources/MobileNetSSD_deploy.caffemodel"
        self.neural_network = None

    def load(self, app_configuration, model_path = "", weights_path = ""):
        '''
        Use this method to load a neural network to recognize or detect people. If you dont want to load a model and use
        the default model, just dont put anything on model_path or weights_path
        :param model_path: The path to the model
        :param weights_path: The weights of the model
        :return:
        '''
        #TODO: work only with configuration, get the path to the neural network files from config
        result = False
        if (not os.path.isfile(model_path) or not os.path.isfile(weights_path)):
            print("The path to the model or weights is wrong, not a file located. Please check the paths to the files")
            sys.exit(-1)

        if (model_path == "" or weights_path == ""):
            model_path = os.path.normpath(self.__nn_graph)
            weights_path = os.path.normpath(self.__nn_weights)

        net = cv2.dnn.readNetFromCaffe(model_path, weights_path)
        #Que devuelve la red cuando no se carga bien, por ejemplo al no encontrar un fichero????
        if (net == None):
            print("Error couldnt load the neural network")
            result = False
        else:
            self.neural_network = net
            result = True
        return result

    def __keep_limits(self, number):
        '''
        Used to keep a number between certain limits. Since the SSD uses fixed size rectangles for detection, the
        detections or bbox returned can sometimes go outside the image Eg: y_right_bottom = 1.0002 and this will result
        in the bounding box going out of scope for the image. Since this is undesired this method checks this and if the
        limits are surpass the point is changed to the inferior or superior limit.
        :param number: The number which limits will be checked
        :return: The number new value in case the limits were surpass
        '''
        return min(max(number, 0.0), 1.0)

    def detect_news(self, frame, threshold_confidence = 0.5):
        '''
        With a preloaded network using load_neural_network(), use this network to detect on the image pedestrians and
        returns the detections as rectangle or bbox(bounding boxes).
        http://www.ebenezertechs.com/mobilenet-ssd-using-opencv-3-4-1-deep-learning-module-python/
        :param frame: Image where the detections will be made
        :param conficence: Values used as a threshold for detection.
        :return: List of bounding box, rectangles. Each rectangle is a tupla with the following structure
        ((x_left_top, y_left_top), (x_right_bottom, y_right_bottom))
        '''

        classes_dict = {"background": 0, "aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4,
                   "bottle": 5, "bus": 6, "car": 7, "cat": 8, "chair": 9, "cow": 10, "diningtable": 11,
                   "dog": 12, "horse": 13, "motorbike": 14, "person": 15, "pottedplant": 16, "sheep": 17,
                   "sofa": 18, "train": 19, "tvmonitor": 20}

        # List that will save the bounding box of the detections that surpass the thresholds and are person.
        person_detections = []

        # Prepossess input of the network
        frame_resized = cv2.resize(frame, (300, 300))  # La red espera 300x300

        # Se usa para adaptar la imagen a lo que espera la red (normalizacion de la media, pasar a RGB de BGR...)
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5),
                                     False)
        # Predict
        self.neural_network.setInput(blob)
        detections = self.neural_network.forward()

        #print("Detections: " + str(detections.shape[2]))

        # Size of frame resize (300x300)
        rows = frame_resized.shape[0]  # Height
        cols = frame_resized.shape[1]
        # For get the class and location of object detected,
        # There is a fix index for class, location and confidence
        # value in @detections array .
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Confidence of prediction
            if confidence > threshold_confidence:  # Filter prediction
                class_id = int(detections[0, 0, i, 1])  # Class label
                if (class_id == classes_dict["person"]):
                    # Object location
                    x_left_top = int(self.__keep_limits(detections[0, 0, i, 3]) * cols)
                    y_left_top = int(self.__keep_limits(detections[0, 0, i, 4]) * rows)
                    x_right_bottom = int(self.__keep_limits(detections[0, 0, i, 5]) * cols)
                    y_right_bottom = int(self.__keep_limits(detections[0, 0, i, 6]) * rows)

                    # Factor for scale to original size of frame
                    heightFactor = frame.shape[0] / 300.0
                    widthFactor = frame.shape[1] / 300.0
                    # Scale object detection to frame
                    x_left_top = int(widthFactor * x_left_top)
                    y_left_top = int(heightFactor * y_left_top)
                    x_right_bottom = int(widthFactor * x_right_bottom)
                    y_right_bottom = int(heightFactor * y_right_bottom)
                    rectangle = ((x_left_top, y_left_top), (x_right_bottom, y_right_bottom))
                    person_detections.append(rectangle)

        return person_detections


class PedestrianDetectorBackgroundSubstraction(PedestrianBaseDetector):

    def __init__(self):
        self.detections = []
        self.backgroundSubtractor = None
        #The minimun area a contour must have in order to be considered a detection.
        self.min_area_threshold = None

    def load(self, app_configuration, path_image_background):
        #TODO: load configuration or sometehing
        self.backgroundSubtractor = BackgroundSubtraction()
        self.backgroundSubtractor.backgroundImage = cv2.imread(path_image_background) #TODO: Obtenerlo de la configuracion
        self.backgroundSubtractor.threshold = 30 #TODO: get from config
        self.min_area_threshold = 100 #TODO: get from config

    def detect_news(self, frame):
        rectangles = []

        background_mask = self.backgroundSubtractor.static_subtraction(frame)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_OPEN, kernel) #Eliminar ruido
        background_mask = cv2.morphologyEx(background_mask, cv2.MORPH_CLOSE, kernel) #Juntar zonas
        # TODO: operaciones morfologicas como cierre y apertura para eliminar ruido y unir elementos que sean el
        #  mismo probar que tal el comportamiento.

        #TESTING ONLY
        test = True
        if (test):
            cv2.imshow("win", background_mask)
            cv2.waitKey(1)
            cv2.destroyWindow("win")

        background_mask = background_mask.astype(np.uint8)
        im2, contours, hierarchy = cv2.findContours(background_mask, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        if (len(contours) > 0):
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                if (area > self.min_area_threshold):
                    top_left_point = (x, y)
                    bottom_rigth_point = (x + w, y + h)
                    rectangles.append((top_left_point, bottom_rigth_point))

        return rectangles



    #
    # # NO DETECTA NADA
    # def detect_news_HOG(self, frame):
    #     # NO CREAR EL HOG DESCRIPTOR TODO EL RATO SINO CREARLO EN UN LOAD O ALGO.
    #
    #     # Detection of the pedestrians
    #     hog = cv2.HOGDescriptor()
    #     hog.setSVMDetector(
    #         cv2.HOGDescriptor_getDefaultPeopleDetector())
    #     rects, weights = hog.detectMultiScale(frame,
    #                                           winStride=(4, 4),
    #                                           padding=(8, 8),
    #                                           scale=1.01)
    #
    #     rects_tuple_style = []
    #     for rect in rects:
    #         top_left_point = (rect[0], rect[1])  # (...) Creates a tuple instead of [] -> LIST
    #         width = rect[2]
    #         height = rect[3]
    #         bottom_right_point = (top_left_point[0] + width, top_left_point[1] + height)
    #         rects_tuple_style.append((top_left_point, bottom_right_point))
    #
    #     return rects_tuple_style, weights