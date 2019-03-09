import cv2
import os
from argparse import ArgumentParser
import sys

if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-v", "--video", required=True, dest="video", type=str, help="path where the video is",
                        default=None)
    parser.add_argument("-sr", "--sample_rate", required=True, dest="sample_rate", type=int, help="Number of frames to sample",
                        default=None)
    parser.add_argument("-i", "--images_directory", required=True, dest="images_directory", type=str,
                        help="The path to save the images",
                        default=None)

    args = parser.parse_args()
    video_path = args.video
    sample_rate = args.sample_rate
    images_directory = args.images_directory

    if (not os.path.isfile(args.video)):
        print("There is no valid file in the argument video, please check that the path to the video file is valid")
        sys.exit(-1)
    else:
        video_path = os.path.normpath(video_path)
        # Video name used to create a folder to save the frames within it
        video_name, video_extension = os.path.splitext(os.path.basename(video_path))
        # The folder will be created within the same directory as the video
        video_dir = os.path.dirname(video_path)

    if(not os.path.isdir(images_directory)):
        print("Use a valid directory to save the images.")
        sys.exit(-1)

    # testing only, fix video path
    # video_path = os.path.normpath(r'/home/omar/workspaces/python/dataset/dataset_2/EnterExitCrossingPaths1front.mpg')

    # *********************READ VIDEO*********************
    cap = cv2.VideoCapture(video_path)

    if (not cap.isOpened()):
        print("The video couldnt be opened")
        sys.exit(-1)

    frame_counter = 0
    counter_sample = 0
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if (ret == False):
            print("End of video")
            break

        # Check if this frame should be sampled
        if (counter_sample == sample_rate):
            # Restart the count
            counter_sample = 1
        else:
            counter_sample = counter_sample + 1
            continue

        # Write the frame
        frame_name = video_name + "_" + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES))) + ".png"
        frame_path = os.path.join(images_directory, frame_name)
        cv2.imwrite(frame_path, frame)  # params=cv2.IMWRITE_PNG_COMPRESSION

        frame_counter = frame_counter + 1