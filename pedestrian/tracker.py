from pedestrian.pedestrian import Pedestrian
#Inheritance
from abc import ABC, abstractmethod
#Centroid
from sklearn.metrics.pairwise import euclidean_distances

class BaseTracker(ABC):
    def __init__(self):
        self.pedestrian_list = []
        #TODO: get from configuration
        self.pedestrian_has_exit_scene_max_count = 50 #El video va a 25 FPS por lo tanto consideramos que ha desaparecido
        # tras dos segundos sin verlo.
        self.__id_count = 0

    def tracker_update(self, new_detections_bbox):
        '''
        This methos updates the pedestrian_list. Recieves a new list of detections and matches the new detections with
        the previous pedestrian detected on the list, also adds new pedestrians and remove previous pedestrians.
        :param new_detections_bbox:
        :return: The updated list of pedestrians
        '''
        #Check if the pedestrian list is empty
        if (len(self.pedestrian_list) == 0):
            for detection_bbox in new_detections_bbox:
                self.__add_new_pedestrian(self.__get_next_id(), detection_bbox, None)
        else:
            self.pedestrian_list = self.__match_pedestrians()

        return self.pedestrian_list

    def __get_next_id(self):
        '''
        Get the next id for a pedestrian. Each time a new pedestrian comes to scene a new and unique id is return.
        :return: The next available and unique id
        '''
        self.__id_count = self.__id_count + 1
        return self.__id_count

    def __add_new_pedestrian(self, id, bbox, matching_parameters):
        '''
        Adds a new pedestrian to the pedestrian list
        :param id: The unique id given to the new pedestrian
        :param bbox: The bbox where this new pedestrian was when detected
        :param matching_parameters: Parameters used to match the pedestrian and track it
        :return: Empty
        '''
        pedestrian = Pedestrian(id, bbox=bbox)
        #TODO add matching parameters
        self.pedestrian_list.append(pedestrian)

    def __update_pedestrian(self, id, bbox, matching_parameters):
        '''
        Given an id the pedestrian with that id updates it bbox and matching parameters
        :param id: The unique id given to the new pedestrian
        :param bbox: The bbox where this pedestrian was last seen
        :param matching_parameters: Parameters used to match the pedestrian and track it
        :return: True if the pedestrian was found and updated, False if there is no pedestrian in the list with that id
        '''
        #search pedestrian
        result = False
        for pedestrian in self.pedestrian_list:
            if (pedestrian.id == id):
                result = True
                pedestrian.bbox = bbox
                pedestrian.matching_parameters = matching_parameters

        return result

    def __remove_pedestrian(self, id):
        '''
        Given an id the pedestrian with that id is remove from the list.
        :param id: The unique id given to the new pedestrian
        :return: True if the pedestrian was found and removed, False if there is no pedestrian in the list with that id.
        '''
        result = False
        for pedestrian in self.pedestrian_list:
            if (pedestrian.id == id):
                result = True
                self.pedestrian_list.remove(pedestrian)

        return result

    @abstractmethod
    def __match_pedestrians(self, new_detections_list):
        '''
        Match the existing pedestrians
        :param new_detections_list:
        :return:
        '''
        raise NotImplementedError

class CentroidTracker(BaseTracker):
    '''
    This is a tracker that uses centroid to match between different objects detected. Closest objetcs centroids
    are matched to the closest new centroids.
    '''
    def __init__(self):
        BaseTracker.__init__()
        #TODO: get from configuration
        self.centroid_max_distance = 20     #Distancia max a la que considerar que podemos matcher centroides

    def __match_pedestrians(self, new_detections_list):
        '''
        Using centroids to keep track of the detected objects, associations between previous pedestrain and new
        detections are stablish. If new detections are made then new pedestrians are create, if previous id are
        unmatched they are keep for a while until they are completely removed.
        :param new_detections_list:
        :return:
        '''
        # Otra forma de hacerlo https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
        # Con from scipy.spatial import distance as dist

        for detection in new_detections_list:
            # Asignamos cada deteccion nueva a pedestrian mas cercano previo.
            centroids_list = self.__get_centroids_list(self.pedestrian_list)
            distance_list = euclidean_distances(centroids_list, detection)
            # TODO 2: Para asignar, ordeno por distancia


    def __get_centroid(self, bbox):
        '''
        Given a bbox with (top_left_point, bottom_rigth_point) get the centroid of that bbox
        :param bbox:
        :return:
        '''
        x = (bbox[0][0] + bbox[1][0]) / 2
        y = (bbox[0][1] + bbox[1][1]) / 2
        centroid = (x, y)
        return centroid

    def __get_centroids_list(self, pedestrian_list):
        '''
        Given a pedestrian list returns the centroids of those pedestrians
        :param pedestrian_list:
        :return: List with the centroids of each pedestrian
        '''
        centroids_list = []
        for pedestrian in pedestrian_list:
            x, y = self.__get_centroid(pedestrian.bbox)
            centroids_list.append([x, y])

        return centroids_list






