# // ---------------------------------------------------------------------
# // ------- [Record] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import flet

import controls
import modules

# // ---- Main
# // Function to render the app
def mainApp(page: flet.Page):
    # // set page properties
    # window size
    page.window_height = 65
    page.window_width = 500
    
    page.window_min_height = page.window_height
    page.window_min_width = page.window_width
    
    page.window_max_height = page.window_height
    page.window_max_width = page.window_width
    
    # window properties
    page.window_resizable = False
    
    page.window_frameless = True
    page.window_title_bar_hidden = True

    # page layout
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    
    # page appearance
    page.title = "Record"
    page.bgcolor = modules.helpers.RGBToHex(245, 245, 245)
    
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
        videoCodec = "mp4v",
        videoFileExtension = "mp4",
        folderPath = "videos"
    )
    
    # titlebar
    titleBar = controls.titleBar(
        page = page,
        name = page.title,
        iconSize = 10,
        height = 22
    )
    
    # finalization
    page.add(
        flet.Column(
            controls = [
                titleBar,
                recordControl
            ],
            
            expand = True,
            alignment = flet.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment = flet.CrossAxisAlignment.START
        )
    )
    
# // Start app
flet.app(
    target = mainApp,
    name = "Record",
    assets_dir = modules.helpers.path("assets")
)