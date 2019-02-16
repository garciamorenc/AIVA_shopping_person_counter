import cv2
import xml.etree.cElementTree as ET
import numpy as np


class Bbox:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


class Pedestrian:
    def __init__(self, _id, bbox):
        self.id = _id
        self.bbox = bbox
        self.previous_bbox = None
        self.hasEnter = False


# ****************************Configuration****************************

def choose_entrance(image):
    # This method receives an image and allows the user to put a line on the entrance of the shop. This method saves
    # the start point and end point of the line, and returns it
    bbox = Bbox(0, 0, 50, 0)
    return bbox

def save_entrance_configuration(entrance):
    # Save the line created by the user on a configuration file.
    # Returns true if the file is successfully created or updated
    root = ET.Element("root")
    doc = ET.SubElement(root, "configuration")

    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some value2"

    tree = ET.ElementTree(root)
    tree.write("filename.xml")
    return True

def configure_entrance():
    # Allows the user to configure the entrance of the commerce by choosing among an image from the video
    # Returns True if the file is succesfully created
    image = np.zeros((5, 3))
    entrance = choose_entrance(image)
    return save_entrance_configuration(entrance)

# ****************************Person counter****************************

def pedestrian_detector(image):
    # Returns a list with the bbox of the detected pedestrians
    bbox1 = Bbox(0, 0, 10, 10)
    bbox2 = Bbox(20, 20, 100, 100)
    detected_pedestrian = [bbox1, bbox2]
    return detected_pedestrian

def pedestrian_tracking(detected_pedestrian_previous, detected_pedestrians):
    # Check the similarity between the detection in the previous frame "detected_pedestrian_previous" and the new frame
    # "detected_pedestrian" and returns a list with the detected_pedestrians and their Ids.
    # If a new pedestrian is detected a new available Id is given to that pedestrian.
    # Updates the position of the "previous_bbox" of the pedestrian
    bbox = Bbox(0, 0, 10, 10)
    tracked_pedestrians = [Pedestrian(_id=i, bbox=bbox) for i in range(0, 6)]
    return tracked_pedestrians

def hasEnterTheShop(tracked_pedestrians):
    # Check if the tracked pedestrians have pass through the defined entrance
    # Using the previous_bbox and the bbox check if the entrance have been surpass
    for pedestrian in tracked_pedestrians:
        # Check if the entrance have been surpass
        pedestrian.hasEnter = True
    return tracked_pedestrians

