import numpy as np
from scipy.spatial.transform import Rotation
from .pid_thrust import pid_thrust
from .pid_attitude import pid_attitude


def lim_angle(_angle):
    if _angle <= lim_angle.min:
        return lim_angle.min
    if _angle >= lim_angle.max:
        return lim_angle.max
    if lim_angle.min < _angle < lim_angle.max:
        return _angle


lim_angle.min = -.25 * np.pi
lim_angle.max = +.25 * np.pi


def lim_thrust(_thrust):
    if _thrust <= lim_thrust.min:
        return lim_thrust.min
    if _thrust >= lim_thrust.max:
        return lim_thrust.max
    if lim_thrust.min < _thrust < lim_thrust.max:
        return _thrust


lim_thrust.min = 0
lim_thrust.max = 1000


def pid_controller(_y_desired, _y_actual):
    _d_alpha, _d_beta, _d_thrust = 0, 0, 0
    # event for belly flop
    # event for last approach (const. speed)
    if _y_actual[2] > 1000:
        _d_alpha, _d_beta, _d_thrust = pid_attitude(_y_desired, _y_actual)
    if _y_actual[2] <= 1000:
        _d_alpha, _d_beta, _d_thrust = pid_thrust(_y_desired, _y_actual)

    pid_controller.alpha += _d_alpha
    pid_controller.beta += _d_beta
    pid_controller.thrust += _d_thrust

    pid_controller.alpha = lim_angle(pid_controller.alpha)
    pid_controller.beta = lim_angle(pid_controller.beta)
    pid_controller.thrust = lim_thrust(pid_controller.thrust)

    _rotation = Rotation.from_euler('YX', [pid_controller.beta, pid_controller.alpha]).as_matrix()

    return np.dot(_rotation, np.array([0, 0, pid_controller.thrust]))


pid_attitude.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}
pid_controller.thrust = 0.
pid_controller.alpha = 0.
pid_controller.beta = 0.
