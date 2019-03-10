from pedestrian.pedestrian import Pedestrian
#Inheritance
from abc import ABC, abstractmethod
import numpy as np
#Centroid
from sklearn.metrics.pairwise import euclidean_distances

class BaseTracker(ABC):
    def __init__(self):
        self.pedestrian_list = []
        #TODO: get from configuration
        self.pedestrian_has_exit_scene_max_count = 50 #El video va a 25 FPS por lo tanto consideramos que ha desaparecido
        # tras dos segundos sin verlo.
        self.__id_count = 0

    @abstractmethod
    def tracker_update(self, new_detections_bbox):
        '''
        This method updates the pedestrian_list. Recieves a new list of detections and matches the new detections with
        the previous pedestrian detected on the list, also adds new pedestrians and remove previous pedestrians.
        :param new_detections_bbox:
        :return: The updated list of pedestrians
        '''
        raise NotImplementedError

    def __get_next_id(self):
        '''
        Get the next id for a pedestrian. Each time a new pedestrian comes to scene a new and unique id is return.
        :return: The next available and unique id
        '''
        self.__id_count = self.__id_count + 1
        return self.__id_count

    def add_new_pedestrian(self, bbox, matching_parameters = None):
        '''
        Adds a new pedestrian to the pedestrian list
        :param bbox: The bbox where this new pedestrian was when detected
        :param matching_parameters: Parameters used to match the pedestrian and track it
        :return: Empty
        '''
        pedestrian = Pedestrian(self.__get_next_id(), bbox=bbox)
        #TODO add matching parameters
        self.pedestrian_list.append(pedestrian)

    def update_pedestrian(self, id, bbox, matching_parameters):
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
                pedestrian.updated = True
                pedestrian.remove_counter = 0

        return result

    def remove_pedestrian(self, id):
        '''
        Given an id the pedestrian with that id is remove from the list.
        :param id: The unique id given to the new pedestrian
        :return: True if the pedestrian was found and removed, False if there is no pedestrian in the list with that id.
        '''
        result = False
        for pedestrian in self.pedestrian_list:
            if (pedestrian.id == id):
                result = True
                # Comprobamos cuanto tiempo lleva el pedestrian sin matchear
                if (self.pedestrian_has_exit_scene_max_count == pedestrian.remove_counter):
                    self.pedestrian_list.remove(pedestrian)
                else:
                    pedestrian.remove_counter = pedestrian.remove_counter + 1

        return result

class CentroidTracker(BaseTracker):
    '''
    This is a tracker that uses centroid to match between different objects detected. Closest objetcs centroids
    are matched to the closest new centroids.
    '''
    def __init__(self):
        super(CentroidTracker, self).__init__()
        #TODO: get from configuration
        self.centroid_max_distance = 30     #Distancia max a la que considerar que podemos matcher centroides

    def tracker_update(self, new_detections_bbox):
        '''
        This method updates the pedestrian_list. Recieves a new list of detections and matches the new detections with
        the previous pedestrian detected on the list, also adds new pedestrians and remove previous pedestrians.
        :param new_detections_bbox:
        :return: The updated list of pedestrians
        '''
        #Check if the pedestrian list is empty
        if (len(self.pedestrian_list) == 0):
            for detection_bbox in new_detections_bbox:
                self.add_new_pedestrian(detection_bbox, None)
        else:
            self.__match_pedestrians(new_detections_bbox)

        return self.pedestrian_list

    def __match_pedestrians(self, new_detections_list):
        # TODO: mejorar esto, pueden darse ocasiones en las que no se matcheen algunos a pesar de haber suficientes
        #  detecciones no es lo normal pero existe el caso. Habria que buscar o bien solucionar el problema con aquellas
        #  asociaciones que minimizan la distancia en total. O bien ir asociando la nueva deteccion a la antifgua que
        #  mas cerca este, pero si se da la casualidad de que hay dos deteccinoes que comparten la distancia mas cercana
        #  a la misma deteccion, que pruebe con el siguiente mas cercano. (Habria que reordenar la matriz de alguna
        #  forma manteniendo por clave valor las dependencias u algo.
        '''
        Using centroids to keep track of the detected objects, associations between previous pedestrain and new
        detections are stablish. If new detections are made then new pedestrians are create, if previous id are
        unmatched they are keep for a while until they are completely removed.
        :param new_detections_list:
        :return: Empty
        '''
        # Otra forma de hacerlo https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
        # Con from scipy.spatial import distance as dist

        if (len(new_detections_list) == 0):
            for pedestrian in self.pedestrian_list:
                self.remove_pedestrian(pedestrian.id)
            return

        new_centroids = self.__get_centroids_list(new_detections_list)
        old_centroids = self.get_centroids_pedestrians(self.pedestrian_list)

        distance_matrix = np.array(euclidean_distances(new_centroids, old_centroids))
        #Cada fila corresponde a la distancia de el un new_centroid, y cada columna la distancia a cada uno de los
        # old_centroids.

        # Esto devolverá el orden en que tendra que ser recorrido el array de distancia, en funcion de la distancia
        # minima. Primero calculamos para cada fila (cada centroide nuevo) cual es la menor distancia a ese y luego
        # calculamos el orden. Argsort dice como tendrian que ordenarse, mientras que sort te los ordena.
        rows_ordered = distance_matrix.min(axis=1).argsort()

        # Mark all the pedestrian as not updated, to check later if some hasnt been updated
        for pedestrian in self.pedestrian_list:
            pedestrian.updated = False

        # For each new detection
        for row_number in rows_ordered:
            new_bbox = new_detections_list[row_number]
            pedestrian_index = distance_matrix[row_number].argmin() #Cogemos el indice del pedestrian que mas cercano esta

            # CASO: Mayor numero de detectiones nuevas que antiguas.
            # Check that the pedestrian hasnt been updated already in this iteration.
            if (self.pedestrian_list[pedestrian_index].updated):
                # Create a new pedestrian
                self.add_new_pedestrian(bbox=new_bbox)
                continue

            self.update_pedestrian(self.pedestrian_list[pedestrian_index].id, bbox=new_bbox, matching_parameters=None)

        # CASO: se podra dar el caso de haya menos detecciones que pedestrian antiguos (alguno salio de escena)
        pedestrian_not_updated_list = [pedestrian for pedestrian in self.pedestrian_list if not pedestrian.updated]

        for pedestrian_not_updated in pedestrian_not_updated_list:
            self.remove_pedestrian(pedestrian_not_updated.id)

        return


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

    def __get_centroids_list(self, bbox_list):
        '''
        Given a bbox list returns the centroids of those coordinates
        :param bbox_list: A list of bbox (top_left_point, bottom_rigth_point)
        :return: List with the centroids of each pedestrian
        '''
        centroids_list = []
        for bbox in bbox_list:
            x, y = self.__get_centroid(bbox)
            centroids_list.append([x, y])

        return centroids_list

    def get_centroids_pedestrians(self, pedestrian_list):
        '''
        Given a list of pedestrians, returns a list of centroids for the bbox of those pedestrians.
        :param pedestrian_list:
        :return: A list with centroids.
        '''
        centroids_list = []
        bbox_list = [pedestrian.bbox for pedestrian in pedestrian_list]
        centroids_list = self.__get_centroids_list(bbox_list)

        return centroids_list



