import json
import requests

from PyQt6 import QtCore
from PyQt6.QtGui import (
    QFont, QFontDatabase
)
from PyQt6.QtCore import (
    QSize,
    QAbstractListModel,
    Qt,
    QModelIndex
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QListView,
    QLineEdit,
    QWidget,
    QHBoxLayout,
    QGridLayout, QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel
)

from dto import RequestDto


class ContactsList(QAbstractListModel):

    def data(self, index, role=None) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            data = self.contacts[index.row()]
            return data

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self.contacts)

    def __init__(self, contacts: list | None):
        super().__init__()
        self.contacts = contacts or []


class CustomDialogue(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        q_button = QDialogButtonBox.StandardButton.Close
        font_id = QFontDatabase.addApplicationFont("Commissioner-Medium.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)

        self.btn_box = QDialogButtonBox(q_button)
        self.btn_box.setCenterButtons(True)
        self.btn_box.clicked.connect(self.close)

        self.layout = QVBoxLayout()
        self.message = QLabel()
        self.message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.message.setFont(QFont(families[0], 80))
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.btn_box)
        self.message.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)


class TextInput(QLineEdit):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(TextInput, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())


class MainWindow:

    def __init__(self):
        self.window = QMainWindow()
        self.widget = QWidget()
        self.model = ContactsList([])

        self.btn_submit = QPushButton('Send')
        self.btn_get = QPushButton('Get contacts')
        self.line_edit = TextInput()
        self.list_view = QListView()

        font_id = QFontDatabase.addApplicationFont("Commissioner-Medium.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        main_layout = QGridLayout()
        layout_1 = QHBoxLayout()

        self.btn_get.setFont(QFont(families[0], 80))
        self.btn_submit.setFont(QFont(families[0], 80))
        self.list_view.setFont(QFont(families[0], 80))

        self.window.setWindowTitle('Simple app')

        self.btn_submit.clicked.connect(self.btn_send_clicked)
        self.btn_get.clicked.connect(self.btn_get_clicked)
        self.line_edit.textEdited.connect(self.text_edited)
        self.line_edit.keyPressed.connect(self.key_pressed)

        layout_1.addWidget(self.line_edit)
        layout_1.addWidget(self.btn_submit)

        main_layout.addLayout(layout_1, 0, 0)

        main_layout.addWidget(self.btn_get, 3, 0)
        main_layout.addWidget(self.list_view, 1, 0)

        self.widget.setLayout(main_layout)
        self.window.setBaseSize(QSize(500, 700))
        self.window.setMaximumSize(QSize(600, 800))
        self.window.setGeometry(400, 400, 550, 500)
        self.window.setCentralWidget(self.widget)

        self.btn_submit.setEnabled(False)
        self.widget.setFocus()

    def btn_get_clicked(self):
        self.model = ContactsList([])
        try:
            data = requests.get(
                'http://127.0.0.1:5000/simpleserver/api/contacts',
                headers={
                    'X-Correlation-Id': '13aa24a8-2460-4222-9133-8000346f8456',
                    'Content-Type': 'application/json',
                    'Accept-Encoding': 'gzip',
                    'Connection': 'keep-alive'
                }
            )
            for i in data.json():
                item = RequestDto(**i)
                self.insert(item)
        except Exception as err:
            self.model.contacts.append(f"{err.request.url} NOT RESPONDING")
        finally:
            self.list_view.setModel(self.model)

    def insert(self, item: RequestDto) -> None:
        item = item.__dict__.values()
        pretty = '     '.join([str(i).center(20) for i in list(item)])
        self.model.contacts.append(pretty)

    def btn_send_clicked(self):
        data = json.dumps({'telephone': self.line_edit.text()})
        self.line_edit.setInputMask('')
        self.line_edit.clear()
        dlg = CustomDialogue(self.window)
        try:
            response = requests.post(
                'http://127.0.0.1:5000/simpleserver/api/contacts',
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept-Encoding': 'gzip',
                    'Connection': 'keep-alive'
                })
            dlg.message.setText(f"{json.loads(response.json()[0]).get('result')}")
        except Exception as err:
            dlg.message.setText(f"{err.request.url} NOT RESPONDING")
        finally:
            dlg.exec()

    def text_edited(self, s):
        if self.line_edit.isModified():
            self.btn_submit.setEnabled(True)
        if self.line_edit.inputMask() == '':
            self.line_edit.setInputMask('+7 999 999-99-99;_')

    def key_pressed(self, key):
        if self.line_edit.cursorPosition() == 16 and not self.line_edit.isModified():
            self.line_edit.setCursorPosition(6)
