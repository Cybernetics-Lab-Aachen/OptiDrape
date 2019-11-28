import sys
import numpy as np
import logging, coloredlogs


def get_logger():
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    return logger


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def calc_shear_angle(X, Y, rx, ry, rz, q=0.013, unit='deg'):
    if unit not in ['deg', 'rad']:
        get_logger().warning("Calculate shear angle: unit %s invalid, deg or rad." % str(unit))
        unit = 'deg'
    try:
        _shear_angle_x = np.arctan((q * np.power(X, 2) * (Y - 2 * ry)) / (Y * rz * rx))
        _shear_angle_y = np.arctan((q * np.power(Y, 2) * (X - 2 * rx)) / (X * rz * ry))
        if unit == 'deg':
            _shear_angle_x = np.rad2deg(_shear_angle_x)
            _shear_angle_y = np.rad2deg(_shear_angle_y)
        return _shear_angle_x, _shear_angle_y
    except:
        get_logger().error("Calcuate shear angle failed, please check!")
        return None, None


def calc_q(X, Y, rx, ry, rz, shear_angle, unit='deg'):

    if unit not in ['deg', 'rad']:
        get_logger().warning("Calculate q from shear angle: unit %s invalid, deg or rad." % str(unit))
        unit = 'deg'
    try:
        if unit == 'deg':
            shear_angle = np.deg2rad(shear_angle)
        qx = np.tan(shear_angle) / (pow(X, 2) * (Y - 2 * ry) / (Y * rx * rz))
        qy = np.tan(shear_angle) / (pow(Y, 2) * (X - 2 * rx) / (X * ry * rz))
        return qx, qy
    except:
        get_logger().error("Calcuate shear angle failed, please check!")
        return None, None


def unit_vector(v):
    return v / np.linalg.norm(v)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.rad2deg(np.arccos(np.clip(np.dot(v1_u, v2_u), -1., 1.)))
