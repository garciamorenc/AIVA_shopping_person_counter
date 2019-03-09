import numpy as np
from collections import deque
from collections import Counter
from numba import jit
import utils
import cv2

#FIFO
class RingBuffer:
    def __init__(self, size):
        self.data = deque([None for i in range(size)])

    def append(self, x):
        self.data.popleft()
        self.data.append(x)

    def get(self):
        return self.data

    def isFilled(self):
        #if None not in self.data: #Funciona hasta que deja de ser una lista de elementos y pasa a ser una lista de numpy arrays (logico)
        if (all(type(element) == np.ndarray for element in self.data)):
            return True
        else:
            return False

class BackgroundSubtraction:

    def __init__(self):
        self.backgroundImage = None
        self.threshold = 0
        self.background_images_count = 0
        self.ringbuffer_backgrounds = None

    # Given an image or frame, the background is subtracted creating a mask to see the changes in the static image.
    # Returns: A boolean image
    def static_subtraction(self, frame):
        # Importante: Los frames los lees de opencv normalmente como uint8, esto al restar uno al otro es facil que haga overflow y 0-2=254, por lo que pasamos a 16bits
        # y ademas con signo. Lo ideal seria que al pasarlos ya vinieran en ese formato.
        frame = frame.astype(np.int16)
        self.backgroundImage = self.backgroundImage.astype(np.int16)
        subtraction = np.abs(np.subtract(frame, self.backgroundImage))

        #subtraction_mask = np.logical_or( np.logical_or(subtraction[:, :, 0] > self.threshold, subtraction[:, :, 1] > self.threshold), subtraction[:, :, 2] > self.threshold)
        subtraction_mask = (subtraction[:, :, 0] > self.threshold) | (subtraction[:, :, 1] > self.threshold) | (subtraction[:, :, 2] > self.threshold)

        #OpenCv imshow() no trabaja con mascaras o arrays booleanos, normalizar entre 0-1 y pasar a float para que imshow automaticamente lo pase a 0-255.
        subtraction_mask = np.multiply(1, subtraction_mask).astype(float)

        return subtraction_mask


    # This method updates the background with the latest frame each time is called. The background subtraction is always done
    # between the last frame and the new one. "frame_k - frame_k+1"
    def consecutive_differences(self, frame):
        # 1. Apply the subtraction
        subtraction_mask = self.static_subtraction(frame)
        # 2. Once the subtraction is donde update the value of the background to the last frame
        self.backgroundImage = frame
        return subtraction_mask

    # Using the last n where n is background_images_count, the average of all the last n images is used to calculate the
    # background image. This background image is the image that will be use for the subtraction. If the ringbuffer hasnt
    # been created, is created.
    # Returns None in case is still buffering with images, not filled, the mask otherwise
    # In case the background is requiered to be reset, do it manually in the properties of the class.
    def average_subtraction(self, frame, background_images_count):
        subtraction_mask = None
        if (self.ringbuffer_backgrounds == None):
            self.background_images_count = background_images_count
            self.ringbuffer_backgrounds = RingBuffer(self.background_images_count)

        if (self.ringbuffer_backgrounds.isFilled()):
            self.backgroundImage = np.mean(self.ringbuffer_backgrounds.data, axis=0) #Sobre cada elemento de la lista
            subtraction_mask = self.static_subtraction(frame)

        # Append the new frame
        self.ringbuffer_backgrounds.append(frame)
        return subtraction_mask

    # Use to get the most repeated pixel value in a set of images. Use by moda:subtraction().
    # Images must be a tensor with (numberImages, height, width, channels)
    def getMostRepeatedPixelValue(self, images):
        numberImages, height, width, channels = np.shape(images)
        moda_image = np.zeros((height, width, channels))
        moda_image_test = np.zeros((height, width, channels)) #Test only
        for channel in range(0, channels):
            for row in range(0, height):
                for column in range(0, width):
                    value_list = []
                    for image in images:
                        value_list.append(image[row, column, channel])

                    #elements_counter = Counter(value_list)

                    elements_counter = [(value_list.count(x), x)for x in set(value_list)]
                    numberOcurrences, max_value = max(elements_counter)
                    moda_image[row, column, channel] = max_value

                    #TEST PARA VER QUE AMBAS FUNCIONES HACEN LO MISMO
                    # max_value_list = []
                    # number_ocurrences = []
                    # # elements_counter = [[x, value_list.count(x)] for x in set(value_list)]
                    # for x in set(value_list):
                    #     max_value_list.append(x)
                    #     number_ocurrences.append(value_list.count(x))
                    #
                    # max_index = np.array(number_ocurrences).argmax()
                    # max_value1 = max_value_list[max_index]
                    # moda_image_test[row, column, channel] = max_value1
                    # if(max_value!=max_value1):
                    #     print("OJO")
                    # print(max_value==max_value1)

        self.backgroundImage = moda_image



    # Using the last n where n is background_images_count, the values that are repeted the most of all the last n images
    # is used to calculate the background image. This background image is the image that will be use for the subtraction.
    # If the ringbuffer hasnt been created, is created.
    # Returns None in case is still buffering with images, not filled, the mask otherwise
    # In case the background is requiered to be reset, do it manually in the properties of the class.
    def moda_subtraction(self, frame, background_images_count):
        subtraction_mask = None
        if (self.ringbuffer_backgrounds == None):
            self.background_images_count = background_images_count
            self.ringbuffer_backgrounds = RingBuffer(self.background_images_count)

        if (self.ringbuffer_backgrounds.isFilled()):
            mylist = list(self.ringbuffer_backgrounds.get())
            data = np.asarray(mylist)
            #self.getMostRepeatedPixelValue(data)
            self.backgroundImage = utils.getMostRepeatedPixelValue(data)
            subtraction_mask = self.static_subtraction(frame)

        # Append the new frame
        self.ringbuffer_backgrounds.append(frame)
        return subtraction_mask

    # Explained
    # https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    # https://tttapa.github.io/Pages/Mathematics/Systems-and-Control-Theory/Digital-filters/Exponential%20Moving%20Average/Exponential-Moving-Average.html
    # Opencv implementation ->  http://answers.opencv.org/question/94520/background-subtraction-using-running-average-in-opencv/
    # Opencv implementation ->  https://docs.opencv.org/2.4/modules/imgproc/doc/motion_analysis_and_object_tracking.html#accumulateweighted
    def moving_average_exponential_subtraction(self, frame, alpha):
        # With this new background, subtract the background to the new frame
        subtraction_mask = self.static_subtraction(frame)
        # Update the background using the moving average
        accuWeight = cv2.accumulateWeighted(frame, self.backgroundImage.astype(float), alpha)
        self.backgroundImage = cv2.convertScaleAbs(accuWeight) #Use this to convert to uint8
        return subtraction_mask

    # Using the mask we choose which values to update. In this case we wont update the pixels that are foreground, this will stay background, and we will update those
    # that were background with
    def moving_average_exponential_subtraction_with_masking(self, frame, alpha):
        # With this new background, subtract the background to the new frame
        subtraction_mask = self.static_subtraction(frame)
        # We want to update only the parts that were background, the pixels that were foreground stays the same as in the previous backgroun image
        #mask = subtraction_mask
        mask = (1-subtraction_mask)
        mask = np.expand_dims(mask, axis=2) #No es necesario, hace el broadcasting solo luego
        mask = mask.astype(np.uint8) #Tiene que ser uint8 como la imagen de entrada
        # Update the background using the moving average
        accuWeight = cv2.accumulateWeighted(frame, self.backgroundImage.astype(float), alpha, mask)
        self.backgroundImage = cv2.convertScaleAbs(accuWeight) #Use this to convert to uint8
        return subtraction_mask
