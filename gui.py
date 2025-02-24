from obj import Recipe, RecipeStep, Settings
from PyQt6 import QtWidgets, uic
import sys

from ui import Ui_MainWindow
from step import Ui_Form

settings = Settings.read()
recipe = Recipe('recipe',3,32,1,RecipeStep(film="Brown 5um"),RecipeStep(),RecipeStep())
print(len(recipe))

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.load_settings(settings)
        self.load_recipe(recipe)
        
    def load_settings(self, settings:Settings):
        self.cbo_film.addItems(settings.film)
        self.cbo_film_2.addItems(settings.film)
        self.cbo_film_3.addItems(settings.film)
        self.cbo_pad.addItems(settings.pad)
        self.cbo_pad_2.addItems(settings.pad)
        self.cbo_pad_3.addItems(settings.pad)
        self.cbo_lubricant.addItems(settings.lubricant)
        self.cbo_lubricant_2.addItems(settings.lubricant)
        self.cbo_lubricant_3.addItems(settings.lubricant)

    def load_recipe(self, recipe:Recipe):
        self.description.setText(recipe.description)
        self.no_of_steps.setValue(recipe.no_of_steps)
        self.quantity.setValue(recipe.quantity)
        self.rework_step.setValue(recipe.rework_step)
        self.cbo_film.setCurrentText(recipe[1].film)
        print(f"{recipe[3].film} == {self.cbo_film.currentText()} ? ")
        self.cbo_film_2.setCurrentText(recipe[2].film)
        self.cbo_film_3.setCurrentText(recipe[3].film)
        


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()