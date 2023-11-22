# // ---------------------------------------------------------------------
# // ------- [Record] Build
# // ---------------------------------------------------------------------

# // ---- Imports
from PyInstaller import __main__ as PyInstaller

# // ---- Variables
name = "Record"

icon = "assets/imgs/favicon.png"

exclusions = [
    "websockets",
    "jinja",
    "pandas",
    "PIL"
]

data = [
    "assets/fonts/Montserrat-Black.ttf",
    "assets/fonts/Montserrat-Bold.ttf",
    "assets/fonts/Montserrat-Regular.ttf"
]

# // ---- Functions
def format(name: str, values: list[str], ending: str = ""):
    new = []
    
    for value in values:
        new.append(f"--{name} {value}{ending}")
        
    return tuple(new)

# // ---- Main
newExclusions = format("exclude", exclusions)
newData = format("add-data", data, ";.")

PyInstaller.run(
    # appearance
    "--name",
    name,
    
    "--icon",
    icon,
    
    # configuration
    "--onefile",
    "--noconsole",
    
    # exclusions
    *newExclusions,
    
    # data
    *newData
)

#py -m PyInstaller main.py --name "Record" --icon "assets/imgs/favicon.png" --onefile --noconsole --add-data "assets/fonts/Montserrat-Black.ttf;." --add-data "assets/fonts/Montserrat-Bold.ttf;." --add-data "assets/fonts/Montserrat-Regular.ttf;." --exclude websockets --exclude pandas --exclude jinja --exclude PIL