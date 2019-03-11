import numpy as np
import cv2
import sys
import os
from configuration.app_configuration import AppConfiguration
from pedestrian.pedestrian_detector import PedestrianDetectorSSD, PedestrianDetectorBackgroundSubstraction
from pedestrian.tracker import CentroidTracker
from utils.drawer import draw_rectangles, draw_pedestrians
from utils.annotations_voc_writer import create_annotation_xml
from argparse import ArgumentParser


# CON ESTO DEL BACKGROUND SUBTRACTION, SE PUEDE USAR PARA EXTRAER EL GROUNDTRUTH PARA ENTRENAR A UNA RED
#  NEURONAL. PODEMOS PARA CADA FRAME MOSTRAR EL BBOX (COMO HASTA AHORA) Y EN FUNCION DE SI SE PULSA LA TECLA "Y"
#  o la tecla "N", podemos considerar ese frame bueno o no. Si es bueno, usamos esos bbox para crear el formato
#  del groundtruth (en funcion de la red que vayamos a entrenar) podriamos guardarlo en formato VOC y entrenar
#  la misma red que usamos en Reconocimiento de Patrones, la cual usaba VOC (aunque lo parseaba previamente). La
#  mayoria de frames diria que el 60% engloban con bastante precision a la persona asi que sería buenos datos
#  para entrenar la red, y luego se pueden usar las detecciones de la red para añadirlo al entrenamiento de
#  forma que acabemos sobreentrenando la red para todos los videos. Consiguiendo un grountruth semiautomatizado
#  y tardando poquisimo en crear el grountruth.


def main(video, groundtruth_path):
    """
    It recognizes the total of people who pass in front of the store and do not get to enter
    :param video: image sequence to detect
    :return: <int> total of people
    """
    conf = AppConfiguration()

    video_name, extension = os.path.splitext(os.path.basename(video))

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

    frame_counter = 1

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check the video has reach the end
        # if (cap.get(cv2.CAP_PROP_POS_FRAMES) == total_frames):
        #     print("Reach end of the video")
        #     break

        if (ret == False):
            print("End of the video reach")
            break

        # To keep a copy of the original frame (will be used as grountruth)
        orig_frame = frame.copy()

        # Detection
        pedestrians_bbox = detector.detect_news(frame=frame)

        # Check video to see detections
        green_color = (0, 255, 0)
        draw_rectangles(frame, pedestrians_bbox, green_color)
        cv2.imshow("TEST", frame)

        key = cv2.waitKey(0) & 0xFF
        if (key == ord('y')):
            file_basepath = os.path.join(groundtruth_path, video_name + "__" + str(frame_counter))
            image_original_path = file_basepath + ".png"
            image_detections_path = file_basepath + "_detections.png"

            cv2.imwrite(image_original_path, orig_frame)
            cv2.imwrite(image_detections_path, frame)
            create_annotation_xml(image_original_path, frame.shape[0], frame.shape[1], pedestrians_bbox)

        frame_counter = frame_counter + 1


if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--video", required=True, dest="video", type=str, help="path where the video is",
                        default=None)
    parser.add_argument("-gt", "--groundtruth_path", required=True, dest="groundtruth_path", type=str,
                        help="dir where the images and grountruth will be saved", default=None)

    args = parser.parse_args()
    video_path = args.video
    groundtruth_path = args.groundtruth_path

    if (not os.path.isfile(args.video)):
        print("There is no valid file in the argument video, please check that the path to the video file is valid")
        sys.exit(-1)
    else:
        video_path = os.path.normpath(video_path)

    if (not os.path.isdir(args.groundtruth_path)):
        print("There is no valid file in the argument video, please check that the path to the video file is valid")
        sys.exit(-1)
    else:
        groundtruth_path = os.path.normpath(args.groundtruth_path)

    main(video_path, groundtruth_path)

