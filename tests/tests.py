import json
import unittest

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QStyleFactory

from src.main_window import MainWindow, ContactsList


class MainWindowTestCase(unittest.TestCase):

    def setUp(self):
        with open('mock.json') as mck:
            self.test_json = json.loads(mck.read())
        self.app = QApplication([])
        self.app.setStyle(QStyleFactory.create("Fusion"))
        self.ui = MainWindow()

    def tearDown(self) -> None:
        self.ui.window.close()

    def test_window_size(self):
        self.assertEqual(self.ui.window.baseSize(), QSize(500, 700),
                         'incorrect base size')
        self.assertEqual(self.ui.window.maximumSize(), QSize(600, 800),
                         'incorrect max size')

    def test_window_resize(self):
        self.ui.window.resize(600, 750)
        self.assertEqual(self.ui.window.size(), QSize(600, 750),
                         'wrong size after resize')

    def test_custom_model(self):
        model = self.ui.model
        self.assertEqual(isinstance(model, ContactsList), True, 'Wrong type of model')
        self.assertEqual(hasattr(model, 'contacts'), True, "No attribute \'contacts\' in model")
        self.assertEqual(model.rowCount(), 0, 'Contacts attr not empty')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(MainWindowTestCase('test_window_size'))
    suite.addTest(MainWindowTestCase('test_window_resize'))
    suite.addTest(MainWindowTestCase('test_send_contact'))
    suite.addTest(MainWindowTestCase('test_custom_model'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())





