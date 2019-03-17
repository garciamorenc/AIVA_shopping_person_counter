import cv2
import sys
import os
from configuration.app_configuration import AppConfiguration
from pedestrian.pedestrian_detector import PedestrianDetectorBackgroundSubtraction
from pedestrian.pedestrian_tracker import CentroidTracker
from utils.drawer import Drawer
from argparse import ArgumentParser


class PedestrianCounter:
    def count(self, video, debug):
        """
        It recognizes the total of people who pass in front of the store and do not get to enter
        :param video: image sequence to detect
        :param debug: True to see results; False doesn't
        :return: <int> total of people
        """
        total_pedestrians = 0
        conf = AppConfiguration()
        detector = PedestrianDetectorBackgroundSubtraction(conf.background, debug)
        tracker = CentroidTracker()

        # Reading video
        cap = cv2.VideoCapture(video)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Detection & tracking
                pedestrians_bbox = detector.detect_news(frame=frame)
                pedestrian_list = tracker.tracker_update(pedestrians_bbox)
                total_pedestrians += self.__get_valid(pedestrian_list, conf.shop_bbox)

                if debug:
                    green_color = (0, 255, 0)
                    Drawer.draw_pedestrians(frame, pedestrian_list, green_color)
                    Drawer.draw_shop_boundary(frame, conf.shop_bbox)
                    cv2.imshow("Test", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        return total_pedestrians

    @staticmethod
    def __get_valid(pedestrian_list, boundary):
        """
        Count the valid pedestrian from a tracking list
        :param pedestrian_list: pedestrian list that are tracked
        :param boundary: preconfigured shop boundary
        :return: total number of valid pedestrians who don't enter to shop
        """
        valid = 0
        for pedestrian in pedestrian_list:
            result = pedestrian.validate(boundary)

            if result:
                valid += 1

        return valid


if __name__ == "__main__":
    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--video", required=True, dest="video", type=str, help="path where the video is",
                        default=None)
    parser.add_argument("-t", "--test", dest="test", help="testing mode", action='store_true')

    args = parser.parse_args()
    video_path = args.video

    if not os.path.isfile(args.video):
        print("There is no valid file in the argument video, please check that the path to the video file is valid")
        sys.exit(-1)
    else:
        video_path = os.path.normpath(video_path)

    counter = PedestrianCounter()
    total = counter.count(video_path, args.test)
    print('Total of people who did not enter the store: ' + str(total))
