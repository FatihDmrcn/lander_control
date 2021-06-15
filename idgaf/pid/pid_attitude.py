import numpy as np


def lim_d_angle(_angle):
    if _angle <= -lim_d_angle.limit:
        return -lim_d_angle.limit
    if _angle >= lim_d_angle.limit:
        return lim_d_angle.limit
    if -lim_d_angle.limit < _angle < lim_d_angle.limit:
        return _angle


lim_d_angle.limit = .0125 * np.pi


def lim_d_thrust(_thrust):
    if _thrust <= -lim_d_thrust.limit:
        return -lim_d_thrust.limit
    if _thrust >= lim_d_thrust.limit:
        return lim_d_thrust.limit
    if -lim_d_thrust.limit < _thrust < lim_d_thrust.limit:
        return _thrust


lim_d_thrust.limit = 10


def pid_attitude(_y_desired, _y_actual):
    error = _y_desired - _y_actual
    _ep = error - pid_attitude.e['t-1']
    _ei = error + pid_attitude.e['t-1']
    _ed = error - 2 * pid_attitude.e['t-1'] + pid_attitude.e['t-2']

    _delta = np.dot(pid_attitude.KP, _ep) + np.dot(pid_attitude.KI, _ei) + np.dot(pid_attitude.KD, _ed)
    _d_alpha = lim_d_angle(_delta[0])
    _d_beta = lim_d_angle(_delta[1])
    _d_thrust = lim_d_thrust(_delta[2])

    if np.all(pid_attitude.e['t-2'] == 0):
        _d_alpha, _d_beta, _d_thrust = 0., 0., 0.

    pid_attitude.e['t-2'] = pid_attitude.e['t-1']
    pid_attitude.e['t-1'] = error
    return _d_alpha, _d_beta, _d_thrust


pid_attitude.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}
pid_attitude.KP = np.zeros((3, 12))
pid_attitude.KI = np.zeros((3, 12))
pid_attitude.KD = np.zeros((3, 12))

# Control Beta
pid_attitude.KP[1][4] = -5
pid_attitude.KI[1][4] = -0.008
pid_attitude.KD[1][4] = -1000
pid_attitude.KP[2][4] = 0
pid_attitude.KI[2][4] = 0.010
pid_attitude.KD[2][4] = 1000
pid_attitude.KP[1][10] = 0
pid_attitude.KI[1][10] = 0
pid_attitude.KD[1][10] = 0
