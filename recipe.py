''' Offline Recipe Generator for Domaille APM-HDC-5320

(c) 2025 under MIT License for not-for-profit use with attribution.
              Developed at the TDGO Fiber Optics Laboratory, 2025.
'''

import os

from obj import Settings, Recipe, RecipeStep, domaille_path

def show_menu():
    print()
    print("(L)ist Recipes")
    print("(V)iew a Recipe")
    print("(N)ew Recipe")   
    print("(Q)uit program and exit")


def ListRecipes():
# get a list of recipes from Domaille/Processes/
  try:
    recipeList = os.listdir("Domaille/Processes/")
    recipeList.remove('Steps')
  except Exception as e:
    raise e
  s = "" if len(recipeList) == 1 else "s"
  print(f"{len(recipeList)} recipe{s} found:")
  for index,recipe in enumerate(recipeList):
    print(f"  ({index+1}) {recipe}")
  return recipeList


def ViewRecipe():
  recipeList = ListRecipes()
  print("Which recipe would you like to view? (#)")
  try:
    recipeNum = int(input(" >> "))-1
    recipeName = recipeList[recipeNum]
  except Exception as e:
    print("Recipe not found.")
    print(e)
    return

  # Get the main recipe process:
  recipe = Recipe.read(recipeName)
  print(recipe.file_format())
  
  # Get each step of the recipe:  
  print()
  for step in range(1, len(recipe)+1):
    print(f"STEP #{step}:")
    print(recipe[step].file_format())


def NewRecipe():
  print("Creating new recipe...")
  recipeName = input("new recipe name: >> ")
  if not recipeName:
    print("Invalid recipe name.")
    return
  if os.path.exists(f"Domaille/Processes/{recipeName}"):
    print("Recipe name already exists. Recipe creation cancelled")
    return

  steps = input(f"How many steps in recipe {recipeName}? (default: 3) >> ")
  try:
    if steps == "": steps = 3
    else: steps = int(steps)
    if steps < 1 or steps > 9: raise ValueError
  except Exception as e: 
    print(f"ERROR: {e}")
    print("Invalid number of steps. Range is 1-9. Recipe creation cancelled.")
    return

  qty = input("what is the recipe max number of contacts? (default: 30) >> ")
  try:
    if qty == "": qty = 30
    else: qty = int(qty)
    if qty < 2 or qty > 72: raise ValueError
  except Exception as e: 
    print(f"ERROR: {e}")
    print("Invalid qty of contacts. Range is 2-72. Recipe creation cancelled.")
    return

  recipe = Recipe(recipeName, steps, qty)
  # get parameters from user and generate step files:
  for step in range(1, steps+1):
    print(f"Step {step} of {steps}:")
    time = 0
    while time < 10 or time > 300:
      print(f"  How many seconds should step #{step} run?")
      time = input(" >> ")   
      # validate input:
      try:
        time = int(time)
        if time < 10 or time > 300: 
          raise ValueError
      except Exception as e:
        print(f"ERROR: {e}. Value should be between 10 and 300.")
        time = 0
    pressure = -1
    while pressure < 0 or pressure > 16:
      print(f"  How much total pressure should step #{step} apply for {qty} contacts? (in lbs)")
      pressure = input(" >> ")
      # validate input for pressure:
      try:
        pressure = float(pressure)
        if pressure < 0 or pressure > 16:
          raise ValueError
      except Exception as e:
        print(f"ERROR: {e} Value should be between 0 and 16.")
        pressure = -1
        continue
      print(f"{pressure} lbs of pressure for {qty} contacts is {pressure/qty:.2f} lbs per contact.")
      confirm = input("Is this correct? Y/N >> ")
      if confirm.upper() == "Y": 
        break
      else:
        pressure = -1
        continue
    recipe_step = RecipeStep(time, pressure)
    recipe[step] = recipe_step
  try:
    recipe.write()
  except Exception as e:
    raise e
  else:
    print(f"Recipe {recipeName} generated with {steps} steps.")
    print(f"You may copy Domaille folder from {os.getcwd()} to flash drive.")
       

def main():
    print()
    print("Offline Recipe Generator for Domaille APM-HDC-5320\n")
    print("                          by Giles Cooper (c) 2025\n")
    # check for file structure
    try: 
        domaille_path()
        option = ""
    except:
        print("No working directory. Exiting.")
        return
    while option.upper() != "Q":
        show_menu()
        option = input(" >> ")
        if option.upper() == "L": ListRecipes()
        if option.upper() == "V": ViewRecipe()
        if option.upper() == "N": NewRecipe()


if __name__=="__main__":
    main()
    input("  press Return to exit program...\n")

