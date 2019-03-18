from pedestrian.pedestrian import Pedestrian
# Inheritance
from abc import ABC, abstractmethod
import numpy as np
# Centroid
from sklearn.metrics.pairwise import euclidean_distances


class BaseTracker(ABC):
    """
    Abstract class used as a base for trackers.
    """
    def __init__(self):
        self.pedestrian_list = []
        # This value is based on the FPS of our video. The pedestrian is missing for 2 seconds (25FPS*2=50)
        self.__pedestrian_has_exit_scene_max_count = 50
        self.__id_count = 0

    @abstractmethod
    def tracker_update(self, new_detections_bbox):
        """
        This method updates the pedestrian_list. Receives a new list of detections and matches the new detections with
        the previous pedestrian detected on the list, also adds new pedestrians and remove previous pedestrians.
        :param new_detections_bbox, a list of Bbox with the new detections made.
        :return: The updated list of pedestrians
        """
        raise NotImplementedError

    def __get_next_id(self):
        """
        Get the next id for a pedestrian. Each time a new pedestrian comes to scene a new and unique id is return.
        :return: The next available and unique id
        """
        self.__id_count = self.__id_count + 1
        return self.__id_count

    def add_new_pedestrian(self, bbox):
        """
        Adds a new pedestrian to the pedestrian list
        :param bbox: The bbox where this new pedestrian was when detected
        :return: Empty
        """
        pedestrian = Pedestrian(self.__get_next_id(), bbox=bbox)
        self.pedestrian_list.append(pedestrian)

    def update_pedestrian(self, _id, bbox):
        """
        Given an id the pedestrian with that id updates it bbox and matching parameters
        :param _id: The unique id given to the new pedestrian
        :param bbox: The bbox where this pedestrian was last seen
        :return: True if the pedestrian was found and updated, False if there is no pedestrian in the list with that id
        """
        result = False
        for pedestrian in self.pedestrian_list:
            if pedestrian.id == _id:
                result = True
                pedestrian.previous_bbox = pedestrian.bbox
                pedestrian.bbox = bbox
                pedestrian.updated = True
                pedestrian.remove_counter = 0

        return result

    def remove_pedestrian(self, _id):
        """
        Given an id the pedestrian with that id is remove from the list. The pedestrian arent removed immediately, they
        are removed once the remove_counter member equals the __pedestrian_has_exit_scene_max_count member.
        :param _id: The unique id given to the new pedestrian
        :return: True if the pedestrian was found, False if there is no pedestrian in the list with that id.
        """
        result = False
        for pedestrian in self.pedestrian_list:
            if pedestrian.id == _id:
                result = True
                # Check that the pedestrian has been missing for the maximum time allowed.
                if self.__pedestrian_has_exit_scene_max_count == pedestrian.remove_counter:
                    self.pedestrian_list.remove(pedestrian)
                else:
                    pedestrian.remove_counter = pedestrian.remove_counter + 1

        return result


class CentroidTracker(BaseTracker):
    """
    This is a tracker that uses centroid to match between different objects detected. Closest objects centroids
    are matched to the closest new centroids.
    """
    def __init__(self):
        super(CentroidTracker, self).__init__()
        # Distance use as the maximum distance that centroids can be matched.
        self.centroid_max_distance = 50

    def tracker_update(self, new_detections_bbox):
        """
        This method updates the pedestrian_list. Receives a new list of detections and matches the new detections with
        the previous pedestrian detected on the list, also adds new pedestrians and remove previous pedestrians.
        :param new_detections_bbox, a list of Bbox with the new detections made.
        :return: The updated list of pedestrians.
        """
        # Check if the pedestrian list is empty
        if len(self.pedestrian_list) == 0:
            for detection_bbox in new_detections_bbox:
                self.add_new_pedestrian(detection_bbox)
        else:
            self.__match_pedestrians(new_detections_bbox)

        return self.pedestrian_list

    def __match_pedestrians(self, new_detections_list):
        """
        Using centroids to keep track of the detected objects, associations between previous pedestrians and new
        detections are establish. If new detections are made then new pedestrians are create, if previous id are
        unmatched they are keep for a while until they are completely removed.
        :param new_detections_list
        :return: Empty
        """
        if len(new_detections_list) == 0:
            for pedestrian in self.pedestrian_list:
                self.remove_pedestrian(pedestrian.id)
            return

        new_centroids = self.__get_centroids_list(new_detections_list)
        old_centroids = self.get_centroids_pedestrians(self.pedestrian_list)

        distance_matrix = np.array(euclidean_distances(new_centroids, old_centroids))

        # This represents the order that the new_detections_list has to be iterate. The order is based on the minimun
        # distance of the new_detections to the closest Pedestrian.
        rows_ordered = distance_matrix.min(axis=1).argsort()

        # Mark all the pedestrian as not updated, to check later if some hasnt been updated
        for pedestrian in self.pedestrian_list:
            pedestrian.updated = False

        # For each new detection
        for row_number in rows_ordered:
            new_bbox = new_detections_list[row_number]
            # The index of the closest Pedestrian
            pedestrian_index = distance_matrix[row_number].argmin()

            # Check that the pedestrian hasnt been updated already in this iteration.
            if self.pedestrian_list[pedestrian_index].updated:
                # Create a new pedestrian
                self.add_new_pedestrian(bbox=new_bbox)
                continue

            if distance_matrix[row_number].min() >= self.centroid_max_distance:
                break

            self.update_pedestrian(self.pedestrian_list[pedestrian_index].id, bbox=new_bbox)

        # Check if there are pedestrians not updated
        pedestrian_not_updated_list = [pedestrian for pedestrian in self.pedestrian_list if not pedestrian.updated]

        for pedestrian_not_updated in pedestrian_not_updated_list:
            self.remove_pedestrian(pedestrian_not_updated.id)

        return

    @staticmethod
    def __get_centroid(bbox):
        """
        Given a bbox with (top_left_point, bottom_rigth_point) get the centroid of that bbox
        :param bbox: Bbox
        :return: The centroid as a tuple representing a point x and y values.
        """
        x = (bbox.x0 + bbox.x1) / 2
        y = (bbox.y0 + bbox.y1) / 2
        centroid = (x, y)
        return centroid

    def __get_centroids_list(self, bbox_list):
        """
        Given a bbox list returns the centroids of those coordinates
        :param bbox_list: A list of bbox (top_left_point, bottom_rigth_point)
        :return: List with the centroids of each pedestrian
        """
        centroids_list = []
        for bbox in bbox_list:
            x, y = self.__get_centroid(bbox)
            centroids_list.append([x, y])

        return centroids_list

    def get_centroids_pedestrians(self, pedestrian_list):
        """
        Given a list of pedestrians, returns a list of centroids for the bbox of those pedestrians.
        :param pedestrian_list:
        :return: List with the centroids of each pedestrian
        """
        bbox_list = [pedestrian.bbox for pedestrian in pedestrian_list]
        centroids_list = self.__get_centroids_list(bbox_list)

        return centroids_list



