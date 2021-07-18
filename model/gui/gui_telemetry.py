import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import norm
from scipy.spatial.transform import Rotation as R


def get_XYZ(angles):
    origin = np.array([0, 0, 0])
    A = R.from_euler('YX', angles)
    length = R.apply(A, np.array([0, 0, 15]))
    radius = 2
    magnitude = norm(length)
    unit_vector = length / magnitude
    not_v = np.array([1, 0, 0])
    if (unit_vector == not_v).all():
        not_v = np.array([0, 1, 0])
    n1 = np.cross(unit_vector, not_v)
    n1 /= norm(n1)
    n2 = np.cross(unit_vector, n1)
    t = np.linspace(0, magnitude, 10)
    theta = np.linspace(0, 2 * np.pi, 10)
    t, theta = np.meshgrid(t, theta)
    X, Y, Z = [origin[i] + unit_vector[i] * t + radius * np.sin(theta) * n1[i] + radius * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    return X, Y, Z

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = get_XYZ(np.array([0.125*np.pi, 0]))
ax.plot_surface(X, Y, Z)
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")
# plot axis
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_zlim(-20, 20)

plt.show()
