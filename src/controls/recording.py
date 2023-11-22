# // ---------------------------------------------------------------------
# // ------- [Record] Recording Control
# // ---------------------------------------------------------------------

# // ---- Imports
import flet
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
        
        self.monitor = get_monitors()[0]

        # video
        self.recording = False
        self.elapsedSeconds = 0
        self.fps = 60
        
        self.recorder = modules.recorder(
            fileName = self.videoFileName,
            resolution = (self.monitor.width, self.monitor.height),
            codec = self.videoCodec, 
            fileExtension = self.videoFileExtension,
            outputFolderPath = self.folderPath,
            fps = self.fps
        )

        # other
        self.page = page

    # // ui
    def build(self):
        # // controls
        # video file name input
        self.videoFileNameInput = flet.TextField(
            value = self.videoFileName,
            height = 15,
            border_color = flet.colors.WHITE,
            tooltip = "Video Name",
            max_length = 15,
            max_lines = 1,

            text_style = flet.TextStyle(
                size = 11,
                font_family = "Montserrat",
            ),
            
            on_change = self.videoFileNameInput_onChange
        )
        
        # recording button
        self.recordingButton = flet.IconButton(
            icon = flet.icons.CIRCLE_ROUNDED,
            icon_color = flet.colors.WHITE,
            on_click = self.recordingButton_onClick
        )
        
        # timer text
        self.timerText = flet.Text(
            value = "0:00:00",
            font_family = "Montserrat"
        )
        
        # fps slider
        self.fpsText = flet.Text(
            value = f"{self.fps} FPS",
            font_family = "Montserrat"
        )
        
        self.fpsSlider = flet.Slider(
            label = "{value} FPS",

            min = 5,
            max = 60,
            divisions = self.fps,
            value = self.fps,
            
            active_color = flet.colors.BLUE_300,
            thumb_color = flet.colors.WHITE,
            scale = 0.8,
            
            on_change = self.fpsSlider_onSlideChange
        )
        
        # // main
        # finalization
        return flet.Row(
            controls = [
                flet.Column(
                    controls = [
                        self.videoFileNameInput,
                        
                        flet.Divider(
                            thickness = 2,
                            color = flet.colors.WHITE
                        ),
                        
                        flet.Row(
                            controls = [
                                self.recordingButton,

                                flet.IconButton(
                                    icon = flet.icons.FOLDER_COPY_ROUNDED,
                                    icon_color = flet.colors.ORANGE_400,
                                    on_click = self.folder_onClick
                                ),
                                
                                self.timerText
                            ],
                        
                            alignment = flet.MainAxisAlignment.CENTER,
                            vertical_alignment = flet.CrossAxisAlignment.CENTER
                        )
                    ],
                    
                    expand = True,
                    alignment = flet.MainAxisAlignment.CENTER,
                    horizontal_alignment = flet.CrossAxisAlignment.CENTER,
                    spacing = 0.2,
                    scale = 0.85
                ),
                
                flet.Column(
                    controls = [
                        self.fpsText,
                        self.fpsSlider
                    ],

                    expand = True,
                    alignment = flet.MainAxisAlignment.CENTER,
                    horizontal_alignment = flet.CrossAxisAlignment.CENTER,
                    spacing = 0.2,
                    scale = 0.85
                )
            ]
        )
        
    # // functionality
    # helpers
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
        self.recorder.videoFileName = self.videoFileName
    
    # control updates
    def updateTimerText(self):
        # format time
        time = datetime.timedelta(seconds = int(self.elapsedSeconds))
        time = str(time)
        
        # update visuals
        self.timerText.value = f"{time} @ {self.fps} FPS"
        self.timerText.update()
    
    # control callbacks    
    def videoFileNameInput_onChange(self, _):
        value = self.videoFileNameInput.value or ""
        self.changeFileName(value)
        
    def fpsSlider_onSlideChange(self, _):
        if self.recording:
            return
        
        # update fps attribute
        self.fps = int(self.fpsSlider.value)
        
        # update visuals
        self.fpsText.value = f"{self.fps} FPS"
        self.fpsText.update()
    
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
            self.recordingButton.icon_color = flet.colors.WHITE
            
        # disable controls depending on recording state
        self.videoFileNameInput.disabled = self.recording
        self.fpsSlider.disabled = self.recording
            
        # update
        self.fpsSlider.update()
        self.videoFileNameInput.update()
        self.recordingButton.update()
        
    def folder_onClick(self, _):
        # open folder
        self.openRecordResultFolder()
        
    # recording
    def record(self):
        # set state
        self.recording = True

        # record screen
        self.recorder.startRecording()
        
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