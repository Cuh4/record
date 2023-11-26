# // ---------------------------------------------------------------------
# // ------- [Record] Recording Control
# // ---------------------------------------------------------------------

# // ---- Imports
import flet
import datetime
import os
import pathlib
import screeninfo
import time
import win10toast_click as win10toast
import threading
from uuid import uuid4

import modules

# // ---- Main
class control(flet.UserControl):
    # // init
    def __init__(self, page: flet.Page, videoCodec: str = "mp4v", videoFileExtension: str = "mp4", folderPath: str = ""):
        # // setup
        # init
        super().__init__()
        
        # create path if it doesnt exist
        pathlib.Path(folderPath).mkdir(parents = True, exist_ok = True)
        
        # // attributes
        # paths, names, etc
        self.folderPath = os.path.abspath(folderPath)
        
        self.videoFileExtension = videoFileExtension
        self.videoCodec = videoCodec
        
        self.monitors = screeninfo.get_monitors()

        # video
        self.recording = False
        self.elapsedSeconds = 0
        self.fps = 60
        
        self.targetMonitor = self.monitors[0]

        # other
        self.page = page

    # // ui
    def build(self):    
        # // controls
        # recording button
        self.recordingButton = flet.IconButton(
            icon = flet.icons.CIRCLE_SHARP,
            icon_color = flet.colors.RED,
            
            on_click = self.recordingButton_onClick
        )
        
        # open video folder button
        self.openVideoFolderButton = flet.IconButton(
            icon = flet.icons.FOLDER_ROUNDED,
            icon_color = flet.colors.BLACK,
            
            on_click = lambda _: self.openVideoFolder()
        )
        
        # timer text
        self.timerText = flet.Text(
            value = self.timerFormatted(),
            font_family = "Montserrat",
            size = 17,

            color = flet.colors.BLACK
        )
        
        # fps slider
        self.fpsSlider = flet.Slider(
            min = 5,
            max = 60,
            divisions = self.fps,
            value = self.fps,
            
            active_color = flet.colors.BLUE_300,
            thumb_color = flet.colors.BLACK,
            
            on_change = self.fpsSlider_onChange
        )
        
        # // main
        # finalization
        return flet.Container(
            content = flet.Row(
                controls = [
                    self.recordingButton,
                    self.openVideoFolderButton,
                    self.fpsSlider,
                    self.timerText
                ],
                
                expand = True,
                scale = 0.7
            ),

            expand = True,
            padding = flet.padding.only(right = 150)
        )
        
    # // functionality
    # helpers
    def generateVideoFileName(self):
        return str(uuid4())
    
    def getMonitorID(self):
        for monitorID, mon in enumerate(self.monitors):
            if mon == self.targetMonitor:
                return monitorID + 1

    def timerFormatted(self):
        time = datetime.timedelta(seconds = int(self.elapsedSeconds))
        time = str(time)

        return f"{time} @ {self.fps} FPS @ Monitor {self.getMonitorID()}"

    def openVideoFolder(self):
        os.startfile(f"{self.folderPath}")
        
    def notify(self, text: str, duration: int = 5):
        toast = win10toast.ToastNotifier()

        toast.show_toast(
            title = self.page.title,
            msg = text,
            duration = duration,
            threaded = True,
            callback_on_click = self.openVideoFolder
        )
    
    # control updates
    def updateTimerText(self):
        self.timerText.value = self.timerFormatted()
        self.timerText.update()
    
    # control callbacks  
    def navigationDrawer_onChange(self, _):
        chosenID = self.page.drawer.selected_index or 0

        self.targetMonitor = self.monitors[chosenID]  
        self.updateTimerText()
      
    def videoFileNameInput_onChange(self, _):
        # get new video filename
        value = self.videoFileNameInput.value or ""

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
        else:
            # change icon of recording button
            self.recordingButton.icon = flet.icons.CIRCLE_SHARP
            
        # disable controls depending on recording state
        self.fpsSlider.disabled = self.recording

        # update
        self.fpsSlider.update()
        self.recordingButton.update()
        
    def folder_onClick(self, _):
        # open folder
        self.openVideoFolder()
        
    # recording
    def record(self):
        # set state
        self.recording = True

        # record screen
        self.recorder = modules.recorder(
            fileName = self.generateVideoFileName(),
            resolution = (self.targetMonitor.width, self.targetMonitor.height),
            codec = self.videoCodec, 
            fileExtension = self.videoFileExtension,
            outputFolderPath = self.folderPath,
            fps = self.fps
        )

        self.recorder.startRecording(self.getMonitorID())
        
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