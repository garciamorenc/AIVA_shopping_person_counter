import pascal_voc_writer
import os

def create_annotation_xml(image_path, width, height, bbox_list):
    '''
    Creates the xml annotation in VOC format for a given image.
    Credits to: https://pypi.org/project/pascal-voc-writer/
    :param image_path: The path where the image is or will be store
    :param width: The width of the image
    :param height: The height of the image
    :param bbox_list: The list of person detected as bbox ((xmin,ymin), (xmax,ymax)) 
    :return: Empty
    '''
    writer = pascal_voc_writer.Writer(image_path, width, height)
    for bbox in bbox_list:
        writer.addObject('person', xmin=bbox[0][0], ymin=bbox[0][1], xmax=bbox[1][0], ymax=bbox[1][1])

    filename, extension = os.path.splitext(os.path.basename(image_path))
    directory = os.path.dirname(image_path)
    annotation_filepath = os.path.join(directory, filename + ".xml")
    writer.save(annotation_filepath)