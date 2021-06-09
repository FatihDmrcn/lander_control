from idgaf.rocket_model import rocket_eq
from idgaf.rocket_pid import pid_thrust
import matplotlib.pyplot as plt
import numpy as np


mass = 20.
length = 15.
radius = 3.
inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
forces = np.zeros(3)

y0 = [0., 0., 800., 0., 0., 0., 0., 0., 50., 0., 0., 0.]
y = y0
y_d = np.zeros(12)

y_log = [y0]
f_log = [forces]
t_step = .01
t_total = 5000

for t in range(5000):
    forces = pid_thrust(forces, y_d, y)
    y = y + t_step*rocket_eq(t, y, forces, mass, length, inertia)
    y_log.append(y)
    f_log.append(forces)

t_begin = 0
t_end = t_total*t_step
t_axis = np.linspace(t_begin, t_end, t_total+1)
y_log = np.asarray(y_log)
f_log = np.asarray(f_log)

plt.xlim(t_begin, t_end)
plt.plot(t_axis, y_log[:, 2], label='alt')
plt.plot(t_axis, y_log[:, 8], label='vel')
plt.plot(t_axis, f_log[:, 2], label='force_z')
plt.grid(True)
plt.legend()
plt.show()
