import os
import sys
import argparse
import logging
from importlib import import_module
from NeuralNetwork.core.model import TFModel
from NeuralNetwork.core.utils import compute_scores


def run(params, warm_start, train, save, gen):
    # init model
    model = TFModel(**params['model'])

    # pre-process data
    scores = compute_scores(fixed_x=params['model']['fixed_x'], fixed_y=params['model']['fixed_y'], **params['data'])

    # load model
    if warm_start:
        model.load()
    else:
        logging.info("No pre-trained warm_start wanted for model='{}'. Starting with random model initialization"
                     .format(model.__class__.__name__))

    # train model
    if train:
        model.train(geometry_dir=params['data']['geometry_dir'], scores=scores)
    elif not warm_start:
        logging.warning("Model='{}' is not pre-trained and training is disabled - further usage is highly questionable"
                        .format(model.__class__.__name__))

    # save model
    if save:
        model.save()
    else:
        logging.info("No save wanted for model='{}'".format(model.__class__.__name__))

    # start genetic
    if gen:
        # ToDo genetic.run(model=model, **params['genetic'])
        
        pass


def main():
    """generic plumbing: resolve directories, files and paths, parse arguments and set ups logging"""
    # dirs, files amd paths
    _project_directory = os.path.realpath(sys.path[0])  # where python file is located
    _working_directory = os.path.realpath(os.getcwd())  # where user calls python file from
    _log_directory = _project_directory
    _log_file = 'logfile.log'
    _log_file_path = os.path.join(_log_directory, _log_file)
    _config_directory = _project_directory
    _config_file = 'hyperparams.py'
    _config_file_path = os.path.join(_config_directory, _config_file)

    # setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-nl', '--no-log',  dest='log', action='store_false',
                        help='deactivates logger (default activate)')
    parser.add_argument('-nt', '--no-train', dest='train', action='store_false',
                        help='deactivates training model (default activate)')
    parser.add_argument('-ns', '--no-save', dest='save', action='store_false',
                        help='deactivates saving model (default activate)')
    parser.add_argument('-ng', '--no-gen', dest='gen', action='store_false',
                        help='deactivates genetic algorithm (default activate)')
    parser.add_argument('-w', '--warmstart', dest='warmstart', action='store_true',
                        help='activates loading for pre-trained start')
    parser.set_defaults(log=True, train=True, save=True, gen=True, warmsart=False)
    parser.add_argument('-ll', '-loglevel', dest='loglevel', type=str, default='INFO',
                        choices=['CRITICAL', 'ERROR',  'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
                        help='depicts logging level')
    parser.add_argument('-lf', '-logfile', dest='logfile', type=str, default=_log_file_path,
                        help='destination of log file')
    parser.add_argument('-lfmt', '-logformat', dest='logformat', type=str,
                        default='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        help='defines logger message format')
    parser.add_argument('-ldfmt', '-logdateformat', dest='logdateformat', type=str, default='%m/%d/%Y %I:%M:%S %p',
                        help='defines logger timestamp format')
    parser.add_argument('-c', '-config',  dest='config', type=str, default=_config_file_path,
                        help='destination of config file')
    args = parser.parse_args()

    # resolve input directories
    _config_directory, _config_file = os.path.split(args.config) if not args.config.startswith('~') else \
        os.path.split(os.path.expanduser(args.config))
    _log_directory, _log_file = os.path.split(args.logfile) if not args.logfile.startswith('~') else \
        os.path.split(os.path.expanduser(args.logfile))
    _config_file_path = os.path.join(_config_directory, _config_file)
    _log_file_path = os.path.join(_log_directory, _log_file)
    assert os.path.exists(_config_directory), "config_directory='{}' for config_file='{}' does not exist".format(
        _config_directory, _config_file)
    assert _config_directory.startswith(_project_directory), "config_directory must be nested within " \
        "project_directory='{}' but found config_directory='{}' instead".format(_project_directory, _config_directory)
    assert os.path.exists(_log_directory), "log_directory='{}' for log_file='{}' does not exist".format(
        _log_directory, _log_file)
    assert os.path.isfile(_config_file_path), "config_file='{}' in config_directory='{}' does not exist or is not a " \
                                              "file".format(_config_file, _config_directory)

    # set up logger
    if args.log:
        logging.basicConfig(format=args.logformat, filename=args.logfile, level=args.loglevel,
                            datefmt=args.logdateformat)
    logging.info("successfully set up logging ")
    logging.debug("called {} with following args; {}".format(__file__, args))
    logging.debug("initialized with the following file/directory variables: config_directory='{}', config_file='{}', "
                  "config_file_path='{}', log_directory='{}', log_file='{}', log_file_path='{}' project_directory='{}',"
                  " working_directory='{}'".format(_config_directory, _config_file, _config_file_path, _log_directory,
                                                   _log_file, _log_file_path, _project_directory, _working_directory))

    # load config file
    _config_file_name, _config_file_type = _config_file.rsplit('.', 1) if '.' in _config_file else (_config_file, None)
    assert _config_file_type == 'py', "hyperparameters has to be a '.py' file but found '{}'".format(_config_file_type)
    _config_package = os.path.relpath(_config_directory, _project_directory).replace('/', '.') \
        if _config_directory != _project_directory else ''
    _config_module = _config_package + '.' + _config_file_name if _config_package != '' else _config_file_name
    params = import_module(_config_module).params
    logging.info("successfully loaded params")
    logging.debug("params={}".format(params))

    # start working
    run(params=params, warm_start=args.warmstart, train=args.train, save=args.save, gen=args.gen)

    # clean up, say fare well
    logging.info("{} terminated".format(__file__))


if __name__ == "__main__":
    main()
