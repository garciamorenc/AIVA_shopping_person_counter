import numpy as np
import cv2


class BackgroundSubtraction:

    def __init__(self, background, threshold):
        self.backgroundImage = background
        self.threshold = threshold
        self.background_images_count = 0
        self.ringbuffer_backgrounds = None

    def static_subtraction(self, frame):
        """
        Given an image, the background is subtracted creating a mask to see the changes in the static image.
        :param frame: input image to apply static subtraction
        :return:
        """
        #TODO que coño devuelve ¿?¿?
        frame = frame.astype(np.int16)
        self.backgroundImage = self.backgroundImage.astype(np.int16)
        subtraction = np.abs(np.subtract(frame, self.backgroundImage))
        subtraction_mask = (subtraction[:, :, 0] > self.threshold) | (subtraction[:, :, 1] > self.threshold) | (subtraction[:, :, 2] > self.threshold)
        subtraction_mask = np.multiply(1, subtraction_mask).astype(float)

        return subtraction_mask

    # Explained
    # https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    # https://tttapa.github.io/Pages/Mathematics/Systems-and-Control-Theory/Digital-filters/Exponential%20Moving%20Average/Exponential-Moving-Average.html
    # Opencv implementation ->  http://answers.opencv.org/question/94520/background-subtraction-using-running-average-in-opencv/
    # Opencv implementation ->  https://docs.opencv.org/2.4/modules/imgproc/doc/motion_analysis_and_object_tracking.html#accumulateweighted
    def moving_average_exponential_subtraction(self, frame, alpha):
        """

        :param frame:
        :param alpha:
        :return:
        """
        #TODO que pongo ¿?¿?
        # With this new background, subtract the background to the new frame
        subtraction_mask = self.static_subtraction(frame)
        # Update the background using the moving average
        accu_weight = cv2.accumulateWeighted(frame, self.backgroundImage.astype(float), alpha)
        self.backgroundImage = cv2.convertScaleAbs(accu_weight)  # Use this to convert to uint8
        return subtraction_mask
