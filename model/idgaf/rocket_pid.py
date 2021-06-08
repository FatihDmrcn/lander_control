import numpy as np


def pid_thrust(_force, _y_desired, _y_actual):
    error = _y_desired - _y_actual
    _ep = error - pid_thrust.e['t-1']
    _ei = error + pid_thrust.e['t-1']
    _ed = error - 2 * pid_thrust.e['t-1'] + pid_thrust.e['t-2']
    _d_force = np.dot(pid_thrust.K['P'], _ep) + np.dot(pid_thrust.K['I'], _ei) + np.dot(pid_thrust.K['D'], _ed)
    f = _force + _d_force

    if np.all(pid_thrust.e['t-2'] == 0):
        f[2] = 0
    if f[2] < 0:
        f[2] = 0
    if f[2] > 1000:
        f[2] = 1000

    pid_thrust.e['t-2'] = pid_thrust.e['t-1']
    pid_thrust.e['t-1'] = error
    return f


KP = np.zeros((3, 12))
KD = np.zeros((3, 12))
KI = np.zeros((3, 12))

KP[2, 2] = 150
KI[2, 2] = 0.1
KD[2, 2] = 3000

KP[2, 8] = 100
KI[2, 8] = .0
KD[2, 8] = 15

pid_thrust.K = {'P': KP, 'I': KI, 'D': KD}
pid_thrust.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}
