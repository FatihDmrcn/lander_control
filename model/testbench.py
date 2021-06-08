from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np


def rocket_eq(t, y, _forces, _mass, _length, _inertia):
    A = np.zeros((12, 12))
    A[:6, 6:] = np.identity(6)

    matrix_rot = (1 / _mass) * R.from_euler('ZYX', [y[5], y[4], y[3]]).as_matrix()
    matrix_trq = - (_length / (2 * _inertia)) * np.array(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    B = np.vstack((np.zeros((6, 3)), matrix_rot, matrix_trq))

    dy_dt = np.array((0., 0., 0., 0., 0., 0., 0., 0., -9.81, 0., 0., 0.)) + np.dot(A, y) + np.dot(B, _forces)
    return dy_dt


KP = np.zeros((3, 12))
KD = np.zeros((3, 12))
KI = np.zeros((3, 12))

KP[2, 2] = 100
KI[2, 2] = .0
KD[2, 2] = 3000

KP[2, 8] = 150
KI[2, 8] = 0
KD[2, 8] = 100


def pid_control(_y_desired, _y_actual):
    error = _y_desired - _y_actual

    _ep = error - pid_control.e['t-1']
    _ei = error + pid_control.e['t-1']
    _ed = error - 2 * pid_control.e['t-1'] + pid_control.e['t-2']

    pid_control.e['t-2'] = pid_control.e['t-1']
    pid_control.e['t-1'] = error

    return np.dot(pid_control.K['P'], _ep) + np.dot(pid_control.K['I'], _ei) + np.dot(pid_control.K['D'], _ed)


pid_control.K = {'P': KP, 'I': KI, 'D': KD}
pid_control.e = {'t-1': 0., 't-2': 0.}


# Trying the simple way
mass = 20.
length = 15.
radius = 3.
inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
forces = [0, 0, 190.]
y0 = [0., 0., 300., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
y = y0
y_d = np.zeros(12)


y_log = []
t_step = .01

for t in range(5000):
    y = y + t_step*rocket_eq(t, y, forces, mass, length, inertia)
    forces = forces + pid_control(y_d, y)

    y_log.append(y)
    print(forces)

y_log = np.asarray(y_log)
plt.plot(y_log[:, 2])
plt.grid(True)
#plt.ylim((-10,400))
plt.show()


'''
def touchdown(t, y, _forces, _mass, _length, _inertia): return y[2]
touchdown.terminal = True
touchdown.direction = -1


def solve_rocket_eq():
    mass=20.
    length=15.
    radius=3.
    inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
    forces = [0, 0, 190.]
    y0 = [0., 0., 300., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

    sol = solve_ivp(rocket_eq, (0, 200), y0, args=(forces, mass, length, inertia), method='LSODA', events=touchdown, max_step=.1)
    plt.plot(sol.t, sol.y[2])
    plt.plot(sol.t, sol.y[8])
    plt.xlabel('t')
    plt.grid()
    plt.show()
'''
