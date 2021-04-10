import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
import math
import copy


class QDrawWidget(Qtw.QWidget):

    light_blue = Qtg.QColor(135, 206, 235)
    dark_green = Qtc.Qt.darkGreen
    dark_red = Qtc.Qt.darkRed
    red = Qtc.Qt.red
    black = Qtc.Qt.black
    transparent = Qtc.Qt.transparent
    font = Qtg.QFont("Console")
    font.setFixedPitch(True)

    def __init__(self, rocket):
        super().__init__()
        self.painter = Qtg.QPainter()
        self.painter.setRenderHints(Qtg.QPainter.HighQualityAntialiasing)
        self.pen = Qtg.QPen()
        self.brush = Qtg.QBrush(Qtc.Qt.SolidPattern)

        self.r = rocket.radius
        self.l = rocket.length

        self.cos = rocket.cos_0dot
        self.vel = rocket.cos_1dot
        self.acc = rocket.cos_2dot

        self.forces = None
        self.deg = self.get_degees(self.cos)

        self.track = []

        self.setMinimumSize(1080, 720)

    def get_degees(self, cos):
        deg = copy.deepcopy(cos[3:])
        deg[:] = [math.degrees(d) for d in deg]
        return deg

    @Qtc.pyqtSlot(object, object, object)
    def reset(self, u_2dot, u_1dot, u_0dot):
        self.cos = u_0dot
        self.vel = u_1dot
        self.acc = u_2dot

        self.deg = self.get_degees(self.cos)
        self.track = []
        self.forces = None
        self.repaint()

    def get_parameter_text(self):
        axis = ['X', 'Y', 'Z', 'A', 'B', 'C']
        lines = '\t\tu_0dot\tu_1dot\tu_2dot\n'
        for j, i in enumerate(range(len(axis)), 0):
            lines += axis[i]+'\t'+'{:+06.1f}|{:+06.1f}|{:+06.1f}\n'.format(self.cos[i], self.vel[i], self.acc[i])
        return lines

    def draw_background(self):
        self.pen.setColor(self.transparent)
        self.pen.setJoinStyle(Qtc.Qt.MiterJoin)
        self.painter.setPen(self.pen)
        # Draw Ground
        self.brush.setColor(self.dark_green)
        self.painter.setBrush(self.brush)
        ground = Qtc.QRectF(-self.width()/2, 0, self.width()-1, 50-1)
        self.painter.drawRect(ground)
        # Draw Sky
        self.brush.setColor(self.light_blue)
        self.painter.setBrush(self.brush)
        sky = Qtc.QRectF(-self.width()/2, -self.height()+50, self.width()-1, self.height()-50)
        self.painter.drawRect(sky)

    def draw_tracker(self):
        if self.track:
            self.painter.save()
            self.pen.setColor(self.black)
            self.brush.setColor(self.transparent)
            self.painter.setPen(self.pen)
            self.painter.setBrush(self.brush)
            path = Qtg.QPainterPath()
            for i, cos in enumerate(self.track):
                x, z = cos[0], -cos[1]
                if i == 0:
                    path.moveTo(x, z)
                if i != 0:
                    path.lineTo(x, z)
            self.painter.drawPath(path)
            self.painter.restore()
        else:
            pass

    def draw_rocket(self):
        self.painter.save()
        self.pen.setColor(self.black)
        self.brush.setColor(self.black)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)
        self.painter.translate(self.cos[0], -self.cos[2])
        self.painter.rotate(self.deg[1])
        self.draw_thrust()
        rocket_tube = Qtc.QRectF(-self.r, -self.l/2, self.r*2, self.l)
        self.painter.drawRect(rocket_tube)
        self.painter.restore()

    def draw_thrust(self):
        if self.forces is not None:
            self.painter.save()
            self.pen.setColor(self.red)
            self.brush.setColor(self.transparent)
            self.painter.setPen(self.pen)
            self.painter.setBrush(self.brush)
            a = Qtc.QPointF(0., self.l/2)
            b = Qtc.QPointF(-self.forces[0], self.l/2+self.forces[2])
            self.painter.drawLine(a, b)
            self.painter.restore()
        else:
            pass

    def draw_parameter_box(self):
        self.pen.setColor(self.red)
        self.painter.setPen(self.pen)
        box = Qtc.QRectF(10, 10, 200, 200)
        self.painter.setFont(self.font)
        self.painter.drawText(box, Qtc.Qt.AlignLeft, self.get_parameter_text())

    def paintEvent(self, event):
        self.painter.begin(self)

        self.painter.save()
        self.painter.translate(self.width()/2, self.height()-50)
        self.draw_background()

        self.pen.setWidth(2)
        self.painter.setPen(self.pen)

        self.draw_tracker()
        self.draw_rocket()
        self.painter.restore()

        self.draw_parameter_box()
        self.painter.end()

    @Qtc.pyqtSlot(object, object, object, object)
    def update_widget(self, u_2dot, u_1dot, u_0dot, forces):
        self.cos = u_0dot
        self.vel = u_1dot
        self.acc = u_2dot
        self.deg = self.get_degees(self.cos)
        self.forces = forces
        self.track.append((self.cos[0], self.cos[2]))
        self.repaint()
