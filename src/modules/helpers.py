# // ---------------------------------------------------------------------
# // ------- [Record] Helpers Module
# // ---------------------------------------------------------------------

# // ---- Imports
import sys
import os

# // ---- Functions
def RGBToHex(r: float|int = 255, g: float|int = 255, b: float|int = 255):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def pathSafeName(name: str):
    return name.replace("\\", "").replace("/", "")

def path(relative_path: str): # https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    try:
        base_path = sys._MEIPASS # temp folder where assets are stored. this folder is created by pyinstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def isBuiltApplication() -> bool:
    try:
        return sys._MEIPASS != None
    except Exception:
        return False