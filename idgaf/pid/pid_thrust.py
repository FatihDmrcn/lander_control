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


def pid_thrust(_y_desired, _y_actual):
    error = _y_desired - _y_actual
    _ep = error - pid_thrust.e['t-1']
    _ei = error + pid_thrust.e['t-1']
    _ed = error - 2 * pid_thrust.e['t-1'] + pid_thrust.e['t-2']

    _delta = np.dot(pid_thrust.KP, _ep) + np.dot(pid_thrust.KI, _ei) + np.dot(pid_thrust.KD, _ed)
    _d_alpha = lim_d_angle(_delta[0])
    _d_beta = lim_d_angle(_delta[1])
    _d_thrust = lim_d_thrust(_delta[2])

    if np.all(pid_thrust.e['t-2'] == 0):
        _d_alpha, _d_beta, _d_thrust = 0., 0., 0.

    pid_thrust.e['t-2'] = pid_thrust.e['t-1']
    pid_thrust.e['t-1'] = error
    return _d_alpha, _d_beta, _d_thrust


pid_thrust.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}
pid_thrust.KP = np.zeros((3, 12))
pid_thrust.KI = np.zeros((3, 12))
pid_thrust.KD = np.zeros((3, 12))

# Control Beta
pid_thrust.KP[1][4] = -5
pid_thrust.KI[1][4] = -0.008
pid_thrust.KD[1][4] = -1000
pid_thrust.KP[2][4] = 0
pid_thrust.KI[2][4] = 0.010
pid_thrust.KD[2][4] = 1000
pid_thrust.KP[1][10] = 0
pid_thrust.KI[1][10] = 0
pid_thrust.KD[1][10] = 0


# Control thrust
pid_thrust.KP[2][2] = 150
pid_thrust.KI[2][2] = 0.1
pid_thrust.KD[2][2] = 3000
pid_thrust.KP[2][8] = 100
pid_thrust.KI[2][8] = 0.
pid_thrust.KD[2][8] = 15

