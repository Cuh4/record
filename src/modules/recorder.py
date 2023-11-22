# // ---------------------------------------------------------------------
# // ------- [Record] Recorder Module
# // ---------------------------------------------------------------------

# major thanks to https://github.com/JRodrigoF/AVrecordeR/ for showing how to record video and audio simultaneously and output into one
# although i couldn't implement it because pyaudio doesn't record output, only input (like microphones), so this only records video now

# // ---- Imports
import cv2
import os
import pathlib
import pyautogui
import numpy
import threading

from . import events

# // ---- Variables
MatLike = numpy.ndarray[numpy.uint8]

# // ---- Classes
class recorder:
    # // init
    def __init__(self, fileName: str, resolution: tuple[int, int], codec: str = "mp4v", fileExtension: str = "mp4", outputFolderPath: str = "", fps: int = 60):
        # // setup
        # create paths if they dont exist
        pathlib.Path(outputFolderPath).mkdir(parents = True, exist_ok = True)
        
        # // attributes
        # paths, names, etc
        self.videoFileName = fileName

        self.outputFolderPath = os.path.abspath(outputFolderPath)
        self.outputFolderPathRel = self.__relativePath(self.outputFolderPath)

        # states
        self.recording = False
        
        # video
        self.fps = fps / 1.5 # prevents speed-up or something
        self.resolution = resolution
        
        self.videoCodec = codec
        self.videoFileExtension = fileExtension
        self.fourcc = cv2.VideoWriter_fourcc(*self.videoCodec)

    # // methods
    # helpers
    def __pathAndFile(self, path: str, file: str, fileExtension: str):
        return os.path.join(path, f"{file}.{fileExtension}")
    
    def __relativePath(self, path: str):
        return os.path.relpath(path)
        
    def __videoWriter(self, path: str):
        return cv2.VideoWriter(path, self.fourcc, float(self.fps / 2), self.resolution, True)

    # recording
    def startRecording(self):
        if self.recording:
            return
        
        # set state
        self.recording = True
        
        # create record event
        recordEvent = events.event()
        
        # record video
        def video():
            # get video writer
            videoWriter = self.__videoWriter(self.__pathAndFile(self.outputFolderPathRel, self.videoFileName, self.videoFileExtension))
            
            # recording loop
            while True: 
                # check stuffs before doing anything
                if not self.recording: # stopped recording, so stop
                    break
                
                # capture screen
                frame = pyautogui.screenshot()
                frame = numpy.array(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                # fire event
                recordEvent.fire(frame)
                    
                # write
                videoWriter.write(frame)
            
            # release video writer
            videoWriter.release()
        
        # create thread
        videoThread = threading.Thread(
            target = video
        )
        
        # start the thread
        videoThread.start()
        
        # return record event
        return recordEvent
        
    def endRecording(self):
        # set state
        self.recording = False