import dataclasses
import json
import os

import requests

from PyQt6 import QtCore
from PyQt6.QtGui import (
    QFont,
    QFontDatabase
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
    QGridLayout,
    QDialog,
    QVBoxLayout,
    QLabel
)

from src.dto import RequestDto
from conf.settings import (
    STATIC, BASE_URL
)


class ContactsList(QAbstractListModel):

    """
    Custom model, representing row in QListView widget
    """

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

    """
    Class represents dialogue window widget.
    Window displayed after send button pressed,
    contains QLabel with textual result and QPushButton
    for closing, placed vertically
    """

    def __init__(self, parent=None):

        super().__init__(parent)

        font_id = QFontDatabase.addApplicationFont(
            os.path.join(
                STATIC,
                "fonts\\barlow\\BarlowCondensed-Medium.ttf"
            )
        )
        families = QFontDatabase.applicationFontFamilies(font_id)

        self.q_button = QPushButton('close')
        self.q_button.setProperty('class', 'close_btn')
        self.q_button.clicked.connect(self.close)

        self.message = QLabel()
        self.message.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.message.setFont(QFont(families[0], 80))
        self.message.setContentsMargins(5, 10, 5, 10)
        self.message.setWordWrap(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.q_button)

        self.setMinimumWidth(150)
        self.setMinimumHeight(120)
        self.setLayout(self.layout)


class TextInput(QLineEdit):

    """
    Custom class that inherits QLineEdit widget
    """
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(TextInput, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())


class MainWindow:

    """
    Container class for managing application main window
    """

    API_PATH = '/simpleserver/api/contacts'
    HEADERS = {
        'Content-Type': 'application/json',
        'Connection': 'keep-alive'
    }

    def __init__(self):

        main_layout = QGridLayout()
        horizontal_layout = QHBoxLayout()
        font_id = QFontDatabase.addApplicationFont(
            os.path.join(
                STATIC, "fonts\\barlow\\BarlowCondensed-Medium.ttf"
            )
        )
        view_font_id = QFontDatabase.addApplicationFont(
            os.path.join(
                STATIC, "fonts\\play\\Play-Regular.ttf"
            )
        )
        main_family = QFontDatabase.applicationFontFamilies(font_id)
        view_family = QFontDatabase.applicationFontFamilies(view_font_id)

        self.window = QMainWindow()
        self.widget = QWidget()
        self.model = ContactsList([])

        self.window.setWindowTitle('Simple app')

        self.btn_submit = QPushButton('send')
        self.btn_get = QPushButton('get contacts')
        self.textline = TextInput()
        self.view = QListView()

        for v in (self.btn_submit, self.btn_get):
            v.setFont(QFont(main_family[0]))
        self.view.setFont(QFont(view_family[0]))

        self.btn_submit.clicked.connect(self.btn_send_clicked)
        self.btn_get.clicked.connect(self.btn_get_clicked)
        self.textline.textEdited.connect(self.text_edited)
        self.textline.keyPressed.connect(self.key_pressed)

        horizontal_layout.addWidget(self.textline)
        horizontal_layout.addWidget(self.btn_submit)

        main_layout.addLayout(horizontal_layout, 0, 0)
        main_layout.addWidget(self.btn_get, 3, 0)
        main_layout.addWidget(self.view, 1, 0)

        self.widget.setLayout(main_layout)

        self.window.setMaximumSize(QSize(600, 800))
        self.window.setGeometry(550, 120, 500, 600)
        self.window.setCentralWidget(self.widget)

        self.btn_submit.setEnabled(False)

    def btn_get_clicked(self):
        self.model = ContactsList([])
        try:
            data = requests.get(BASE_URL + self.API_PATH)
            data.raise_for_status()
            for i in data.json():
                self.insert(
                    RequestDto(**i)
                )
        except requests.HTTPError as http_err:
            self.model.contacts.append(
                f"Error: {http_err}"
            )
        finally:
            self.view.setModel(self.model)

    def insert(self, item: RequestDto) -> None:
        item = dataclasses.asdict(item).values()
        pretty = '   '.join(
            [str(i).rjust(10, ' ') for i in list(item)])
        self.model.contacts.append(pretty)

    def btn_send_clicked(self):

        dlg = CustomDialogue(self.window)
        data = json.dumps({'telephone': self.textline.text()})

        self.textline.setInputMask('')
        self.textline.clear()

        try:
            response = requests.post(
                BASE_URL + self.API_PATH, data=data, headers=self.HEADERS
            )
            response.raise_for_status()
            dlg.message.setText(
                f"{json.loads(response.json()[0]).get('result')}"
            )
        except requests.ConnectionError as con_err:
            winerror = str(con_err).split(':')[-1][:-3].strip()
            dlg.message.setText(winerror)
        finally:
            dlg.exec()

    def text_edited(self, s):
        num_count = len([i for i in self.textline.displayText() if i.isnumeric()])
        if num_count >= 11:
            self.btn_submit.setEnabled(True)
        if self.textline.inputMask() == '':
            self.textline.setInputMask('+7 (999) 999-99-99;_')
        if len(s) <= 1:
            self.textline.cursorForward(False, 1)

    def key_pressed(self, key):
        if self.textline.cursorPosition() == 16 and not self.textline.isModified():
            self.textline.cursorBackward(False, 8)
        if key == QtCore.Qt.Key.Key_Backspace:
            self.btn_submit.setEnabled(False)

