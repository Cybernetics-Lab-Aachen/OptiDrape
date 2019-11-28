import numpy as np
import tensorflow as tf
from copy import deepcopy
from tqdm import tqdm
from abc import abstractmethod


class AbstractEvolAlg(object):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def _check_for_sanity(self):
        """Diese Funktion ist dafür da einen Sanitycheck für die Initialdaten zu machen"""
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def _create_start_population(self):
        """Hier wird die Startpopulation erstellt"""
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def _mutate(self, population=None):
        """Hier wird ein inidividuum mutiert"""
        # Falls man das alte Individuum behalten will, muss man eine deppcopy machen
        # _mutated_individuum = deepcopy(individuum)
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def _calculate_score(self, population=None):
        """Hier wird der score eines Individuums berechnet"""
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def _selection(self, number_of_selected_individuals, population=None):
        """Hier werden die Individuen selektiert. Es wird eine Liste von Individuen zurückgegeben"""
        # Beispiel für die Selektierung
        # scores = [self._calculate_score(seq) for seq in list_of_individuums]
        # arguments = np.argsort(scores)[-number_of_selected_individuums:]
        # selected_individuums = [list_of_individuums[arg] for arg in arguments]
        # return selected_individuums[::-1]
        raise NotImplementedError("Not Implemented")

    @abstractmethod
    def run_algorithm(self):
        """Hier fügen sich alle Funktionen zum genetischen Algorithmus zusammen"""
        # Hier tqdm verwenden: https://pypi.org/project/tqdm/
        raise NotImplementedError("Not Implemented")


