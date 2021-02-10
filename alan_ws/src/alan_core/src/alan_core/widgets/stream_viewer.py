import tkinter as tk
import cv2
import rospy
from alan_core.pi_video_stream import PiVideoStream
from PIL import Image,ImageTk

class StreamViewer(tk.LabelFrame):
    def __init__(self,parent,*args,**kwargs):
        tk.LabelFrame.__init__(self,parent,*args,**kwargs)
        self.parent = parent

        self.is_streaming = False
        self.camera = PiVideoStream()


        # display left hand controls
        self.left_wheel_label = tk.Label(self,text="Left Power: ")
        self.left_wheel_label.grid(row=0,column=0)

        # allow user to start or stop stream 
        self.stream_button_text = tk.StringVar()
        self.stream_button_text.set("Start Steam")
        self.stream_button= tk.Button(self, textvariable=self.stream_button_text)
        self.stream_button.grid(row=0,column=1)
        self.stream_button.bind('<Button-1>',self.start_stream)

        # display right hand controls
        self.right_wheel_label = tk.Label(self,text="Right Power: ")
        self.right_wheel_label.grid(row=0,column=2)

        self.frame = tk.Frame(self, highlightthickness=1)
        self.frame.grid(row=1,column=0,columnspan=3)

        self.label = tk.Label(self.frame,padx=200,pady=200)
        self.label.grid(row=1,column=0,columnspan=3)

    def start_stream(self,event):
        self.stream_button_text.set("Stop Stream")
        self.stream_button.bind('<Button-1>',self.stop_stream)

        # allow stream loop to begin
        self.is_streaming = True

        # start camera only if it is not already started
        if (self.camera.stopped):
            self.camera.start()

        # begin streaming
        self.stream()

    def stop_stream(self,event):
        self.stream_button_text.set("Start Stream")
        self.stream_button.bind('<Button-1>',self.start_stream)

        # stop stream looping
        self.is_streaming = False

        # stop camera
        self.camera.stop()

    def stream(self):
        try:

            # stop stream loop
            if not self.is_streaming:
                return

            # Capture frame-by-frame
            frame = self.camera.read()

            # flip to correct rotation
            frame = cv2.flip(frame,0)
            frame = cv2.flip(frame,1)

            # display stream frame onto screen
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.label.config(image=frame)
            self.label.image =frame
            
            # call stream function again in 1ms
            self.label.after(1,lambda:self.stream())

        except:
            self.camera.stop()
            return
