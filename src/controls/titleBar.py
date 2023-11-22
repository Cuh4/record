# // ---------------------------------------------------------------------
# // ------- [Record] Title Bar Control
# // ---------------------------------------------------------------------

# // ---- Imports
import flet

import modules

# // ---- Main
class control(flet.UserControl):
    # // init
    def __init__(self, name: str, page: flet.Page, iconSize: int = 15, height: int = 25):
        # // setup
        # init
        super().__init__()
        
        # // attributes
        # main
        self.name = name
        self.page = page

        self.iconSize = iconSize
        self.height = height
    
    # // ui
    def build(self):
        # // controls
        # top most button
        self.topMostButton = flet.IconButton(
            icon = flet.icons.ARROW_UPWARD_ROUNDED,
            icon_color = flet.colors.ORANGE,
            on_click = self.topMostButton_onClick,
            icon_size = self.iconSize
        )
        
        # // main
        # finalization
        return flet.Container(
            content = flet.WindowDragArea(
                content = flet.Row(
                    controls = [
                        # first half of title bar (left)
                        flet.Container(
                            content = flet.Text(
                                value = self.name,
                                text_align = flet.TextAlign.LEFT,
                                font_family = "MontserratBlack"
                            ),
                            
                            padding = flet.padding.only(7),
                            expand = True
                        ),
                        
                        # second half of title bar (right)
                        flet.Container(
                            content = flet.Row(
                                controls = [
                                    # minimize button
                                    flet.IconButton(
                                        icon = flet.icons.HORIZONTAL_RULE_ROUNDED,
                                        icon_color = flet.colors.GREEN_ACCENT,
                                        on_click = self.minimizeButton_onClick,
                                        icon_size = self.iconSize
                                    ),

                                    # top-most button
                                    self.topMostButton,

                                    # close button
                                    flet.IconButton(
                                        icon = flet.icons.CLOSE_ROUNDED,
                                        icon_color = flet.colors.RED,
                                        on_click = self.closeButton_onClick,
                                        icon_size = self.iconSize
                                    )
                                ],
                                
                                alignment = flet.MainAxisAlignment.END,
                                spacing = 3
                            ),
                            
                            padding = flet.padding.only(right = 7),
                            expand = True
                        )
                    ],
                    
                    alignment = flet.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment = flet.CrossAxisAlignment.CENTER
                ),

                expand = True,
                maximizable = False
            ),
            
            height = self.height,
            expand = True,
            bgcolor = flet.colors.BLACK38
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