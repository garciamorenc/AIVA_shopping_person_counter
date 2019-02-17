import xml.etree.cElementTree as ET
from utils.bounding_box import Bbox


class AppConfiguration:

    def __init__(self, path):
        self.path = path
        self.shop_bbox = None
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

        tree = ET.ElementTree(root)
        tree.write(self.path)
        return True

    def load(self):
        """
        Load the configuration from file self.path
        """
        x0 = 10
        y0 = 50
        x1 = 10
        y1 = 50
        self.shop_bbox = Bbox(x0, y0, x1, y1)

    def set_configuration(self, x0, y0, x1, y1):
        """
        Set a new application configuration and save it
        :param x0: new x0 coord
        :param y0: new y0 coord
        :param x1: new x1 coord
        :param y1: new y1 coord
        """
        self.shop_bbox = Bbox(x0, y0, x1, y1)
        self.save()

