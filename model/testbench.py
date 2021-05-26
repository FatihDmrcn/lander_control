from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import numpy as np


def rocket_eq(t, y, _forces, _mass, _length, _inertia):
    matrix_rot = (1 / _mass) * R.from_euler('ZYX', [y[5], y[4], y[3]]).as_matrix()
    matrix_trq = - (_length / (2 * _inertia)) * np.array(((0, 1, 0), (1, 0, 0), (0, 0, 0)))
    A = np.vstack((matrix_rot, matrix_trq))
    dy_1dot = y[6:]
    dy_2dot = np.array((0., 0., -9.81, 0., 0., 0.)) + np.dot(A, _forces)
    return [*dy_1dot, *dy_2dot]


def touchdown(t, y, _forces, _mass, _length, _inertia): return y[2]
touchdown.terminal = True
touchdown.direction = -1


mass=20.
length=15.
radius=3.
inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
forces = [0, 0, 150.]
y0 = [0., 0., 300., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
t = np.linspace(0, 20, 1001)

sol = odeint(rocket_eq, y0, t, args=(forces, mass, length, inertia), tfirst=True)
sol2 = solve_ivp(rocket_eq, (0, 20), y0, args=(forces, mass, length, inertia), method='LSODA', events=touchdown, max_step=.1)
print(sol2)

plt.plot(t, sol[:, 2])
plt.plot(sol2.t, sol2.y[2])
plt.plot(t, sol[:, 8])
plt.plot(sol2.t, sol2.y[8])
plt.xlabel('t')
plt.grid()
plt.show()
