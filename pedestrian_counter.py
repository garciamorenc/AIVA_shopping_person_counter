import numpy as np
from configuration.app_configuration import AppConfiguration
from pedestrian.pedestrian_detector import PedestrianDetector
from argparse import ArgumentParser


def count(video):
    """
    It recognizes the total of people who pass in front of the store and do not get to enter
    :param video: image sequence to detect
    :return: <int> total of people
    """
    total = 0
    conf = AppConfiguration()
    detector = PedestrianDetector()

    # TODO loop video
    pedestrians = detector.detect_news(np.zeros((10, 10)))

    for item in pedestrians:
        # Keep tracking if the pedestrian has not entered the store or left the scene
        if (not item.is_valid) and (not item.hasEnter):
            item.tracking(conf.shop_bbox)
            if item.is_valid:  # Left the scene and has not entered the store
                total += 1

    return total


if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--video", dest="video", type=str, default=None)

    args = parser.parse_args()

    total = count(args.video)
    print('Total of people who did not enter the store: ' + str(total))
