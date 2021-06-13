import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
import gui_widget as gw
from idgaf.model import run


class QThreadIntegrate(Qtc.QThread):
    threadFinished = Qtc.pyqtSignal()

    def __init__(self, model):
        super().__init__(model)
        self.model = model

    def run(self):
        print('IDGAF')
        self.model.integrate()


class MainClassAsGUI(Qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("You're my Baby!")
        #self.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)
        self.y_log, self.f_log = run()

        self.draw = gw.QDrawWidget(run.radius, run.length, run.y_initial)
        self.slider = Qtw.QSlider(Qtc.Qt.Horizontal)
        self.slider.setRange(0, len(self.y_log)-1)
        self.slider.sliderMoved.connect(self.update_state)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.draw)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.show()

    def update_state(self):
        pos = self.slider.value()
        self.draw.update_widget(self.y_log[pos, :6], self.y_log[pos, 6:12], self.f_log[pos])


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()
