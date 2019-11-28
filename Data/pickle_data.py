import os, sys
import pickle
import h5py, tqdm, itertools
import numpy as np


# These are for training
def load_pyramid_hdf(path, pickle_for_training=False):
    """
    :param path: path of the hdf5 from matlab
    :param pickle_for_training: when pickle for training, only shear angle in the simulation result will be pickled
    :return:
    """
    _data = h5py.File(path, 'r')

    _max_height = 500
    _min_height = 100
    _max_width = 1000
    _min_width = 200
    _max_angle = 88
    _min_angle = 0

    _data_piece = _data['ZT']

    _dim_height = _data_piece.shape[2]
    _dim_width = _data_piece.shape[1]
    _dim_angle = _data_piece.shape[0]

    _step_height = int((_max_height - _min_height) / (_dim_height - 1))
    _step_width = int((_max_width - _min_width) / (_dim_width - 1))
    _step_angle = int((_max_angle - _min_angle) / (_dim_angle - 1))

    if not (_max_height - _min_height) % _dim_height or \
            not (_max_width - _min_width) % _dim_width or \
            not (_max_angle - _min_angle) % _dim_angle:
        print("Warning: Size of Geometry dosenot fit the min/max.")

    _geo_list = list()
    _angle_list = list()

    print(_dim_angle, _dim_height, _dim_width)
    with tqdm.tqdm(total=_dim_angle* _dim_height * _dim_width,
                   desc="Extracting Geometry Pyramidenstumpf ...") as pbar:

        for i_angle, i_height, i_width in itertools.product(range(_dim_angle), range(_dim_height),
                                                            range(_dim_width)):
            _ori_z_matrix = _data[_data['ZG'][i_angle, i_width, i_height]]
            _z_matrix = _data[_data_piece[i_angle, i_width, i_height]]

            if not pickle_for_training:
                _x_vector = _data[_data['XT'][i_angle, i_width, i_height]]
                _y_vector = _data[_data['YT'][i_angle, i_width, i_height]]

            _shear_angle_matrix = _data[_data['Scherwinkel'][i_angle, i_width, i_height]]

            if _z_matrix.size > 2:  # if the size of the geometry exists, then we could extract
                _sim_result = []

                if not pickle_for_training:
                    for i, j in itertools.product(range(_z_matrix.shape[0]), range(_z_matrix.shape[1])):  #print([_x_vector[0, i], _y_vector[j, 0], _z_matrix[i, j], _shear_angle_matrix[i, j]])
                        if type(_shear_angle_matrix[i, j]) == tuple:
                            _sim_result.append([_x_vector[0, i], _y_vector[j, 0], _z_matrix[i, j], _shear_angle_matrix[i, j][0]])

                        else:
                            _sim_result.append([_x_vector[0, i], _y_vector[j, 0], _z_matrix[i, j], _shear_angle_matrix[i, j]])

                _this_geo_name = 'H' + str(_min_height + i_height * _step_height) + \
                                 'W' + str(_min_width + i_width * _step_width) + \
                                 'A' + str(_min_angle + i_angle * _step_angle)

                with open(os.path.dirname(path) + '/Pyramide/geometry/' + _this_geo_name + '.pickle', 'wb') as handle:
                    pickle.dump(np.asarray(_ori_z_matrix, dtype=np.float32), handle, protocol=pickle.HIGHEST_PROTOCOL)

                try:
                    with open(os.path.dirname(path) + '/Pyramide/label/' + _this_geo_name + '.pickle', 'wb') as handle:
                        if pickle_for_training:
                            pickle.dump(np.asarray(_shear_angle_matrix, dtype=np.float32), handle,
                                        protocol=pickle.HIGHEST_PROTOCOL)
                        else:
                            pickle.dump(np.asarray(_sim_result, dtype=np.float32), handle,
                                        protocol=pickle.HIGHEST_PROTOCOL)

                    #_angle_list.append(np.asarray(_shear_angle_matrix, dtype=np.float32))
                except:
                    print("Error in numpy")
                    print(_sim_result)
                    print(i_angle, i_height, i_width)
                    print(np.asarray(_shear_angle_matrix))

                    _angle_array = np.asarray(_shear_angle_matrix)
                    _angle_matrix = _angle_array.tolist()

                    if pickle_for_training:
                        for i, j in itertools.product(range(_angle_array.shape[0]), range(_angle_array.shape[1])):
                            _angle_matrix[i][j] = _angle_matrix[i][j][0]

                        with open(os.path.dirname(path) + '/Pyramide/label/' + _this_geo_name + '_label.pickle',
                                  'wb') as handle:
                            pickle.dump(np.asarray(_angle_matrix, dtype=np.float32), handle,
                                        protocol=pickle.HIGHEST_PROTOCOL)
                    else:
                        for this_list in _sim_result:
                            this_list[3] = this_list[3][0]

                        with open(os.path.dirname(path) + '/Pyramide/label/' + _this_geo_name + '_label.pickle',
                                  'wb') as handle:
                            pickle.dump(np.asarray(_sim_result, dtype=np.float32), handle,
                                        protocol=pickle.HIGHEST_PROTOCOL)

            pbar.update()


def load_halbkugel_hdf(path, pickle_for_training=False):

    _data = h5py.File(path, 'r')

    _min_height = 100
    _max_height = 2000
    _min_radius = 100
    _max_radius = 2000

    _data_piece = _data['ZT']

    _dim_height = _data_piece[0, :].size
    _dim_radius = _data_piece[:, 0].size

    _step_height = int((_max_height - _min_height) / (_dim_height - 1))
    _step_radius = int((_max_radius - _min_radius) / (_dim_radius - 1))

    if not (_max_height - _min_height) % _dim_height or \
            not (_max_radius - _min_radius) % _dim_radius:
        print("Warning: Size of Geometry dosenot fit the min/max.")

    _geometry_dict = dict()
    _geo_list = list()
    _angle_list = list()
    with tqdm.tqdm(total=_data['ZT'].size,
                   desc="Extracting Geometry Halbkugel ...") as pbar:

        for i_radius, i_height in itertools.product(range(_dim_radius), range(_dim_height)):
            _ori_z_matrix = _data[_data['ZG'][i_radius, i_height]]
            _z_matrix = _data[_data_piece[i_radius, i_height]]
            if not pickle_for_training:
                _x_vector = _data[_data['XT'][i_radius, i_height]]
                _y_vector = _data[_data['YT'][i_radius, i_height]]
            _shear_angle_matrix = _data[_data['Scherwinkel'][i_radius, i_height]]

            if _shear_angle_matrix.size > 2:
                _sim_result = []
                try:
                    for i, j in itertools.product(range(_z_matrix.shape[0]), range(_z_matrix.shape[1])):
                        _sim_result.append([_x_vector[0, i], _y_vector[j, 0], _z_matrix[i, j], _shear_angle_matrix[i, j]])
                        #print(i_radius, i_height, i, j)
                #        print([_x_vector[0, i], _y_vector[j, 0], _z_matrix[i, j], _shear_angle_matrix[i, j]])
                        #_sim_result.append(_shear_angle_matrix[i, j])
                except:
                    print("Index Error")
                    print(i_radius, i_height)
                    print(_x_vector.size, _y_vector.size, _shear_angle_matrix.size)
                    print(_x_vector.shape, _y_vector.shape, _shear_angle_matrix.shape)

                _this_geo_name = 'R' + str(_min_radius + i_radius * _step_radius) + \
                                 'H' + str(_min_height + i_height * _step_height)

                #_geometry_dict.update({_this_geo_name: {'origin': np.asarray(_ori_z_matrix, dtype=np.float16),
                #                                        'result': np.asarray(_sim_result, dtype=np.float16)}})
                #_geo_list.append(np.asarray(_ori_z_matrix, dtype=np.float32))
                #_angle_list.append(np.asarray(_shear_angle_matrix, dtype=np.float32))

                #with open(os.path.dirname(path) + '/Halbkugel/geometry/' + _this_geo_name + '.pickle', 'wb') as handle:
                #    pickle.dump(np.asarray(_ori_z_matrix, dtype=np.float32), handle, protocol=pickle.HIGHEST_PROTOCOL)

                if pickle_for_training:
                    with open(os.path.dirname(path) + '/Halbkugel/label/' + _this_geo_name + '.pickle', 'wb') as handle:
                        pickle.dump(np.asarray(_shear_angle_matrix, dtype=np.float32), handle, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    with open(os.path.dirname(path) + '/Halbkugel/label/' + _this_geo_name + '.pickle', 'wb') as handle:
                        pickle.dump(np.asarray(_sim_result, dtype=np.float32), handle, protocol=pickle.HIGHEST_PROTOCOL)

            pbar.update()


# General
def load_pickle_data(path):
    if os.path.isfile(path):
        return pickle.load(open(path, 'rb'))
    else:
        return None


def update_pickled_data(path, data_dict, without_check=False):
    _data = data_dict
    # if the file exist, then we update it!
    if not without_check and os.path.isfile(path):
        _data = pickle.load(open(path, 'rb'))
        _data.update(data_dict)

    pickle.dump(_data, open(path, 'wb'))


def pickle_data(path, data_dict):
    pass



if __name__ == '__main__':
    path = "/home/optidrape/Desktop/DrapeSimulation/Pyramide.mat"

    load_pyramid_hdf(path)






































