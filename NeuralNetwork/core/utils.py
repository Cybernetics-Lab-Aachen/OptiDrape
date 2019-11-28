import numpy as np
import pickle as pk
import os
import logging
from random import shuffle
from tqdm import tqdm
from .calculate_score import ScoreCalculator
from glob import glob


def load_geometry(file_path, fixed_x, fixed_y):
    geometry_file_path = file_path
    _geometry_file = open(geometry_file_path, 'rb')
    _geometry_pk = pk.load(_geometry_file)
    assert isinstance(_geometry_pk, np.ndarray), "pickled file='{}' was expected to be of type='{}' but found " \
        "type='{}' instead".format(geometry_file_path, np.ndarray, type(_geometry_pk))
    assert len(_geometry_pk.shape) == 2, "pickled file='{}' was expected to be of rank='{}' but found rank='{}' " \
        "instead".format(geometry_file_path, 2, len(_geometry_pk.shape))
    assert fixed_x >= _geometry_pk.shape[0], "pickled file's='{}' x-dim='{}' must not exceed fixed_x='{}'".format(
        geometry_file_path, _geometry_pk.shape[0], fixed_x)
    assert fixed_y >= _geometry_pk.shape[1], "pickled file's='{}' y-dim='{}' must not exceed fixed_y='{}'".format(
        geometry_file_path, _geometry_pk.shape[1], fixed_y)
    if (fixed_x, fixed_y) != _geometry_pk.shape:
        _padded_geometry = np.zeros(shape=(fixed_x, fixed_y), dtype=np.float32)
        _padded_geometry[:_geometry_pk.shape[0], :_geometry_pk.shape[1]] = _geometry_pk
    else:
        _padded_geometry = _geometry_pk
    return _padded_geometry


def batch_gen(iterable, batch_size):
    shuffle(iterable)
    size = len(iterable)
    cursor = 0
    while cursor < size:
        yield iterable[cursor:min(cursor+batch_size, size)]
        cursor += batch_size


def compute_scores(geometry_dir, label_dir, fixed_x, fixed_y, threshold, weight_max_angle, scale=1.0,
                   input_regexp='*.pickle', store_output=True, output_dir_prefix='pre-comp-',
                   output_file='scores.pickle'):
    # asserts
    assert os.path.exists(geometry_dir), "geometry_dir='{}' does not exist".format(geometry_dir)
    assert os.path.exists(label_dir), "label_dir='{}' does not exist".format(label_dir)
    geometry_file_paths = glob(os.path.join(geometry_dir, input_regexp))
    label_file_paths = glob(os.path.join(label_dir, input_regexp))
    output_label_path, output_label_name = os.path.split(label_dir)
    output_label_dir = os.path.join(output_label_path, output_dir_prefix + output_label_name)
    scores_output_path = os.path.join(output_label_dir, output_file)
    assert len(geometry_file_paths) > 0, "can't locate '{}'-files in geometry_dir='{}'".format(input_regexp,
                                                                                                     geometry_dir)
    assert len(label_file_paths) > 0, "can't locate '{}'-files in label_dir='{}'".format(input_regexp,
                                                                                               label_dir)
    assert len(label_file_paths) == len(geometry_file_paths), "number of geometries='{}' must equal number of labels="\
        "'{}'".format(len(geometry_file_paths), len(label_file_paths))

    # check if output already exists
    if os.path.exists(scores_output_path):
        logging.info("output_file='{}' already exists - delete it, if you want to re-compute it or change output_file "
                     "accordingly".format(scores_output_path))
        _file = open(scores_output_path, 'rb')
        return pk.load(_file)
    # create output folder
    if store_output and not os.path.exists(output_label_dir):
        os.mkdir(output_label_dir)
        logging.info("created new directory: {}".format(output_label_dir))

    # instantiate score calculator and output container
    sc = ScoreCalculator(fixed_x_size=fixed_x, fixed_y_size=fixed_y, threshold=threshold,
                         weight_max_angle=weight_max_angle, scale=scale)
    scored_labels = dict()
    logging.info("starting to pre-calculate scores")

    # load geometry labels
    for geometry_file_path in tqdm(geometry_file_paths, unit='geometry', desc='ScoreCalculation'):
        # load label
        _file_name, _file_type = os.path.split(geometry_file_path)[-1].rsplit('.', 1)
        label_file_path = os.path.join(label_dir, _file_name + '_label.' + _file_type)
        _label_file = open(label_file_path, 'rb')
        _label_pk = pk.load(_label_file)
        assert len(_label_pk.shape) == 2, "pickled file='{}' was expected to be of rank='{}' but found rank='{}' " \
            "instead".format(label_file_path, 2, len(_label_pk.shape))
        score = sc.calculate_score(input_data=_label_pk.reshape(-1))
        scored_labels[_file_name] = score

    # store if wanted
    if store_output:
        _store_file = open(scores_output_path, 'wb')
        pk.dump(scored_labels, _store_file)
        logging.info("created output-file='{}'".format(scores_output_path))
    logging.info("finished pre-calculate scores")
    return scored_labels
