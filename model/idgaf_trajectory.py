import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt


class Trajectory:
    @staticmethod
    def __get_orthogonal_vector(_vector, unit=True):
        orthogonal = np.array([-_vector[2], 0, _vector[0]])
        if unit:
            return Trajectory.__get_unit_vector(orthogonal)
        if not unit:
            return orthogonal

    @staticmethod
    def __get_unit_vector(_vector):
        _magnitude = np.linalg.norm(_vector)
        return (1 / _magnitude) * _vector

    @staticmethod
    def __get_signs(succession='mid', degree=1, magnitude=.1):
        start_value = np.nan
        end_value = np.nan
        if succession == 'last':
            start_value = -degree
            end_value = 1
        if succession == 'first':
            start_value = 0
            end_value = degree+1
        if succession == 'mid':
            start_value = -degree
            end_value = degree+1
        signs = np.arange(start_value, end_value, 1)
        signs = (magnitude/np.amax(np.absolute(signs)))*signs
        return signs

    @staticmethod
    def get_spline_elements(positions, vectors, degree=1, magnitude=.1):
        positions_new = []
        vectors_new = []
        for _i, (_p, _v) in enumerate(zip(positions, vectors), 0):
            if _v is np.nan:
                positions_new.append(_p)
                vectors_new.append((np.nan, np.nan, np.nan))
                continue
            succession = 'mid'
            if _i == 0:
                succession = 'first'
            if _i == len(vectors)-1:
                succession = 'last'
            signs = Trajectory.__get_signs(succession, degree=degree, magnitude=magnitude)
            unit_vector = Trajectory.__get_unit_vector(_v)
            for _s in signs:
                auxiliary_position = _p+_s*unit_vector
                positions_new.append(auxiliary_position)
                vectors_new.append(unit_vector)
        return np.asarray(positions_new), np.asarray(vectors_new)

    @staticmethod
    def spline(positions, vectors, degree=1, magnitude=.1, k=3):
        _p, _v = Trajectory.get_spline_elements(positions, vectors, degree=degree, magnitude=magnitude)
        # noinspection PyTupleAssignmentBalance
        _tck, _u = interpolate.splprep([_p[:, 0], _p[:, 1], _p[:, 2]], k=k, s=0)
        return _tck, _u, _p, _v

    @staticmethod
    def get_circular_plane(_position, _vector, number_of_edges=10, magnitude=10):
        unit_vector = Trajectory.__get_unit_vector(_vector)
        orthogonal = Trajectory.__get_orthogonal_vector(_vector)
        edges = []
        for _n in range(number_of_edges):
            r = R.from_rotvec(_n * (2 * np.pi / 10) * unit_vector)
            edge_vector = r.apply(orthogonal)
            edges.append(np.asarray(_position + magnitude*edge_vector))
        return np.asarray(edges)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-600, 20)
    ax.set_ylim3d(-600, 20)
    ax.set_zlim3d(0, 800)
    x_scale, y_scale, z_scale = 1, 1, 1
    scale = np.diag([x_scale, y_scale, z_scale, 1.0])
    scale = scale*(1.0/scale.max())
    scale[3,3] = 1.0


    def short_proj():
      return np.dot(Axes3D.get_proj(ax), scale)


    ax.get_proj = short_proj

    position = []
    vector = []
    position.append(np.array([-500, -500, 700]))
    position.append(np.array([-100, -100, 500]))
    position.append(np.array([0, 0, 0]))
    vector.append(np.array([1, 1, -.2]))
    vector.append(np.nan)
    vector.append(np.array([0, 0, -1]))

    tck, u, p, v = Trajectory.spline(position, vector, k=3, magnitude=40)
    u_fine = np.linspace(np.amin(p), np.amax(p), 100000)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck, ext=3)
    ax.plot(x_fine, y_fine, z_fine, 'r')
    ax.scatter(p[:, 0], p[:, 1], p[:, 2], color='k')

    for p, v in zip(position, vector):
        if v is np.nan:
            continue
        e = Trajectory.get_circular_plane(p, v, magnitude=40)
        ax.plot(e[:, 0], e[:, 1], e[:, 2], color='g')
        ax.quiver(p[0], p[1], p[2], v[0], v[1], v[2], length=40, color='b')

    plt.show()
