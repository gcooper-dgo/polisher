from obj import Recipe, RecipeStep, Settings
from PyQt6 import QtWidgets, uic
import sys

from ui import Ui_MainWindow
from step import Ui_Form

print(Settings.read().file_format())

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

class StepForm(QtWidgets.QFormLayout, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)




app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()