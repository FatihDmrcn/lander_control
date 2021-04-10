import PyQt5.QtCore as Qtc
import PyQt5.QtWidgets as Qtw
from model import idgaf_model, gui_widget as gw


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
        self.setSizePolicy(Qtw.QSizePolicy.Fixed, Qtw.QSizePolicy.Fixed)

        self.model = idgaf_model.IDGAF()
        self.draw = gw.QDrawWidget(self.model)
        self.thread = QThreadIntegrate(self.model)
        self.model.steps.connect(self.draw.update_widget)
        self.model.reset.connect(self.draw.reset)
        self.reset()

        self.button_start = Qtw.QPushButton('Start Baby!')
        self.button_start.clicked.connect(self.start_simulation)
        self.button_reset = Qtw.QPushButton('Redo this Baby!')
        self.button_reset.clicked.connect(self.reset)

        layout = Qtw.QVBoxLayout()
        layout.addWidget(self.draw)
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_reset)
        self.setLayout(layout)

        self.show()

    def start_simulation(self):
        self.thread.start()

    def reset(self):
        self.model.randomize_ic()


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI()
    gui.show()
    app.exec_()
