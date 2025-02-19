class Settings():
    def __init__(self):
        pass

class RecipeStep():
    def __init__(self, time=75, pressure=16):
        self.time = time
        self.speed = 110
        self.speed_ramp = 1
        self.pressure = pressure
        self.pressure_ramp = 1
        self.fci = 5
        self.lower_speed_limit = 10
        self.upper_speed_limit = 10
        self.lower_pressure_limit = 0.5
        self.upper_pressure_limit = 0.5
        self.fixture_weight = 0
        self.film = ""
        self.flubricant = "DI Water"
        self.pad = "70 Duro Violet"
        self.description1 = ""
        self.description2 = ""
        self.speed_ramp_dn = 1
        self.pressure_ramp_dn = 1

    def __repr__(self):
        return f"<Step({self.time}s @ {self.pressure}lbs.)>"


class Recipe():
    def __init__(self, description:str, no_of_steps:int = 3, quantity:int = 32, rework_step:int = 1):
        self.description = description
        self.no_of_steps = no_of_steps
        self.quantity = quantity
        self.rework_step = rework_step
        
        self._step = []
        for _ in range(no_of_steps):
            self._step.append(RecipeStep())

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

