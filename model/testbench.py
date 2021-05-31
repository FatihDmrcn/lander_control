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



# Trying the simple way
mass=20.
length=15.
radius=3.
inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
forces = [0, 0, 190.]
y0 = [0., 0., 300., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
y = y0
y_d = np.zeros(6)

e_error = np.zeros(6)
e_prev_error_1 = np.zeros(6)
e_prev_error_2 = np.zeros(6)

KP = np.zeros((3, 6))
KD = np.zeros((3, 6))
KI = np.zeros((3, 6))

KP[2, 2] = 19
KI[2, 2] = .001
KD[2, 2] = 4000

y_log = []
t_step = .01

for t in range(5000):
    y = y + t_step*rocket_eq(t, y, forces, mass, length, inertia)
    y_log.append(y)
    e_error = y_d - y[:6]

    e_p = e_error-e_prev_error_1
    e_i = e_error+e_prev_error_1
    e_d = e_error-2*e_prev_error_1+e_prev_error_2

    forces = forces + np.dot(KP, e_p) + np.dot(KI, e_i) + np.dot(KD, e_d)
    print(forces)

    e_prev_error_2 = e_prev_error_1
    e_prev_error_1 = e_error


y_log = np.asarray(y_log)
plt.plot(y_log[:, 2])
plt.grid(True)
#plt.ylim((-10,400))
plt.show()

