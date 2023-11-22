# // ---------------------------------------------------------------------
# // ------- [Record] Build
# // ---------------------------------------------------------------------

# // ---- Imports
import os

# // ---- Variables
fileName = "main.py"
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
def format(name: str, values: list[str], ending: str = "", wrapInQuotes: bool = False):
    new = []
    quote = "\"" if wrapInQuotes else ""
    
    for value in values:
        new.append(f"--{name} {quote}{value}{ending}{quote}")
        
    return tuple(new)

# // ---- Main
newExclusions = format("exclude", exclusions, wrapInQuotes = True)
newData = format("add-data", data, ";.", True)

os.system(
    # appearance
    " ".join([
        "PyInstaller",
        fileName,
        
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
    ])
)

#py -m PyInstaller main.py --name "Record" --icon "assets/imgs/favicon.png" --onefile --noconsole --add-data "assets/fonts/Montserrat-Black.ttf;." --add-data "assets/fonts/Montserrat-Bold.ttf;." --add-data "assets/fonts/Montserrat-Regular.ttf;." --exclude websockets --exclude pandas --exclude jinja --exclude PIL