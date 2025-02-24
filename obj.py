import os   # for file operations

class Dommaile():
    """Manages polishing system settings, recipes and file operations.
    
    The main class for interacting with polishing recipes and settings.
    Creates and manages a directory structure for storing configuration.
    
    Usage:
        >>> domaille = Dommaile()  # Create with default settings
        >>> domaille.create_path("C:/MyPolishingData")  # Set up directory structure
        >>> recipe = Recipe("test", 3, 32, 1)  # Create a new recipe
        >>> domaille.recipes.append(recipe)  # Add recipe
        >>> domaille.write()  # Save everything to disk
    """
    
    def __init__(self, *args, path:'Path' = None, settings:'Settings' = None, 
                 recipes:'RecipeList' = None):
        """Initialize Domaille with optional path, settings and recipes.
        
        Args:
            path (Path, optional): Directory path for data storage
            settings (Settings, optional): Settings object, defaults to Settings.default()
            recipes (RecipeList, optional): List of recipes, defaults to empty list
        """
        
        if not path:
            self._path = path = Path(os.getcwd())
        elif not os.path.isdir(str(path)):
            self._path = path = Path(os.getcwd())

        
        if isinstance(path, Path):
            print(' Dommaile.__init__(path:Path)')
            self._path = path
        elif isinstance(path, str): 
            print(' Dommaile.__init__(path:str)')
            self._path = Path(path)
        else:
            print("Path must be a string or Path object")
            print(f"type(path): {type(path)}")
            print(f"path: {path}")
        
        if not settings:
            self._settings = Settings.default()
        else:
            self._settings = settings
        
        if not recipes:
            self._recipes = RecipeList()
        else:
            self._recipes = RecipeList(recipes)


    def create_path(self, directory:'Path'=os.getcwd()) -> 'Path':
        """Creates the Domaille directory structure in specified location.
        
        Creates 'Domaille/Processes/Steps' folders hierarchy.
        
        Args:
            directory (str): Parent directory to create structure in
            
        Returns:
            Path: Path to parent of Domaille directory, or None if failed
            
        Usage:
            >>> domaille.create_path("E:/")
            'E:/'  
        """
        domaille_dir = f"{directory}{os.sep}Domaille"
        steps_dir = f"{domaille_dir}{os.sep}Processes{os.sep}Steps"
        if not os.path.isdir(directory):
            print(f"Invalid directory: {directory}")
            return self._path
        if not os.path.isdir(steps_dir):
            try:
                os.makedirs(steps_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating directories: {e}")
                return None
    
        self._path = Path(directory)
        return self._path
            
    @property
    def path(self) -> str: 
        # return the _path, but also verify that it exists
        # if it doesn't exist, return None
        if self._path and os.path.isdir(self._path):
            return self._path
        else:
            return os.getcwd()
    @path.setter
    def path(self, path:str):
        # checks a path to see if it's a directory,
        # normalizes path to parent directory of Domaille folder
        if os.path.isdir(str(path)):
            parts = path.split('Domaille')
            if len(parts) > 1:
                # If Domaille is in the path, use everything before it
                path = parts[0].rstrip(os.sep)
            self._path = path
        else:
            print(f"Invalid path: {path}")
            self._path = None
    
            
    @property
    def settings(self) -> 'Settings':
        return self._settings
    @settings.setter
    def settings(self, settings:'Settings'):
        if isinstance(settings, Settings):
            self._settings = settings
        else:
            raise TypeError("Settings must be a Settings object")
        
    def create_settings(self, directory:str):
        '''creates a new settings file in the Domaille directory'''
        
        settings = Settings.default()
        settings.write(directory)
        self._settings = settings
        return settings
    
    @property
    def recipes(self) -> 'RecipeList':
        return self._recipes
    @recipes.setter
    def recipes(self, recipes:'RecipeList'):
        if isinstance(recipes, RecipeList):
            self._recipes = recipes
        elif isinstance(recipes, list):
            if all(isinstance(recipe, Recipe) for recipe in recipes):
                self._recipes = RecipeList(recipes)
        elif isinstance(recipes, Recipe):
            self._recipes = RecipeList([recipes])
        else:
            raise TypeError("Recipes must be in a list or RecipeList object")

    def create_recipes(self, directory:str):
        '''reads all files in the Processes directory and creates Recipe objects'''
        recipes = RecipeList()
        recipes.read(f"{directory}{os.sep}Processes")
        if not recipes:
            recipe=Recipe('default',3,32,2, RecipeStep(), RecipeStep(), RecipeStep())
            recipes.append(recipe)
            recipe.write(directory)

        self._recipes = recipes
        return recipes  

    def write(self, path:'Path' = None):
        '''writes the Domaille object to the specified path'''
        if not path:
            path = self.path
            self.path = Path(path)
        self.path.write(path)
        self.settings.write(path)
        self.recipes.write(path)

    def read(self, directory:'Path' = None):
        '''reads the Domaille directory contents'''
        if not directory:
            directory = self.path      
        if not os.path.isdir(directory):
            print(f"Invalid directory: {directory}")
            return None
        self.path = Path.read(directory)
        self.settings = Settings.read(directory)
        # Initialize RecipeList with directory path
        self._recipes = RecipeList(directory)
        return self
            
    @staticmethod
    def wipe(directory:str) -> bool:
        ''' wipes the Domaille directory and all contents
            returns True if successful, False if failed
        '''
        if not os.path.isdir(directory):
            print(f"Invalid directory: {directory}")
            return False
        
        if directory.endswith('Domaille'):
            directory = directory.rstrip('Domaille').rstrip(os.sep)

        if not os.path.isdir(f"{directory}{os.sep}Domaille"):
            print(f"Domaille directory not found: {directory}")
            return True # nothing to delete
        
        try:
            domaille_path = f"{directory}{os.sep}Domaille"
            for root, dirs, files in os.walk(domaille_path, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception as e:
                        print(f"Error deleting directory: {e}")
                os.rmdir(domaille_path)
            return True
        except Exception as e:
            print(f"Error deleting directory: {e}")
            return False


class Path(str):
    """Enhanced string class for handling filesystem paths.
    
    Extends str with path validation and Domaille-specific operations.
    
    Usage:
        >>> path = Path("C:/MyData")
        >>> str(path)  # Get string representation
        'C:/MyData'
    """
    def __init__(self, path:str=os.getcwd()):
        super().__init__()
        # set the value of the string to the path
        if isinstance(path, Path):
            self._path = path
        elif os.path.isdir(path):
            self._path = path
        else:
            print(f"Invalid Path in Path init: {path}")
            self._path = os.getcwd()

    def __str__(self):
        return self._path

    # setter:
    def __set__(self, path:str):
        if os.path.isdir(path):
            super().__init__(path)
            self._path = path

        else:
            print(f"Invalid path in Path setter: {path}")
            self._path = os.getcwd()

    # getter:
    def __get__(self):
        return self._path
    
    def write(self, path:str):
        try:
            os.makedirs(f"{path}{os.sep}Domaille{os.sep}Processes{os.sep}Steps", exist_ok=True)
            return True
        except Exception as e:
            print('FAILED: ', e)
            return False
        
    def read(self, path:str=None) -> str:
        # check for presence of Domaille directory, return parent directory
        # or none if not found
        if os.path.isdir(f"{path}{os.sep}Domaille{os.sep}Processes{os.sep}Steps"):
            return path
        else:
            return None
        


class Settings():
    """Manages polishing system settings.
    
    Handles configuration for films, pads, lubricants and quantity limits.
    
    Usage:
        >>> settings = Settings.default()  # Create with defaults
        >>> settings.max_quantity = 64  # Modify settings
        >>> settings.write("C:/MyData")  # Save to disk
    """
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
        
    def write(self, directory:str):
        try:
            with open(f'{directory}{os.sep}Domaille{os.sep}Settings.txt', 'w') as f:
                f.write(self.file_format())
        except Exception as e:
            print('FAILED: ', e)
            raise e
        else: print('done.') 


    @staticmethod
    def read(path=os.getcwd()) -> 'Settings':
        if not os.path.isdir(path):
            print(f"Invalid directory: {path}")
            path

        file = f"{path}{os.sep}Domaille{os.sep}Settings.txt"
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
            elif line.startswith('Film'):
                films = [film.strip() for film in line.split(',')[1:]]
            elif line.startswith('Pad'):
                pads = [pad.strip() for pad in line.split(',')[1:]]
            elif line.startswith('Lubricant'):
                lubricants = [lube.strip() for lube in line.split(',')[1:]]
        return Settings(quantity, films, pads, lubricants)
    

class RecipeStep():
    """Represents a single step in a polishing recipe.
    
    Contains all parameters for one polishing operation step.
    
    Usage:
        >>> step = RecipeStep(time=45, pressure=12)
        >>> step.speed = 120
        >>> step.film = "Brown 5um"
    """
    def __init__(self, time=75, pressure=16, **kwargs):
        """Initialize a recipe step.
        
        Args:
            time (int): Duration in seconds
            pressure (int): Pressure in lbs.
            **kwargs: Additional step parameters
        """
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
        for k,v in kwargs.items():
            setattr(self, k, v)
            

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
        
   
  
class RecipeList(list):
    """Maintains a list of Recipe objects with type checking.
    
    Only allows Recipe objects to be added. Can load/save from directory.
    
    Usage:
        >>> recipes = RecipeList()
        >>> recipes.append(Recipe("test"))  # Add single recipe
        >>> recipes.read("C:/MyData")  # Load all recipes from disk
    """
    def __init__(self, input=None):
        super().__init__()
        if isinstance(input, Recipe):
            self.append(input)
        elif isinstance(input, list):
            for recipe in input:
                self.append(recipe)
        elif isinstance(input, str) or isinstance(input, Path):
            # If initialized with a path, read recipes from that directory
            self.read(input)
    
    def append(self, item):
        if not isinstance(item, Recipe):
            raise TypeError("Can only add Recipe objects")
        super().append(item)
        
    def extend(self, items):
        if not all(isinstance(item, Recipe) for item in items):
            raise TypeError("Can only add Recipe objects")
        super().extend(items)
        
    def __setitem__(self, index, item):
        if not isinstance(item, Recipe):
            raise TypeError("Can only add Recipe objects")
        super().__setitem__(index, item)

    def write(self, directory):
        for recipe in self:
            recipe.write(directory)
    
    def read(self, directory):
        # read all files in Processes directory
        process_dir = f"{directory}{os.sep}Domaille{os.sep}Processes"
        if not os.path.isdir(process_dir):
            return self
            
        
        for file in os.listdir(process_dir):
            try:
                if os.path.isfile(os.path.sep.join([process_dir, file])):
                    recipe = Recipe.read(file, directory)
                    if recipe:
                        self.append(recipe)
            except Exception as e:
                print(f"Error reading recipes: {e}"
                      f"\nFile: {file}")

class Recipe():
    """Represents a complete polishing recipe with multiple steps.
    
    Contains recipe metadata and ordered list of RecipeStep objects.
    
    Usage:
        >>> recipe = Recipe("MyRecipe", no_of_steps=3)
        >>> recipe[1] = RecipeStep(45, 12)  # Set first step
        >>> recipe.write("C:/MyData")  # Save to disk
    """
    def __init__(self, description:str, no_of_steps:int = 3, 
                 quantity:int = 32, rework_step:int = 1, *steps:RecipeStep):
        """Initialize a new recipe.
        
        Args:
            description (str): Recipe name/description
            no_of_steps (int): Number of polishing steps
            quantity (int): Default batch quantity
            rework_step (int): Step to return to for rework
            *steps (RecipeStep): Initial step definitions
        """
        no_of_steps = int(no_of_steps)
        self.description = description
        self.no_of_steps = 3 # default to 3 steps
        self.quantity = quantity
        self.rework_step = rework_step

        self._steps = []
        if steps:
           for step in steps:
               self._steps.append(step)
        else:            
            for _ in range(no_of_steps):
                self._steps.append(RecipeStep())

    def __repr__(self): 
        return f"<Recipe({self.description}, {self.no_of_steps} steps)>"
    
    def append(self, step:RecipeStep):
        self._steps.append(step)


    def __getitem__(self, index) -> RecipeStep:
        if index == 0:
            return None
        elif index < 0:
            return self._steps[index]
        elif index > len(self._steps):
            return None
        else:
            return self._steps[index-1]
  
    def __setitem__(self, index, value:RecipeStep) -> None:
        self._steps[index-1] = value

    def __iter__(self):
        return iter(self._steps)

    def __len__(self):
        return len(self._steps)
    
    def file_format(self):
        desc = f"strRecipeDescription := {self.description}\n"
        steps = f"intRecipeNoOfSteps := {self.no_of_steps}\n"
        qty = f"intRecipeQty := {self.quantity}\n"
        rework = f"intRecipeReworkStep := {self.rework_step}\n"
        return f"{desc}{steps}{qty}{rework}"
    
    def write(self, directory):
        process_dir = f"{directory}{os.sep}Domaille{os.sep}Processes"
        steps_dir = f"{process_dir}{os.sep}Steps"
        try:
            os.makedirs(steps_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directories: {e}")
            return False

        try:
            with open(f'{process_dir}{os.sep}{self.description}', 'w') as f:
                f.write(self.file_format())
            for num, step in enumerate(self, start=1):
                if step:
                    with open(f'{steps_dir}{os.sep}{self.description}.{num:0>3}', 'w') as f:
                        f.write(self[num].file_format())
        except Exception as e:
            print('FAILED: ', e)
            raise e
        else: 
            print(f'{self.description} written to {process_dir}')

    @staticmethod
    def read(name:str, directory) -> 'Recipe':
        """Load a recipe from disk.
        
        Args:
            name (str): Recipe name/filename
            directory (str): Directory containing recipe files
            
        Returns:
            Recipe: Loaded recipe object or None if failed
            
        Usage:
            >>> recipe = Recipe.read("MyRecipe", "C:/MyData")
        """
        # get variables from files and create Recipe()
        file = f"{directory}{os.sep}Domaille{os.sep}Processes{os.sep}{name}"
        try:
            with open(file, 'r', encoding='ascii') as f:
                recipe = f.readlines()
        except FileNotFoundError as e:
            print('File not found:', file)
            return None
        except PermissionError as e:
            print('Permission denied:', file)
            return None
        except IOError as e:
            print('IO error reading file:', file)
            return None
        except UnicodeDecodeError as e:
            print('Invalid file encoding:', file)
            return None
        except Exception as e:
            print('ERROR', e)
            return None
    
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
                file = f"{directory}{os.sep}Domaille{os.sep}Processes{os.sep}Steps{os.sep}{name}.{step_number:0>3}"
                with open(file, 'r', encoding='ascii') as f:
                    step = f.readlines()
            except Exception as e:
                print('ERROR', e)
                print('File:', file)
                print('this needs a better exception block, in some cases '
                      'it should not be an issue and just pass through')
                raise e    
            for line in step:
                if line.startswith('rRecipeStepTime '):
                    time = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepSpeed '):
                    speed = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepSpeedRamp '):
                    speed_ramp = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepPressure '):
                    pressure = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepPressureRamp '):
                    pressure_ramp = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepFCI '):
                    fci = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepLowerSpeedLimit '):
                    lower_speed_limit = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepUpperSpeedLimit '):
                    upper_speed_limit = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepLowerPressureLimit '):
                    lower_pressure_limit = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepUpperPressureLimit '):
                    upper_pressure_limit = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepFixtureWeight '):
                    fixture_weight = line.split(":=")[-1].strip()
                elif line.startswith('intRecipeStepOpCode '):
                    op_code = line.split(":=")[-1].strip()
                elif line.startswith('strRecipeStepFilm '):
                    film = line.split(":=")[-1].strip()
                elif line.startswith('strRecipeStepLubricant '):
                    lubricant = line.split(":=")[-1].strip()
                elif line.startswith('strRecipeStepPad '):
                    pad = line.split(":=")[-1].strip()
                elif line.startswith('strRecipeStepDescription1 '):
                    description1 = line.split(":=")[-1].strip()
                elif line.startswith('strRecipeStepDescription2 '):
                    description2 = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepSpeedRampDn '):
                    speed_ramp_dn = line.split(":=")[-1].strip()
                elif line.startswith('rRecipeStepPressureRampDn '):
                    pressure_ramp_dn = line.split(":=")[-1].strip()
                else:
                    print(f"Unknown setting in {step}:") 
                    print(line)

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
    step1, step2, step3 = RecipeStep(45), RecipeStep(45,12), RecipeStep(75,12)
    recipe = Recipe('test23',3,32,1, step1, step2, step3)
   
    cwd = os.getcwd()
    dir = cwd 
    # dir = 'c:\\Users\\giles\\Documents\\test'
    
    domaille = Dommaile()
    # domaille.recipes.append(recipe)

    os.makedirs(dir, exist_ok=True)
    
    domaille.recipes.append(Recipe('default',3,32,2, RecipeStep(), RecipeStep(), RecipeStep()))
    
    print(domaille.recipes)

    domaille.read()
    
    print(domaille.recipes)
    


