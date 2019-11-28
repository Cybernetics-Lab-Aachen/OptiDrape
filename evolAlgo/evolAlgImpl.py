
from evolAlgo.evolAlg import AbstractEvolAlg
from evolAlgo.evolIndividual import EvolConfig, DrapeIndividual
import threading
#import openmesh
import copy, sys
from enum import Enum
from numba import jit


# todo: this class is a "manager" of evol, as the evol is started, multiple threads will be created as the number of selected textiles
# todo: a start, pause and stop algorithm


class EvolAlgState(Enum):
    IDLE = 0,
    RUNNING = 1,
    PAUSED = 2,
    STOPPED = 3,
    FINISHED = 4,
    FINISHED_SATISFIED = 5



class EvolAlgManager(object):
    pass




class EvolAlgImpl(object):
    def __init__(self, input_geometry, textile, crit_sAngle, fitness_function, constraints, config):
        """
        :param input_geometry: input geometry with formate DrapeTriMesh
        :param textile: extile name
        :param crit_sAngle: critical shear angle,
        :param fitness_function: fitness function to the score function
        :param constraints: constraints for mutation
        :param config: configuration for evol
        """
        super(EvolAlgImpl, self).__init__()

        # config
        self._config = config
        # self._config = EvolConfig()

        self._textile_name = textile
        self._crit_shear_angle = crit_sAngle

        # global variables
        self._state = EvolAlgState.IDLE
        self._input_geometry = input_geometry
        self._fitness_function = fitness_function
        self._population = []
        self._last_population = []
        self._constraints = constraints
        self._termination_satisfied = False

        # and we also need to initialize the NN for deploy !

        # processing variables
        self._processing_thread = threading.Thread(name=self._textile_name,
                                                   target=self.run_algorithm)
        self._mutex = threading.RLock()
        self._pause_event = threading.Event()

        self._current_threads = dict()
        self._current_iteration = 0

   # def start(self):
        # create
    #    pass

    @property
    def state(self):
        return self._state

    def start(self):

        self._create_start_population()
        pass


    def pause(self):
        with self._mutex:
            if self._state is EvolAlgState.RUNNING:
                self._state = EvolAlgState.PAUSED
            else:
                pass

    def continue_algl(self):
        with self._mutex:
            if self._state is EvolAlgState.PAUSED:
                self._state = EvolAlgState.RUNNING
                self._pause_event.set()

    def stop(self):
        with self._mutex:
            self._state = EvolAlgState.STOPPED

    def run_algorithm(self):
        for i in range(self._config.max_iteration):
            with self._mutex:
            # check whether to pause
                if self._state is EvolAlgState.PAUSED:
                    self._pause_event.clear()
                    self._pause_event.wait(sys.maxsize)
                elif self._state is EvolAlgState.STOPPED or self._termination_satisfied:
                    break

                # mutation
                for individual in self._population:
                    individual.mutate_once()

                # selection
                self._selection()

                self._current_iteration = i
                # TODO: Here begins the iteration
                # TODO: | -> selection -> mutate (score will be calculated after mutation) -> check_termination -> |

        if self._state is EvolAlgState.RUNNING:
            self._state = EvolAlgState.FINISHED


    def _create_start_population(self):
        # To create the start population, we could feed the input geometry to the fitness function
        # to get a first basis for mutation
        for i in range(self._config.population_size):
            _individual = DrapeIndividual(geometry=self._input_geometry.deepcopy(name=self._input_geometry.name + '_' + self._textile_name + '_{}'.format(i)),
                                          score_function=self._fitness_function,
                                          config=self._config,
                                          constraints=self._constraints)

            _individual.mutate_once()
            self._population.append(_individual)

        if not self._check_for_sanity():
            raise ArithmeticError

    def _check_for_sanity(self):
        return True

    def _selection(self, number_of_selected_individuals):
        # todo:
        for individual in self._population:
            pass

    def update_evol_param(self, config=None, constraints=None):
        # by default, the configs will be updated before running the algorithm so we do not need to lock the mutex
        # ToDo: 1. thrown info that the configs were updated, 2. check for sanity

        with self._mutex:
            if config:
                self._config = config
                for individual in self._population:
                    pass
            if constraints:
                self._constraints = constraints

    def get_status(self):
        with self._mutex:
            return self._current_iteration / self._config.max_iteration, self._current_iteration, self._config.max_iteration

    def get_result(self):
        # if
        with self._mutex:
            if self._current_iteration < self._config.max_iteration:
                return False, self._current_iteration / self._config.max_iteration

        return True, self._population
















