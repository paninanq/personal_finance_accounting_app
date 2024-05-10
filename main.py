from gui_fin.main_gui import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec()
