import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
import math
import copy


class QDisplay(Qtw.QWidget):

    light_blue = Qtg.QColor(135, 206, 235)
    dark_green = Qtc.Qt.darkGreen
    dark_red = Qtc.Qt.darkRed
    red = Qtc.Qt.red
    black = Qtc.Qt.black
    white = Qtc.Qt.white
    transparent = Qtc.Qt.transparent
    font = Qtg.QFont("Console")
    font.setFixedPitch(True)

    def __init__(self, _r, _l, y):
        super().__init__()
        self.radius = _r
        self.length = _l

        self.cos = y[:6]
        self.vel = y[6:12]
        self.forces = None
        self.deg = self.get_degrees(self.cos)

        self.track = []
        self.setMinimumSize(1080, 720)

    @staticmethod
    def get_degrees(cos):
        deg = copy.deepcopy(cos[3:])
        deg[:] = [math.degrees(d) for d in deg]
        return deg

    @Qtc.pyqtSlot(object, object, object, object)
    def update_widget(self, u_0dot, u_1dot, forces):
        self.cos = u_0dot
        self.vel = u_1dot
        self.deg = QDisplay.get_degrees(self.cos)
        self.forces = forces
        self.track.append((self.cos[0], self.cos[2]))
        self.repaint()

    def paintEvent(self, event):
        painter = Qtg.QPainter()
        painter.setRenderHints(Qtg.QPainter.Antialiasing)

        pen = Qtg.QPen()
        pen.setJoinStyle(Qtc.Qt.MiterJoin)
        pen.setColor(self.transparent)
        painter.setPen(pen)

        brush = Qtg.QBrush(Qtc.Qt.SolidPattern)
        brush.setColor(self.transparent)
        painter.setBrush(brush)

        painter.begin(self)

        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.scale(12., 12.)
        self.draw_background(painter, pen, brush)
        self.draw_rocket(painter, pen, brush)
        painter.restore()

        self.draw_parameter_box(painter, pen)
        painter.end()

    def draw_background(self, painter, pen, brush):
        painter.save()
        painter.translate(-self.cos[0], self.cos[2])
        pen.setColor(self.transparent)
        painter.setPen(pen)

        # Draw Ground
        brush.setColor(self.dark_green)
        painter.setBrush(brush)
        ground = Qtc.QRectF(-self.width(), 0, 2*self.width(), 2000)
        painter.drawRect(ground)

        # Draw Sky
        brush.setColor(self.light_blue)
        painter.setBrush(brush)
        sky = Qtc.QRectF(-self.width(), -2000, 2*self.width(), 2000)
        painter.drawRect(sky)

        painter.restore()

    def draw_rocket(self, painter, pen, brush):
        painter.save()
        painter.rotate(self.deg[1])

        brush.setColor(self.white)
        painter.setBrush(brush)
        pen.setColor(self.black)
        pen.setWidthF(.25)
        painter.setPen(pen)

        self.draw_thrust(painter, pen, brush)
        rocket_tube = Qtc.QRectF(-self.radius, -self.length / 2, self.radius * 2, self.length)
        painter.drawRect(rocket_tube)

        painter.restore()

    def draw_thrust(self, painter, pen, brush):
        if self.forces is not None:
            painter.save()
            pen.setColor(self.red)
            painter.setPen(pen)

            brush.setColor(self.transparent)
            painter.setBrush(brush)

            a = Qtc.QPointF(0., self.length / 2)
            scale = 0.1
            b = Qtc.QPointF(-scale*self.forces[0], self.length / 2 + scale*self.forces[2])
            painter.drawLine(a, b)
            painter.restore()
        else:
            pass

    def draw_parameter_box(self, painter, pen):
        pen.setColor(self.red)
        painter.setPen(pen)
        box = Qtc.QRectF(10, 10, 200, 200)
        painter.setFont(self.font)
        painter.drawText(box, Qtc.Qt.AlignLeft, self.get_parameter_text())

    def get_parameter_text(self):
        axis = ['X', 'Y', 'Z', 'A', 'B', 'C']
        lines = '\t\t\tu_0dot\t\tu_1dot\n'
        for j, i in enumerate(range(len(axis)), 0):
            lines += axis[i]+'\t'+'{:+07.1f}|{:+07.1f}\n'.format(self.cos[i], self.vel[i])
        return lines
