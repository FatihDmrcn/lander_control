import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
from .gui_display import QDisplay


class MainClassAsGUI(Qtw.QWidget):

    def __init__(self, run):
        super().__init__()
        self.setWindowTitle("You're my Baby!")
        self.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)
        self.run = run
        self.y_log, self.f_log = run()

        self.draw = QDisplay(run.radius, run.length, run.y_initial)
        self.slider = Qtw.QSlider(Qtc.Qt.Horizontal)
        self.slider.setRange(0, len(self.y_log)-1)
        self.slider.sliderMoved.connect(self.update_state)
        self.button = Qtw.QPushButton("Animate")
        self.button.clicked.connect(self.start)

        self.counter = 0
        self.timer = Qtc.QTimer(self)
        self.timer.timeout.connect(self.animate)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.draw)
        layout.addWidget(self.slider)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.show()

    def start(self):
        self.counter = 0
        self.slider.setDisabled(True)
        self.button.setDisabled(True)
        self.timer.start(4)

    def animate(self):
        self.draw.update_widget(self.y_log[self.counter, :6], self.y_log[self.counter, 6:12], self.f_log[self.counter])
        if self.counter < self.run.t_total:
            self.counter += 1
            self.slider.setValue(self.counter)
        if self.counter == self.run.t_total:
            self.timer.stop()
            self.slider.setEnabled(True)
            self.button.setEnabled(True)

    def update_state(self):
        pos = self.slider.value()
        self.draw.update_widget(self.y_log[pos, :6], self.y_log[pos, 6:12], self.f_log[pos])
