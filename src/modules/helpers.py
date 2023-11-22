# // ---------------------------------------------------------------------
# // ------- [Record] Helpers Module
# // ---------------------------------------------------------------------

# // ---- Functions
def RGBToHex(r: float|int = 255, g: float|int = 255, b: float|int = 255):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def pathSafeName(name: str):
    return name.replace("\\", "").replace("/", "")