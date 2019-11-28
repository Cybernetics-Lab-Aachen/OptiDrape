
import numpy as np
import openmesh, copy
from NeuralNetwork.deploy import DrapeFitnessFunction
from collections import deque
from gui.ui.ui_optimization_manager import MutationPolicy, VertexSelectionPolicy, NeighbourPolicy
from .constrains import EvolAlgoConstraints
from Data.custom_deque import ResizableDeque
from Data.drape_utils import *
from itertools import product
from numba import jit, njit

class EvolConfig:
    def __init__(self):
        self.default_config()

    def default_config(self, from_file=False):
        # reset all parameters in default
        self.population_size = 10
        self.mutation_prob = 0.
        self.convergence_threshold = 80  # the score or 80% of the best score
        self.max_iteration = 1000

        self.min_vertex_to_mutate = 5
        self.max_vertex_to_mutate = 30

        self.min_vertex_neighbours = 3
        self.max_vertex_neighbours = 29

        self.min_neighbourhood_groups = 1

        self.is_mutation_adaptive = True  # it means that the current mutation parameter will be affected with the last mutation

        self.crit_shear_angle_offset = 0.

        self.vertex_selection_policy = VertexSelectionPolicy.MAX_CURVATURE_NEIGHBORS

        self.mutation_policy = MutationPolicy.REDUCE_CURVATURE

        self.neighbour_policy = NeighbourPolicy.CONTINUOUS

        self.sl_size_geo = 5  # number of geometry solutions of each selected textile

        self.num_config_history = 2

    def update_config(self,
                      size_of_population=None,
                      iteration=None,
                      min_vertex=None,
                      max_vertex=None,
                      adaptive_mutation=None,
                      convergence_threshold=None,
                      sangle_offset=None,
                      vertex_selection_policy=None,
                      mutation_policy=None,
                      num_config_history=None,
                      neighbour_policy = None):
        # pack configuration as a dict

        ## todo: value check

        if neighbour_policy:
            self.neighbour_policy = neighbour_policy

        if num_config_history:
            self.num_config_history = num_config_history

        if size_of_population:
            self.population_size = size_of_population

        if iteration:
            self.max_iteration = iteration

        if min_vertex:
            self.min_vertex_to_mutate = min_vertex

        if max_vertex:
            self.max_vertex_to_mutate = max_vertex

        if adaptive_mutation:
            self.is_mutation_adaptive = adaptive_mutation

        if convergence_threshold:
            self.convergence_threshold = convergence_threshold

        if sangle_offset:
            self.crit_shear_angle_offset = sangle_offset

        if vertex_selection_policy:
            self.vertex_selection_policy = vertex_selection_policy

        if mutation_policy:
            self.mutation_policy = mutation_policy

    def show_evol_config(self, browser=None):
        _str_to_print = ["- Size Population: {}".format(self.population_size),
                         "- Iteration: {}".format(self.max_iteration),
                         "- Min. Vertex: {}".format(self.min_vertex_to_mutate),
                         "- Max. Vertex: {}".format(self.max_vertex_to_mutate),
                         "- Adaptive Mutation: {}".format(self.is_mutation_adaptive),
                         "- Terminate Score: {}".format(self.convergence_threshold),
                         "- sAngle Offset: {}".format(self.crit_shear_angle_offset),
                         "- Vertex Selection Policy:",
                         "  {}".format(self.vertex_selection_policy.name),
                         "- Mutation Policy:",
                         "  {}".format(self.mutation_policy.name)]

        if browser:
            browser.append("")
            browser.append("Current Evol Config:")
            for s in _str_to_print:
                browser.append(s)
            browser.append("")
        else:
            print("Current Evol Config:")
            for s in _str_to_print:
                print(s)


class DrapeIndividual:
    # it could be nice when we pack all related info in a object, because the bauteilgeometrie is kind of mesh, but
    # the data we are process, are no more mesh, but point cloud. The output of the tool should be a mesh, then we need
    # to keep the reduced geometry in its object
    def __init__(self, geometry, score_function, constraints, config=None):
        self._geometry = geometry  # this should be a Trimesh object of openmesh lib, a kind of friend class
        self._mutation_basis = np.matrix([])
        self._score = 0.
        self._current_iteration = 0
        self._score_function = score_function

        self._constraints = copy.deepcopy(constraints)

        self._vertex2mutate = self._constraints['node_expected']
        self._p_vertex2mutate = [1 / len(self._vertex2mutate) for _ in range(len(self._vertex2mutate))] # mutate
        if config:
            self._evol_config = copy.deepcopy(config)
        else:
            self._evol_config = EvolConfig()

        self._evol_config_history = deque(maxlen=self._evol_config.num_config_history)
        self._mutated_vertex_history = deque(maxlen=self._evol_config.num_config_history)
        self._score_history = deque(maxlen=self._evol_config.num_config_history)

    def _calc_score(self):
        # todo:
        _geometry_matrix = self._geometry.create_xy_normalized_projection()
        self._score = self._score_function(_geometry_matrix)

    def mutate_once(self):
        # todo: 1: finish the mutation functionality
        # todo: 2: after each mutation, generate new x_y_projection
        # todo: 3: after got new x_y_projection, deploy the fitness function to get score

        if self._evol_config.is_mutation_adaptive:
            # update the config parameter according to last run
            pass

        if self._evol_config.mutation_policy is MutationPolicy.REDUCE_CURVATURE:
            pass

        elif self._evol_config.mutation_policy is MutationPolicy.REDUCE_Z_COORDINATE:
            pass

        elif self._evol_config.mutation_policy is MutationPolicy.RANDOMLY:
            pass

        self._evol_config_history.append(self._evol_config)

    def __get_neighbours(self, center_node=None):

        if not center_node:
            center_node = 0

    @njit()
    def _select_vertex_to_mutate(self):
        # todo: this function must be tested
        _node_number = np.random.randint(low=self._evol_config.min_vertex_to_mutate,
                                         high=self._evol_config.max_vertex_to_mutate)

        _node_2_mutate = None

        if self._evol_config.vertex_selection_policy is VertexSelectionPolicy.RANDOMLY:
            return [np.random.choice(self._vertex2mutate, _node_number, p=self._p_vertex2mutate)]

        elif self._evol_config.vertex_selection_policy is VertexSelectionPolicy.RANDOMLY_NEIGHBORS:
            # to get the neighbors, first we select a node and located it
            _node_still_2_select = copy.deepcopy(_node_number)

            _min_neighbour_grps = copy.deepcopy(self._evol_config.min_neighbourhood_groups)
            _vertex_map = self._geometry.xy_matrix
            _created_neighbour_grps = 0

            print("Selecting vertex and its neighbours")

            _random_node = np.random.choice(self._vertex2mutate, 1, p=self._p_vertex2mutate)[0]

            _random_node_index = tuple([c[0] for c in np.where(_vertex_map == _random_node)])

            _number_of_neighbour = np.random.randint(low=self._evol_config.min_vertex_neighbours,
                                                     high=self._evol_config.max_vertex_neighbours)
            
            if _node_still_2_select - _number_of_neighbour <= 0:
                _number_of_neighbour = _node_still_2_select

            _node_2_mutate = [_random_node]

            while len(_node_2_mutate) < _number_of_neighbour + 1:
                if self._evol_config.neighbour_policy is NeighbourPolicy.RANDOMLY:
                    _this_neighbour_feasible = False
                    while not _this_neighbour_feasible:
                        neighbour_row = np.random.randint(1, _number_of_neighbour)
                        neighbour_col = np.random.randint(1, _number_of_neighbour)
                        neighbour = _vertex_map[_random_node_index[0] + neighbour_row,
                                                _random_node_index[1] + neighbour_col]
                        if neighbour not in _node_2_mutate:
                            _this_neighbour_feasible = True
                            _node_2_mutate.append(neighbour)
                elif self._evol_config.neighbour_policy is NeighbourPolicy.CONTINUOUS:
                    _neighbour_range = int(_number_of_neighbour / 4)
                    for neighbour_row, neighbour_col in product(range(-_neighbour_range, _neighbour_range), range(-_neighbour_range, _neighbour_range)):
                        try:
                            neighbour = _vertex_map[_random_node_index[0] + neighbour_row,
                                                    _random_node_index[1] + neighbour_col]
                            if neighbour not in _node_2_mutate:
                                _node_2_mutate.append(neighbour)
                            if len(_node_2_mutate) >= _number_of_neighbour:
                                break
                        except:
                            pass
                else:
                    _node_2_mutate.append(None)
                    break

            return _node_2_mutate

        elif self._evol_config.vertex_selection_policy is VertexSelectionPolicy.MAX_COORDINATE:


            pass

        elif self._evol_config.vertex_selection_policy is VertexSelectionPolicy.MAX_COORDINATE_NEIGHBORS:
            pass

        elif self._evol_config.vertex_selection_policy is VertexSelectionPolicy.MAX_CURVATURE:
            pass

        elif self._evol_config.vertex_selection_policy is VertexSelectionPolicy.MAX_CURVATURE_NEIGHBORS:
            pass

        else:
            return None

    @property
    def geometry(self):
        return self._geometry

    @property
    def score(self):
        return self._score





















































