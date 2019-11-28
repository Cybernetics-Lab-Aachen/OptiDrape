from importlib import import_module

from .core.model import TFModel
from NeuralNetwork.core.calculate_score import ScoreCalculator


class DrapeFitnessFunction:
    def __init__(self, model_path, param_path, logger=None):
        if not model_path and not param_path:
            if logger:
                logger.set_text("Score Function: no valid path given, model_path='{}', param_path={}".format(model_path,
                                                                                                             param_path))
            print("Score Function: no valid path given, model_path='{}', param_path={}".format(model_path, param_path))
        self._logger = logger
        self.reset(model_path=model_path,
                   param_path=param_path)

    def score(self, geo_projection, critical_shearangle):
        #_shearangle_prediction = self._model.inference(geometry=geo_projection)
        return self._model.inference(geometry=geo_projection)

    def reset(self, model_path, param_path):
        self._model_path = model_path
        self._param_path = param_path
        params = import_module(param_path).params  # try catch?

        self._model = TFModel(**params['model'])
        self._model.load()

        if self._logger:
            self._logger.set_text("Score Function: Loaded TF Model successfully")






