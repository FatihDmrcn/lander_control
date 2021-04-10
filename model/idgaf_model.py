import numpy as np
from scipy.spatial.transform import Rotation as R
import PyQt5.QtCore as Qtc
# SELAM VE DUA LIPA
# FIFTY-ONE-ERGS


class IDGAF(Qtc.QObject):

    gravity = (0., 0., -9.81)

    steps = Qtc.pyqtSignal(object, object, object, object)
    reset = Qtc.pyqtSignal(object, object, object)

    def __init__(self, mass=20., length=15., radius=3.):
        super().__init__()
        self.mass = mass
        self.length = length
        self.radius = radius
        self.inertia = 0.25*self.mass*(self.radius**2 + (1/3)*self.length**2)

        self.F_total = 200.
        self.angle_max = np.pi/8
        self.F_orthogonal = self.F_total * np.sin(self.angle_max)

        # x, y, z, alpha, beta, gamma
        self.cos_2dot = [0., 0., 0., 0., 0., 0.]
        self.cos_1dot = [0., 0., 0., 0., 0., 0.]
        self.cos_0dot = [0., 0., 0., 0., 0., 0.]

        self.u_2dot = []
        self.u_1dot = []
        self.u_0dot = []
        self.forces = []

    def F(self, forces, u_n):
        r = R.from_euler('ZYX', [u_n[5], u_n[4], u_n[3]])               # Roll, Pitch, Yaw
        t = np.array(((0, 1, 0), (1, 0, 0), (0, 0, 0)))                 # Matrix for torque

        f_xyz = self.gravity + r.apply(forces) / self.mass              # translational acceleration in x, y, z
        f_abc = - (self.length/2) * np.dot(t, forces) / self.inertia    # rotational acceleration in a, b, c

        return np.concatenate((f_xyz, f_abc))

    def thrust_exceeding(self, thrust_vector):
        def check_thrust(vector):
            if 0 <= np.linalg.norm(vector) < self.F_total: return False
            else: return True

        def check_angles(vector):
            if 0 <= np.sqrt(vector[0]**2+vector[1]**2) < self.F_orthogonal: return False
            else: return True

        if check_thrust(thrust_vector) or check_angles(thrust_vector): return True
        else: return False

    def thrust_control(self, u_0dot, u_1dot, r_0dot=np.array((0, 0, 500, 0, 0, 0))):
        # THIS IS THE PART WITH NN!
        e_0dot = u_0dot - r_0dot

        U_0mat = np.ones((3, 6))
        U_1mat = np.random.rand(3, 6)
        F_vector = np.dot(U_0mat, u_0dot) + np.dot(U_1mat, u_1dot)
        while self.thrust_exceeding(F_vector):
            U_1mat = np.random.rand(3, 6)
            F_vector = np.dot(U_0mat, u_0dot) + np.dot(U_1mat, u_1dot)
        # thrust_vector = np.array([1.2, 0., 200.])
        return F_vector

    def trajectory(self):
        # IDGAF Trajectory is done so far
        pass

    def integrate(self):
        Time = 200.
        t = 0.01
        ct = 0
        while ct < Time:
            forces = self.thrust_control(self.cos_0dot, self.cos_1dot)
            self.cos_2dot = self.F(forces, self.cos_0dot)
            self.cos_1dot = self.cos_2dot*t + self.cos_1dot
            self.cos_0dot = self.cos_1dot*t + self.cos_0dot

            self.u_2dot.append(self.cos_2dot)
            self.u_1dot.append(self.cos_1dot)
            self.u_0dot.append(self.cos_0dot)
            self.forces.append(forces)

            thrust_vector = 20.*forces/np.linalg.norm(forces)
            self.steps.emit(self.cos_2dot, self.cos_1dot, self.cos_0dot, thrust_vector)

            if self.cos_0dot[2] <= self.length/2:
                break
            ct += t

    def randomize_ic(self):
        self.cos_0dot = [-700., 0., 700., 0., np.pi/4., 0.]
        self.cos_1dot = [30., 0., -5., 0., 0., 0.]
        self.cos_2dot = [0., 0., 0., 0., 0., 0.]

        self.reset.emit(self.cos_2dot, self.cos_1dot, self.cos_0dot)

        self.u_0dot[:] = []
        self.u_1dot[:] = []
        self.u_2dot[:] = []
        self.forces[:] = []
