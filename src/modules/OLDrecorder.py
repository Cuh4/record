# // ---------------------------------------------------------------------
# // ------- [Record] Recorder Module
# // ---------------------------------------------------------------------

# major thanks to https://github.com/JRodrigoF/AVrecordeR/ for showing how to record video and audio simultaneously and output into one

# // ---- Imports
import cv2
import os
import pathlib
import pyautogui
import numpy
import threading
import pyaudio
import wave

# // ---- Variables
MatLike = numpy.ndarray[numpy.uint8]

# // ---- Classes
class recorder:
    # // init
    def __init__(self, fileName: str, pathToFFMPEG: str, resolution: tuple[int, int], tempFolderPath: str = "temp", outputFolderPath: str = "", fps: int = 60):
        # // setup
        # create paths if they dont exist
        pathlib.Path(outputFolderPath).mkdir(parents = True, exist_ok = True)
        pathlib.Path(tempFolderPath).mkdir(parents = True, exist_ok = True)
        
        # // attributes
        # paths, names, etc
        self.videoFileName = fileName

        self.outputFolderPath = os.path.abspath(outputFolderPath)
        self.outputFolderPathRel = self.relativePath(self.outputFolderPath)

        self.tempFolderPath = os.path.abspath(tempFolderPath)
        self.tempFolderPathRel = self.relativePath(self.tempFolderPath)
        
        self.tempFileName = "temp"

        # states
        self.recording = False
        
        # video and audio
        self.ffmpegPath = os.path.abspath(pathToFFMPEG)
        
        # video
        self.fps = fps
        self.resolution = resolution
        
        self.videoFileExtension = "mp4"
        self.videoCodec = "mp4v"
        self.fourcc = cv2.VideoWriter_fourcc(*self.videoCodec)
        
        # audio
        self.rate = 44100
        self.framesPerBuffer = 1024
        self.channels = 1

        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        
        self.audioFileExtension = "wav"

    # // methods
    # helpers
    def ffmpeg(self, command: str):
        return os.system(f"{self.ffmpegPath} {command}")
    
    def pathAndFile(self, path: str, file: str, fileExtension: str):
        return os.path.join(path, f"{file}.{fileExtension}")
    
    def relativePath(self, path: str):
        return os.path.relpath(path)
        
    # recording
    def __videoWriter(self, path: str):
        return cv2.VideoWriter(path, self.fourcc, float(self.fps / 2), self.resolution, True)
    
    def __audioStream(self):
        return self.audio.open(
            format = self.format,
            rate = self.rate,
            channels = self.channels,
            input = True,
            frames_per_buffer = self.framesPerBuffer
        )
        
    def __audioRecord(self, stream: pyaudio.Stream) -> list[bytes]:
        # get vars
        frames = []
        
        # main recording loop
        stream.start_stream()
        
        while True:
            # check if still recording
            if not self.recording:
                break
            
            data = stream.read(self.framesPerBuffer)
            frames.append(data)
            
        return frames
    
    def __videoRecord(self) -> list[MatLike]:
        # get vars
        frames = []
        
        # main recording loop
        while True: 
            # check stuffs before doing anything
            if not self.recording: # stopped recording, so stop
                break
            
            # capture screen
            frame = pyautogui.screenshot()
            frame = numpy.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
            # write
            frames.append(frame)
            
        return frames
    
    def startRecording(self):
        # set state
        self.recording = True
        
        # record video
        def video():
            # record video and save the frames
            videoWriter = self.__videoWriter(self.pathAndFile(self.tempFolderPathRel, self.tempFileName, self.videoFileExtension))
            videoFrames = self.__videoRecord()
            
            videoWriter.release()
            
            # save video
            for frame in videoFrames:
                videoWriter.write(frame)
                
        # record audio
        def audio():
            # record audio and save the frames
            waveFile = wave.open(self.pathAndFile(self.tempFolderPathRel, self.tempFileName, self.audioFileExtension), "wb")
            audioStream = self.__audioStream()

            audioFrames = self.__audioRecord(audioStream)

            audioStream.stop_stream()
            audioStream.close()
            
            # save audio
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b"".join(audioFrames))
        
        # create threads
        videoThread = threading.Thread(
            target = video
        )
        
        audioThread = threading.Thread(
            target = audio
        )
        
        # start the threads
        videoThread.start()
        audioThread.start()
        
    def endRecording(self):
        # set state
        self.recording = False