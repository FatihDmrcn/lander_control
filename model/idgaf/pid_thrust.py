import numpy as np


def pid_thrust(_force, _y_desired, _y_actual):
    error = _y_desired - _y_actual
    _ep = error - pid_thrust.e['t-1']
    _ei = error + pid_thrust.e['t-1']
    _ed = error - 2 * pid_thrust.e['t-1'] + pid_thrust.e['t-2']
    _d_force = np.dot(pid_thrust.K['P'], _ep) + np.dot(pid_thrust.K['I'], _ei) + np.dot(pid_thrust.K['D'], _ed)
    f = _force + _d_force

    if np.all(pid_thrust.e['t-2'] == 0):
        f = np.zeros(3)
    if f[2] < pid_thrust.min_thrust:
        f[2] = 0
    if f[2] > pid_thrust.max_thrust:
        f[2] = pid_thrust.max_thrust
    if f[0] < pid_thrust.min_thrust_X:
        f[0] = pid_thrust.min_thrust_X
    if f[0] > pid_thrust.max_thrust_X:
        f[0] = pid_thrust.max_thrust_X

    pid_thrust.e['t-2'] = pid_thrust.e['t-1']
    pid_thrust.e['t-1'] = error
    return f


KP_thr = np.zeros((3, 12))
KI_thr = np.zeros((3, 12))
KD_thr = np.zeros((3, 12))

KP_thr[2, 2] = 150
KI_thr[2, 2] = 0.1
KD_thr[2, 2] = 3000

KP_thr[2, 8] = 100
KI_thr[2, 8] = .0
KD_thr[2, 8] = 15

KP_thr[0, 4] = -100
KI_thr[0, 4] = -0.1
KD_thr[0, 4] = -10000

KP_thr[0, 10] = 0
KI_thr[0, 10] = 0
KD_thr[0, 10] = 0

pid_thrust.min_thrust = 0
pid_thrust.max_thrust = 1000
pid_thrust.min_thrust_X = -50
pid_thrust.max_thrust_X = +50
pid_thrust.K = {'P': KP_thr, 'I': KI_thr, 'D': KD_thr}
pid_thrust.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}


