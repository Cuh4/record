# // ---------------------------------------------------------------------
# // ------- [Record] Title Bar Control
# // ---------------------------------------------------------------------

# // ---- Imports
import flet

import modules

# // ---- Main
class control(flet.UserControl):
    # // init
    def __init__(self, page: flet.Page, name: str, iconSize: int = 15, height: int = 25):
        # // setup
        # init
        super().__init__()
        
        # // attributes
        # main
        self.page = page
        self.name = name

        self.iconSize = iconSize
        self.height = height
    
    # // ui
    def build(self):
        # // controls
        self.title = flet.Text(
            value = self.page.title,
            font_family = "Montserrat",
            text_align = flet.TextAlign.LEFT
        )
        
        self.minimizeButton = flet.IconButton(
            icon = flet.icons.HORIZONTAL_RULE_ROUNDED,
            icon_color = flet.colors.WHITE,
            icon_size = self.iconSize,
            
            on_click = self.minimizeButton_onClick
        )

        self.topMostButton = flet.IconButton(
            icon = flet.icons.ARROW_UPWARD_ROUNDED,
            icon_color = flet.colors.ORANGE,
            icon_size = self.iconSize,

            on_click = self.topMostButton_onClick
        )
        
        self.closeButton = flet.IconButton(
            icon = flet.icons.CLOSE_ROUNDED,
            icon_color = flet.colors.RED,
            icon_size = self.iconSize,
            
            on_click = self.closeButton_onClick
        )
        
        # // main
        # finalization
        return flet.WindowDragArea(
            content = flet.Container(
                content = flet.Row(
                    controls = [
                        # title (first half)
                        flet.Text(
                            value = self.name,
                            font_family = "Montserrat",
                            text_align = flet.TextAlign.LEFT
                        ),
                        
                        # buttons (second half)
                        flet.Row(
                            controls = [
                                self.minimizeButton,
                                self.topMostButton,
                                self.closeButton
                            ],
                        )
                    ],
                    
                    expand = True,
                    alignment = flet.MainAxisAlignment.SPACE_BETWEEN
                ),

                bgcolor = modules.helpers.RGBToHex(15, 15, 15),
                expand = True
            ),
            
            height = self.height,
            expand = True
        )
        
    # // functionality
    def minimizeButton_onClick(self, _):
        self.page.window_minimized = True
        self.page.update()
    
    def closeButton_onClick(self, _):
        self.page.window_close() # purely destroys gui and all flet stuffs
        exit(0) # destroys threads
    
    def topMostButton_onClick(self, _):
        # update page top-most
        self.page.window_always_on_top = not self.page.window_always_on_top
        self.page.update()
        
        # update button
        self.topMostButton.icon_color = flet.colors.BLUE if self.page.window_always_on_top else flet.colors.ORANGE
        self.topMostButton.update()