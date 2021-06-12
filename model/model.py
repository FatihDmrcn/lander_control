from idgaf.rocket_model import rocket_eq
from idgaf.rocket_pid import pid_attitude, pid_thrust
import matplotlib.pyplot as plt
import numpy as np


def plot_telemetry():
    pass


mass = 20.
length = 15.
radius = 3.
inertia = 0.25*mass*(radius**2 + (1/3)*length**2)
forces = np.zeros(3)

y0 = [0., 0., 1500., 0., -np.pi, 0., 0., 0., -50., 0., 0., 0.]
y = y0
y_d = np.zeros(12)
y_d[2] = length/2.

y_log = [y0]
f_log = [forces]
t_step = .01
t_total = 5000

for t in range(5000):
    forces = pid_attitude(forces, y_d, y)
    y = y + t_step*rocket_eq(t, y, forces, mass, length, inertia)
    print(forces)
    y_log.append(y)
    f_log.append(forces)

t_begin = 0
t_end = t_total*t_step
t_axis = np.linspace(t_begin, t_end, t_total+1)
y_log = np.asarray(y_log)
f_log = np.asarray(f_log)

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
fig.suptitle('Aligning x-axis using sharex')
# ax1.plot(t_axis, y_log[:, 2], label='alt')
ax1.plot(t_axis, y_log[:, 4], label='alt')
ax1.set_xlim(t_begin, t_end)
ax1.grid(True)

# ax2.plot(t_axis, y_log[:, 8], label='vel')
ax2.plot(t_axis, y_log[:, 10], label='vel')
ax2.grid(True)

# ax3.plot(t_axis, f_log[:, 2], label='force')
ax3.plot(t_axis, f_log[:, 0], label='force')
ax3.grid(True)
plt.show()
