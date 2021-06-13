from run_model import run
from gui.gui_main import MainClassAsGUI
import PyQt5.QtWidgets as Qtw


if __name__ == "__main__":
    app = Qtw.QApplication([])
    gui = MainClassAsGUI(run)
    gui.show()
    app.exec_()
