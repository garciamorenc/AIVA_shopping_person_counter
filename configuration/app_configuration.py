import xml.etree.cElementTree as ET
from utils.bounding_box import Bbox


class AppConfiguration:
    """
    Class that contains the configuration of the application. The configuration is loaded from an xml file.
    """
    def __init__(self, bbox=None, background=None):
        self.__path = './config.xml'
        self.shop_bbox = None
        self.background = None

        if bbox and background:
            self.set_configuration(bbox.x0, bbox.y0, bbox.x1, bbox.y1, background)
        else:
            self.load()

    def save(self):
        """
        Save the current configuration into a XML file
        :return Boolean about save process execution
        """
        root = ET.Element("root")
        doc = ET.SubElement(root, "configuration")

        ET.SubElement(doc, "x0", name="x0").text = str(self.shop_bbox.x0)
        ET.SubElement(doc, "y0", name="y0").text = str(self.shop_bbox.y0)
        ET.SubElement(doc, "x1", name="x1").text = str(self.shop_bbox.x1)
        ET.SubElement(doc, "y1", name="y1").text = str(self.shop_bbox.y1)
        ET.SubElement(doc, "background", name="background").text = str(self.background)

        tree = ET.ElementTree(root)
        tree.write(self.__path)
        return True

    def load(self):
        """
        Load the configuration from file self.__path
        """
        tree = ET.parse(self.__path)
        root = tree.getroot()

        x0 = root[0][0].text.strip()
        y0 = root[0][1].text.strip()
        x1 = root[0][2].text.strip()
        y1 = root[0][3].text.strip()
        self.shop_bbox = Bbox(x0, y0, x1, y1)
        self.background = root[0][4].text.strip()

    def set_configuration(self, x0, y0, x1, y1, background):
        """
        Set a new application configuration and save it
        :param x0: new x0 coord
        :param y0: new y0 coord
        :param x1: new x1 coord
        :param y1: new y1 coord
        :param background: new background using to background subtraction
        """
        self.shop_bbox = Bbox(x0, y0, x1, y1)
        self.background = background
        self.save()
