import numpy as np
import cv2
import sys
import os
from configuration.app_configuration import AppConfiguration
from pedestrian.pedestrian_detector import PedestrianDetectorSSD, PedestrianDetectorBackgroundSubstraction
from utils.drawer import draw_rectangles
from argparse import ArgumentParser


def count(video):
    """
    It recognizes the total of people who pass in front of the store and do not get to enter
    :param video: image sequence to detect
    :return: <int> total of people
    """
    total = 0
    conf = AppConfiguration()

    # detector = PedestrianDetectorSSD()
    # detector.load(conf, os.path.normpath(r"resources/MobileNetSSD_deploy.prototxt"),
    #               os.path.normpath(r"resources/MobileNetSSD_deploy.caffemodel"))

    detector = PedestrianDetectorBackgroundSubstraction()
    detector.load(conf, os.path.normpath(r"resources/background_image.png"))

    #READ VIDEO
    cap = cv2.VideoCapture(video)

    if (not cap.isOpened()):
        print("The video couldnt be opened")
        sys.exit(-1)

    frame_counter = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check the video has reach the end
        # if (cap.get(cv2.CAP_PROP_POS_FRAMES) == total_frames):
        #     print("Reach end of the video")
        #     break

        if (ret == False):
            print("Bad frame")
            break

        # Detection
        pedestrians_bbox = detector.detect_news(frame=frame)
        #pedestrians_bbox, weights = detector.detect_news_HOG(frame=frame)

        # Check video to see detections
        green_color = (0, 255, 0)
        draw_rectangles(frame, pedestrians_bbox, green_color)
        cv2.imshow("TEST", frame)
        cv2.waitKey(5)

        frame_counter = frame_counter + 1


    #
    # pedestrians = detector.detect_news(np.zeros((10, 10)))
    #
    # for item in pedestrians:
    #     # Keep tracking if the pedestrian has not entered the store or left the scene
    #     if (not item.is_valid) and (not item.hasEnter):
    #         item.tracking(conf.shop_bbox)
    #         if item.is_valid:  # Left the scene and has not entered the store
    #             total += 1

    return total


if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--video", required=True, dest="video", type=str, help="path where the video is",
                        default=None)

    args = parser.parse_args()
    video_path = args.video



    if (not os.path.isfile(args.video)):
        print("There is no valid file in the argument video, please check that the path to the video file is valid")
        sys.exit(-1)
    else:
        video_path = os.path.normpath(video_path)

    # testing only, fix video path
    #video_path = os.path.normpath(r'/home/omar/workspaces/python/dataset/dataset_2/EnterExitCrossingPaths1front.mpg')
    total = count(video_path)
    print('Total of people who did not enter the store: ' + str(total))
