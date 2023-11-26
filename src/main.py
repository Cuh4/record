# // ---------------------------------------------------------------------
# // ------- [Record] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import flet
import math

import controls
import modules

# // ---- Main
# // Function to render the app
def mainApp(page: flet.Page):
    # // set page properties
    # window size
    page.window_height = 45
    page.window_width = 400
    
    page.window_min_height = page.window_height
    page.window_min_width = page.window_width
    
    page.window_max_height = page.window_height
    page.window_max_width = page.window_width
    
    # window properties
    page.window_resizable = False
    
    page.window_frameless = True
    page.window_title_bar_hidden = True
    
    page.window_always_on_top = True

    # page layout
    page.padding = 0
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    
    # page appearance
    page.title = "Record"
    page.bgcolor = modules.helpers.RGBToHex(15, 15, 15)
    
    
    # fonts
    page.fonts = {
        "Montserrat" : "fonts/MontSerrat-Regular.ttf",
        "MontserratBold" : "fonts/MontSerrat-Bold.ttf",
        "MontserratBlack" : "fonts/MontSerrat-Black.ttf"
    }
    
    # // app controls
    # recording control
    recordControl = controls.recording(
        page = page,
        defaultVideoFileName = "unnamed",
        videoCodec = "mp4v",
        videoFileExtension = "mp4",
        folderPath = "videos"
    )
    
    recordControl.setupNavigationDrawer()
    
    # finalization
    page.add(
        flet.Stack(
            controls = [
                # background
                flet.Container(
                    # background gradient
                    gradient = flet.LinearGradient(
                        colors = [
                            modules.helpers.RGBToHex(25, 12, 0),
                            modules.helpers.RGBToHex(0, 0, 12)
                        ],
                        
                        rotation = math.radians(35)
                    ),

                    expand = True
                ),
                
                # main app
                recordControl
            ],
            
            expand = True
        )
    )
    
# // Start app
flet.app(
    target = mainApp,
    name = "Record",
    assets_dir = modules.helpers.getWorkingDirectory() if modules.helpers.isBuiltApplication() else "assets"
)