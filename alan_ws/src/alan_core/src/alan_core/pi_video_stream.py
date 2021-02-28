#! /home/sorozco/computer_vision/bin/python3

## pi camera allows access to the RAspberry Pi camera module
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time

class PiVideoStream:
    def __init__(self,resolution=(640,480),framerate=90):

        ##initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,format = "bgr",use_video_port=True)

        ## initialize the frame and variable use to indicate if thread should be stopped
        self.frame = None
        self.stopped = True

    def start(self):
        self.stopped = False
        #start the thread to read frames from the video stream
        Thread(target=self.update,args=()).start()

        ## give camera some time to warmup 
        time.sleep(2.0)
        return self

    def update(self):
        # keep looping infinitely until the thread stops
        for f in self.stream:
            #grab the frame from the stream and clear the stream in prep for next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indication variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
    def read(self):
        # return the frame most recently read
        return self.frame
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

        ## give camera some time to cool down and deallocate resources
        time.sleep(2.0)


