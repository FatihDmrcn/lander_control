import numpy as np


def pid_attitude(_force, _y_desired, _y_actual):
    error = _y_desired - _y_actual
    _ep = error - pid_attitude.e['t-1']
    _ei = error + pid_attitude.e['t-1']
    _ed = np.zeros(12)
    if np.any(pid_attitude.e['t-2'] != 0):
        _ed = error - 2 * pid_attitude.e['t-1'] + pid_attitude.e['t-2']
    print(_ep[4], _ei[4], _ed[4])
    _d_force = np.dot(pid_attitude.K['P'], _ep) + np.dot(pid_attitude.K['I'], _ei) + np.dot(pid_attitude.K['D'], _ed)
    f = _force + _d_force

    if np.all(pid_attitude.e['t-2'] == 0):
        f[0] = 0
    if f[0] < pid_attitude.min_thrust:
        f[0] = pid_attitude.min_thrust
    if f[0] > pid_attitude.max_thrust:
        f[0] = pid_attitude.max_thrust

    pid_attitude.e['t-2'] = pid_attitude.e['t-1']
    pid_attitude.e['t-1'] = error
    return f


KP_att = np.zeros((3, 12))
KI_att = np.zeros((3, 12))
KD_att = np.zeros((3, 12))

KP_att[0, 4] = -100
KI_att[0, 4] = -0.1
KD_att[0, 4] = -10000

KP_att[0, 10] = 0
KI_att[0, 10] = 0
KD_att[0, 10] = 0

pid_attitude.min_thrust = -50
pid_attitude.max_thrust = +50
pid_attitude.K = {'P': KP_att, 'I': KI_att, 'D': KD_att}
pid_attitude.e = {'t-1': np.zeros(12), 't-2': np.zeros(12)}
