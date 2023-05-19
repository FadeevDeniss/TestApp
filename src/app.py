from PyQt6.QtWidgets import QApplication, QStyleFactory

from conf.settings import STATIC
from main_window import MainWindow


def main():
    app = QApplication([])

    app.setStyle(QStyleFactory.create("Fusion"))
    with open(STATIC + '/style.css') as f:
        app.setStyleSheet(f.read())

    ui = MainWindow()
    ui.window.show()
    app.exec()


if __name__ == '__main__':
    main()
