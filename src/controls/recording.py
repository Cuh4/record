# // ---------------------------------------------------------------------
# // ------- [Record] Recording Control
# // ---------------------------------------------------------------------

# // ---- Imports
import flet
from flet_core import alignment
import datetime
import os
import pathlib
from screeninfo import get_monitors
import time
import win10toast_click as win10toast
import threading

import modules

# // ---- Main
class control(flet.UserControl):
    # // init
    def __init__(self, page: flet.Page, defaultVideoFileName: str = "unnamed", videoCodec: str = "mp4v", videoFileExtension: str = "mp4", folderPath: str = ""):
        # // setup
        # init
        super().__init__()
        
        # create path if it doesnt exist
        pathlib.Path(folderPath).mkdir(parents = True, exist_ok = True)
        
        # // attributes
        # paths, names, etc
        self.videoFileName = defaultVideoFileName
        self.folderPath = os.path.abspath(folderPath)
        
        self.videoFileExtension = videoFileExtension
        self.videoCodec = videoCodec
        
        self.monitors = get_monitors()

        # video
        self.recording = False
        self.elapsedSeconds = 0
        self.fps = 60
        
        self.targetMonitor = self.monitors[0]
        self.targetMonitorID = 0

        # other
        self.page = page

    # // ui
    def build(self):    
        # // controls
        # video file name input
        self.videoFileNameInput = flet.TextField(
            border_color = flet.colors.WHITE,
            tooltip = "Video Name",
            hint_text = "Video Name",

            text_style = flet.TextStyle(
                size = 14,
                font_family = "Montserrat"
            ),
            
            on_change = self.videoFileNameInput_onChange
        )
        
        # recording button
        self.recordingButton = flet.OutlinedButton(
            text = "Record",

            icon = flet.icons.CIRCLE_ROUNDED,
            icon_color = flet.colors.RED,

            on_click = self.recordingButton_onClick
        )
        
        # open folder button
        self.openFolderButton = flet.OutlinedButton(
            text = "Open Folder",
            
            icon = flet.icons.FOLDER_COPY_ROUNDED,
            icon_color = flet.colors.ORANGE_400,

            on_click = self.folder_onClick
        )
        
        # timer text
        self.timerText = flet.Text(
            value = self.timerFormatted(),
            font_family = "Montserrat"
        )
        
        # choose monitor menu button
        self.chooseMonitorButton = flet.OutlinedButton(
            text = "Choose Monitor",

            icon = flet.icons.MONITOR_ROUNDED,
            icon_color = flet.colors.WHITE,
            
            on_click = lambda _: self.toggleDrawer()
        )
        
        # fps slider
        self.fpsSlider = flet.Slider(
            label = "{value} FPS",

            min = 5,
            max = 60,
            divisions = self.fps,
            value = self.fps,
            
            active_color = flet.colors.BLUE_300,
            thumb_color = flet.colors.WHITE,
            scale = 0.8,
            
            on_change = self.fpsSlider_onChange
        )
        
        # // main
        # finalization
        return flet.Container(
            content = flet.Column(
                controls = [
                    flet.Row(
                        controls = [
                            self.videoFileNameInput
                        ],
                        
                        alignment = flet.MainAxisAlignment.CENTER,
                        vertical_alignment = flet.CrossAxisAlignment.CENTER
                    ),
                    
                    flet.Row(
                        controls = [
                            self.timerText,
                            self.fpsSlider
                        ],
                        
                        alignment = flet.MainAxisAlignment.CENTER
                    ),
                    
                    flet.Divider(
                        thickness = 2,
                        color = flet.colors.WHITE
                    ),
                    
                    flet.Row(
                        controls = [
                            self.recordingButton,
                            self.openFolderButton,
                            self.chooseMonitorButton
                        ],
                    
                        alignment = flet.MainAxisAlignment.CENTER,
                        vertical_alignment = flet.CrossAxisAlignment.CENTER
                    )
                ],
                
                expand = True,
                alignment = flet.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment = flet.CrossAxisAlignment.CENTER,
                spacing = 0.2,
                scale = 0.85
            ),

            expand = True
        )
        
    # // functionality
    # setup stuffs
    def setupNavigationDrawer(self):
        self.page.drawer = flet.NavigationDrawer(
            controls = [
                flet.Container(height = 15),
                *[flet.NavigationDrawerDestination(icon = flet.icons.MONITOR_ROUNDED, selected_icon = flet.icons.CHECK_BOX_ROUNDED, label = f"{monitor.name} ({monitorID})") for monitorID, monitor in enumerate(self.monitors)]
            ],
            on_change = self.navigationDrawer_onChange,
            
            surface_tint_color = flet.colors.BLACK,
            indicator_color = flet.colors.ORANGE
        )
    
    # helpers
    def timerFormatted(self):
        time = datetime.timedelta(seconds = int(self.elapsedSeconds))
        time = str(time)

        return f"{time} @ {self.fps} FPS"
    
    def showDrawer(self):
        self.page.drawer.open = True
        self.page.drawer.update()   
        
    def hideDrawer(self):
        self.page.drawer.open = False
        self.page.drawer.update()   
        
    def toggleDrawer(self):
        self.page.drawer.open = not self.page.drawer.open
        self.page.drawer.update()  

    def openRecordResultFolder(self):
        os.startfile(f"{self.folderPath}")
        
    def notify(self, text: str, duration: int = 5):
        toast = win10toast.ToastNotifier()

        toast.show_toast(
            title = self.page.title,
            msg = text,
            duration = duration,
            threaded = True,
            callback_on_click = lambda: self.openRecordResultFolder()
        )
    
    def changeFileName(self, newFileName: str):
        self.videoFileName = modules.helpers.pathSafeName(newFileName)
    
    # control updates
    def updateTimerText(self):
        self.timerText.value = self.timerFormatted()
        self.timerText.update()
    
    # control callbacks  
    def navigationDrawer_onChange(self, _):
        chosenID = self.page.drawer.selected_index or 0

        self.targetMonitorID = int(chosenID)
        self.targetMonitor = self.monitors[self.targetMonitorID]
      
    def videoFileNameInput_onChange(self, _):
        # get new video filename
        value = self.videoFileNameInput.value or ""
        
        # enforce character limit
        if len(value) > 15:
            value = value[:15]
            
            self.videoFileNameInput.value = value
            self.videoFileNameInput.update()

        # change video filename to the desired filename
        self.changeFileName(value)
        
    def fpsSlider_onChange(self, _):
        # update fps attribute
        self.fps = int(self.fpsSlider.value)
        
        # update visuals
        self.updateTimerText()
    
    def recordingButton_onClick(self, _):
        # // functionality
        # start/stop recording
        if self.recording:
            # stop recording
            self.stopRecording()
        else:
            # start recording
            self.record()
        
        # // visuals
        # change icons depending on recording state
        if self.recording:
            # change icon of recording button
            self.recordingButton.icon = flet.icons.STOP_ROUNDED
            self.recordingButton.icon_color = flet.colors.GREEN
        else:
            # change icon of recording button
            self.recordingButton.icon = flet.icons.CIRCLE_ROUNDED
            self.recordingButton.icon_color = flet.colors.RED
            
        # disable controls depending on recording state
        self.videoFileNameInput.disabled = self.recording
        self.fpsSlider.disabled = self.recording
        self.chooseMonitorButton.disabled = self.recording
            
        # update
        self.videoFileNameInput.update()
        self.fpsSlider.update()
        self.chooseMonitorButton.update()
        self.recordingButton.update()
        
    def folder_onClick(self, _):
        # open folder
        self.openRecordResultFolder()
        
    # recording
    def record(self):
        # set state
        self.recording = True

        # record screen
        self.recorder = modules.recorder(
            fileName = self.videoFileName,
            resolution = (self.targetMonitor.width, self.targetMonitor.height),
            codec = self.videoCodec, 
            fileExtension = self.videoFileExtension,
            outputFolderPath = self.folderPath,
            fps = self.fps
        )

        self.recorder.startRecording(self.targetMonitorID + 1)
        
        # increase timer text
        def increaseTimer():
            while True:
                if not self.recording:
                    break
                
                # increase elapsed seconds
                self.elapsedSeconds += 1
                self.updateTimerText()
                
                # wait a second
                time.sleep(1)
                
        threading.Thread(
            target = increaseTimer
        ).start()
            
    def stopRecording(self):
        # set state
        self.recording = False
        
        # release stuffs
        self.recorder.endRecording()
        
        # reset elapsed seconds
        self.elapsedSeconds = 0
        self.updateTimerText()
        
        # notify user
        self.notify(f"Your recording has finished.\nClick here to open the folder containing the video.")