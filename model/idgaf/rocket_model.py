from scipy.spatial.transform import Rotation as R
import numpy as np


def rocket_eq(t, y, _forces, _mass, _length, _inertia):
    A = np.zeros((12, 12))
    A[:6, 6:] = np.identity(6)

    matrix_rot = (1 / _mass) * R.from_euler('ZYX', [y[5], y[4], y[3]]).as_matrix()
    matrix_trq = - (_length / (2 * _inertia)) * np.array(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    B = np.vstack((np.zeros((6, 3)), matrix_rot, matrix_trq))

    dy_dt = np.array((0., 0., 0., 0., 0., 0., 0., 0., -9.81, 0., 0., 0.)) + np.dot(A, y) + np.dot(B, _forces)
    return dy_dt
