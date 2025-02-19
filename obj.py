class Settings():
    def __init__(self):
        pass

class RecipeStep():
    def __init__(self, time, pressure):
        self.time = time
        self.pressure = pressure

class Recipe():
    def __init__(self, description:str, no_of_steps:int = 3, quantity:int = 32, rework_step:int = 1):
        self.description = description
        self.no_of_steps = no_of_steps
        self.quantity = quantity
        self.rework_step = rework_step
        
        self._step = [None]
        for _ in range(no_of_steps-1):
            self._step.append(None)

    def __getitem__(self, index) -> RecipeStep:
        return self._step[index-1]
  
    def __setitem__(self, index, value:RecipeStep) -> None:
        self._step[index-1] = value

    def __len__(self):
        return len(self._step)



recipe = Recipe('test')
print(f"recipe length: {len(recipe)}")
for x in range(1, 4):
    print(f"step {x}: {recipe[x]}")

