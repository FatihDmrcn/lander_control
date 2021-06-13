from .pid_attitude import pid_attitude
from .pid_thrust import pid_thrust


def pid_controller(_force, _y_desired, _y_actual):
    return pid_thrust(_force, _y_desired, _y_actual)

