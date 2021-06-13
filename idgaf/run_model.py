from rocket.rocket_model import rocket_eq
from pid.controller import pid_controller
import matplotlib.pyplot as plt
import numpy as np


def run():
    y_actual = run.y_initial
    forces = np.zeros(3)

    _y_log = [y_actual]
    _f_log = [forces]

    for t in range(run.t_total):
        forces = pid_controller(forces, run.y_desired, y_actual)
        y_actual = y_actual + run.t_step * rocket_eq(t, y_actual, forces, run.mass, run.length, run.inertia)
        _y_log.append(y_actual)
        _f_log.append(forces)

    return np.asarray(_y_log), np.asarray(_f_log)


run.mass = 20.
run.length = 15.
run.radius = 3.
run.inertia = 0.25*run.mass*(run.radius**2 + (1/3)*run.length**2)
run.y_desired = np.zeros(12)
run.y_desired[2] = run.length/2.
run.y_initial = [0., 0., 1500., 0., -np.pi, 0., 0., 0., -50., 0., 0., 0.]

run.t_begin = 0
run.t_step = .01
run.t_total = 5000
run.t_end = run.t_total*run.t_step
run.t_axis = np.linspace(run.t_begin, run.t_end, run.t_total+1)


if __name__ == '__main__':
    y_log, f_log = run()

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    fig.suptitle('Aligning x-axis using sharex')
    ax1.plot(run.t_axis, y_log[:, 2], label='alt')
    ax1.plot(run.t_axis, y_log[:, 4], label='alt')
    ax1.set_xlim(run.t_begin, run.t_end)
    ax1.grid(True)

    ax2.plot(run.t_axis, y_log[:, 8], label='vel')
    ax2.plot(run.t_axis, y_log[:, 10], label='vel')
    ax2.grid(True)

    ax3.plot(run.t_axis, f_log[:, 2], label='force')
    ax3.plot(run.t_axis, f_log[:, 0], label='force')
    ax3.grid(True)
    plt.show()

