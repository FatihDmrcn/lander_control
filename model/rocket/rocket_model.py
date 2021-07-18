from scipy.spatial.transform import Rotation
import numpy as np
# SELAM VE DUA LIPA
# FIFTY-ONE-ERGS


def rocket_eq(t, y, _forces, _mass, _length, _inertia):
    matrix_rot = (1 / _mass) * Rotation.from_euler('ZYX', [y[5], y[4], y[3]]).as_matrix()
    matrix_trq = - (_length / (2 * _inertia)) * np.array(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    _B = np.vstack((np.zeros((6, 3)), matrix_rot, matrix_trq))

    dy_dt = rocket_eq.g + np.dot(rocket_eq.A, y) + np.dot(_B, _forces)
    return dy_dt


A = np.zeros((12, 12))
A[:6, 6:] = np.identity(6)
rocket_eq.A = A
rocket_eq.g = np.array((0., 0., 0., 0., 0., 0., 0., 0., -9.81, 0., 0., 0.))
