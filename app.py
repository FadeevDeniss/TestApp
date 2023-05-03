from PyQt6.QtWidgets import QApplication, QStyleFactory

from main_window import MainWindow


def main():
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Fusion"))

    app.setStyleSheet('''
        QWidget {
        
            font-size: 15px;
        }
            
        QLabel {
            
            font-size: 15px;
            font-weight: bold;
        
        }

        QPushButton {

            font-size: 15px;
            font-weight: bold;
        }

        QPushButton {

            border-radius: 5px;
            background-color: #2e2e2d;
            min-width: 80px;
            min-height: 35%;
            
        }

        QPushButton:pressed {

            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 grey, stop: 1 white);
        }

        QPushButton:flat {

            border: 0; /* no border for a flat push button */
        }

        QPushButton:default {

            border: 1px solid qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0,
                                              stop: 0 #F98B36, stop: 1 #D64F00);
        }
        
        QPushButton:hover {
            
            border: 1px solid qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0,
                                              stop: 0 #F98B36, stop: 1 #D64F00);
            
        }

        QLineEdit {

            height: 35%;
            border-radius: 5px;
            padding: 0 8px;
            background: black;
            selection-background-color: darkgray;
            
        }
        
        QLineEdit:focus {
            
            border: 1px solid qlineargradient(x1: 0, y1: 1, x2: 0, y2: 0,
                                              stop: 0 #F98B36, stop: 1 #D64F00);           
        }    

        QListView {

            alternate-background-color: black;
        }
        
        QListView::item:selected {

            border: 1px solid #FF8027;
        }
        ''')

    ui = MainWindow()
    ui.window.show()
    app.exec()


if __name__ == '__main__':
    main()
