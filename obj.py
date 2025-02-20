import os

def domaille_path() -> bool:
    ''' check to see if the path directories exist'''
    if os.path.isdir(f'Domaille{os.sep}Processes{os.sep}Steps'):
        return f"{os.getcwd()}{os.sep}Domaille"
    else:
        try:
            os.makedirs(f'Domaille{os.sep}Processes{os.sep}Steps')
            if not os.path.exists(f"Domaille{os.sep}Settings.txt"):
                Settings.default().write()
        except Exception as e:
            print('FAILED: ', e)
            raise e
        else:
            return f"{os.getcwd()}{os.sep}Domaille"

class Settings():
    def __init__(self, max_quantity=32, film=[], pad=[], lubricant=[]):
        self.max_quantity = max_quantity
        self.film = film
        self.pad = pad
        self.lubricant = lubricant

    @staticmethod
    def default():
        return Settings(32, ['<None>', 'Brown 5um', 'Purple 1um', 'Clear FOS-22'],
                            ['<None>', '60 Duro Blue', '65 Duro Dark Blue',
                             '70 Duro Violet', '75 Duro Brown', '80 Duro Green',
                             '85 Duro Gray', '90 Duro Black'],
                            ['<None>', 'DI Water'])
    
    def file_format(self): # (it's a CSV)
        max_q = f"Max Quantity,{self.max_quantity}\n"
        films = "Film," + ",".join(self.film) + "\n"
        pads = "Pad," + ",".join(self.pad) + "\n"
        lube = "Lubricant," + ",".join(self.lubricant) + "\n"
        return f"{max_q}{films}{pads}{lube}"
        
    def write(self):
        if domaille_path():
            try:
                with open(f'{domaille_path()}{os.sep}Settings.txt', 'x') as f:
                    f.write(self.file_format())
            except Exception as e:
                print('FAILED: ', e)
                raise e
            else: print('done.') 
    
    @staticmethod
    def read() -> 'Settings':
        file = f"{domaille_path()}{os.sep}Settings.txt"
        try:
            with open(file, 'r', encoding='ascii') as f:
                settings = f.readlines()
        except Exception as e:
            print('ERROR', e)
            return None
        for line in settings:
        # TODO: read Settings file
            if line.startswith('Max Quantity'):
                quantity = int(line.split(',')[1])
            if line.startswith('Film'):
                films = line.split(',')[1:]
            if line.startswith('Pad'):
                pads = line.split(',')[1:]
            if line.startswith('Lubricant'):
                lubricants = line.split(',')[1:]
        return Settings(quantity, films, pads, lubricants)
    

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
        self.op_code = 300
        self.film = "<None>"
        self.pad = "<None>"
        self.lubricant = "<None>"
        self.description1 = ""
        self.description2 = ""
        self.speed_ramp_dn = 1
        self.pressure_ramp_dn = 1

    def __repr__(self):
        return f"<Step({self.time}s @ {self.pressure}lbs.)>"

    def file_format(self):
        time = f"rRecipeStepTime := {self.time}\n"
        speed = f"rRecipeStepSpeed := {self.speed}\n"
        speed_ramp = f"rRecipeStepSpeedRamp := {self.speed_ramp}\n"
        pressure = f"rRecipeStepPressure := {self.pressure}\n"
        pressure_ramp =f"rRecipeStepPressureRamp := {self.pressure_ramp}\n"
        fci = f"rRecipeStepFCI := {self.fci}\n"
        lower_speed_limit = f"rRecipeStepLowerSpeedLimit := {self.lower_speed_limit}\n"
        upper_speed_limit = f"rRecipeStepUpperSpeedLimit := {self.upper_speed_limit}\n"
        lower_pressure_limit = f"rRecipeStepLowerPressureLimit := {self.lower_pressure_limit}\n"
        upper_pressure_limit = f"rRecipeStepUpperPressureLimit := {self.upper_pressure_limit}\n"
        fixture_weight = f"rRecipeStepFixtureWeight := {self.fixture_weight}\n"
        op_code = f"intRecipeStepOpCode := {self.op_code}\n"
        film = f"strRecipeStepFilm := {self.film}\n"
        lubricant = f"strRecipeStepLubricant := {self.lubricant}\n"
        pad = f"strRecipeStepPad := {self.pad}\n"
        desc1 = f"strRecipeStepDescription1 := {self.description1}\n"
        desc2 = f"strRecipeStepDescription2 := {self.description2}\n"
        speed_ramp_dn = f"rRecipeStepSpeedRampDn := {self.speed_ramp_dn}\n"
        pressure_ramp_dn = f"rRecipeStepPressureRampDn := {self.pressure_ramp_dn}\n"

        return (f"{time}{speed}{speed_ramp}{pressure}{pressure_ramp}"
                f"{fci}{lower_speed_limit}{upper_speed_limit}"
                f"{lower_pressure_limit}{upper_pressure_limit}"
                f"{fixture_weight}{op_code}{film}{lubricant}{pad}"
                f"{desc1}{desc2}{speed_ramp_dn}{pressure_ramp_dn}")
        

class Recipe():
    def __init__(self, description:str, no_of_steps:int = 3, quantity:int = 32, rework_step:int = 1, *steps:RecipeStep):
        no_of_steps = int(no_of_steps)
        self.description = description
        self.no_of_steps = no_of_steps
        self.quantity = quantity
        self.rework_step = rework_step

        self._step = []
        if steps:
           for step in steps:
               self._step.append(step)
        else:            
            for _ in range(no_of_steps):
                self._step.append(RecipeStep())

    def __getitem__(self, index) -> RecipeStep:
        if index == 0:
            return None
        elif index < 0:
            return self._step[index]
        else:
            return self._step[index-1]
  
    def __setitem__(self, index, value:RecipeStep) -> None:
        self._step[index-1] = value

    def __len__(self):
        return len(self._step)
    
    def file_format(self):
        desc = f"strRecipeDescription := {self.description}\n"
        steps = f"intRecipeNoOfSteps := {self.no_of_steps}\n"
        qty = f"intRecipeQty := {self.quantity}\n"
        rework = f"intRecipeReworkStep := {self.rework_step}\n"
        return f"{desc}{steps}{qty}{rework}"
    
    def write(self):
        try:
            with open(f'{domaille_path()}{os.sep}Processes{os.sep}{self.description}', 'w') as f:
                f.write(self.file_format())
            for num, step in enumerate(self):
                if step:
                    with open(f'{domaille_path()}{os.sep}Processes{os.sep}Steps/{self.description}.{num:0>3}', 'w') as f:
                        f.write(self[num].file_format())
        except Exception as e:
            print('FAILED: ', e)
            raise e
        else: print('done.')

    @staticmethod
    def read(name:str) -> 'Recipe':
        # get variables from files and create Recipe()
        file = f"{domaille_path()}{os.sep}Processes{os.sep}{name}"
        try:
            with open(file, 'r', encoding='ascii') as f:
                recipe = f.readlines()
        except Exception as e:
            print('ERROR', e)
            raise e
        for line in recipe:
            if line.startswith('strRecipeDescription'):
                description = line.split(":=")[-1].strip()
            elif line.startswith('intRecipeNoOfSteps'):
                no_of_steps = line.split(":=")[-1].strip()
            elif line.startswith('intRecipeQty'):
                quantity = line.split(":=")[-1].strip()
            elif line.startswith('intRecipeReworkStep'):
                rework_step = line.split(":=")[-1].strip()
        recipe = Recipe(description, no_of_steps, quantity, rework_step)
        for step_number in range(1,recipe.no_of_steps+1):
            try:
                file = f"{domaille_path()}{os.sep}Processes{os.sep}Steps{os.sep}{name}.{step_number:0>3}"
                with open(file, 'r', encoding='ascii') as f:
                    step = f.readlines()
            except Exception as e:
                print('ERROR', e)
                raise e    
            for line in step:
                if line.startswith('rRecipeStepTime '):
                    time = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepSpeed '):
                    speed = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepSpeedRamp '):
                    speed_ramp = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepPressure '):
                    pressure = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepPressureRamp '):
                    pressure_ramp = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepFCI '):
                    fci = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepLowerSpeedLimit '):
                    lower_speed_limit = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepUpperSpeedLimit '):
                    upper_speed_limit = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepLowerPressureLimit '):
                    lower_pressure_limit = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepUpperPressureLimit '):
                    upper_pressure_limit = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepFixtureWeight '):
                    fixture_weight = line.split(":=")[-1].strip()
                if line.startswith('intRecipeStepOpCode '):
                    op_code = line.split(":=")[-1].strip()
                if line.startswith('strRecipeStepFilm '):
                    film = line.split(":=")[-1].strip()
                if line.startswith('strRecipeStepLubricant '):
                    lubricant = line.split(":=")[-1].strip()
                if line.startswith('strRecipeStepPad '):
                    pad = line.split(":=")[-1].strip()
                if line.startswith('strRecipeStepDescription1 '):
                    description1 = line.split(":=")[-1].strip()
                if line.startswith('strRecipeStepDescription2 '):
                    description2 = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepSpeedRampDn '):
                    speed_ramp_dn = line.split(":=")[-1].strip()
                if line.startswith('rRecipeStepPressureRampDn '):
                    pressure_ramp_dn = line.split(":=")[-1].strip()
                    
            recipe[step_number] = RecipeStep(time, pressure)
            recipe[step_number].time = time
            recipe[step_number].speed = speed
            recipe[step_number].speed_ramp = speed_ramp
            recipe[step_number].pressure = pressure
            recipe[step_number].pressure_ramp = pressure_ramp
            recipe[step_number].fci = fci
            recipe[step_number].lower_speed_limit = lower_speed_limit
            recipe[step_number].upper_speed_limit = upper_speed_limit
            recipe[step_number].lower_pressure_limit = lower_pressure_limit
            recipe[step_number].upper_pressure_limit = upper_pressure_limit
            recipe[step_number].fixture_weight = fixture_weight
            recipe[step_number].op_code = op_code
            recipe[step_number].film = film
            recipe[step_number].lubricant = lubricant
            recipe[step_number].pad = pad
            recipe[step_number].description1 = description1
            recipe[step_number].description2 = description2
            recipe[step_number].speed_ramp_dn = speed_ramp_dn
            recipe[step_number].pressure_ramp_dn = pressure_ramp_dn
        return recipe


if __name__=="__main__":

    step1, step2, step3 = RecipeStep(25), RecipeStep(35,12), RecipeStep(75,12)
    recipe = Recipe('test',3,32,1, step1, step2, step3)
    
    print(recipe.file_format())

    for num, step in enumerate(recipe):
        if step:
            print(f"Step {num}")
            print(step.file_format())

    recipe.write()

