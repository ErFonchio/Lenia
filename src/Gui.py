from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import cv2

SECONDWINDOW_BG = "white"


class Gui:
    def __init__(self, WIDTH, HEIGHT, FPS, window):
        self.root = window
        self.root.title("Lenia")
        self.width = WIDTH
        self.height = HEIGHT
        self.MAINFRAME_W = (WIDTH*0.7)-30
        self.MAINFRAME_H = HEIGHT
        self.SECONDFRAME_W = (WIDTH*0.3)-20
        self.SECONDFRAME_H = HEIGHT
        self.FPS = FPS
        self.playFlag = 1 #flag for play and stop button

        '''initializing mainframe and secondframe'''
        self.root.maxsize(self.width, self.height)
        self.mainframe = Frame(self.root, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.mainframe.grid(row=0, column=0, padx=0, pady=0)

        self.labelFps = Label(self.mainframe, text="FPS: "+str(self.FPS), font=("Helvetica", 16))
        self.labelFps.pack()

        self.secondframe = Frame(self.root, width=self.SECONDFRAME_W, height=self.SECONDFRAME_H, bg=SECONDWINDOW_BG)
        self.secondframe.grid_propagate(False)
        self.secondframe.grid(row=0, column=1, padx=0, pady=0)
        
        self.initialize_secondwindow()
        
        self.img = None
        self.canvas = Canvas(self.mainframe, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.canvas.pack()

    def mainloop_gui(self, tableList):
        self.printTable(tableList, fit=False)
        

    def print_kernel(self, kernel, padx=10, pady=10):
        kernel = self.matrix_scaling(kernel, 30, 30)
        kernel = self.color_mapping(kernel)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(kernel))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def printTable(self, tableList, padx=10, pady=10, fit=False):
        zoom = 3
        scaledTables = []
        #print(tableList)
        for i in range(len(tableList)):
            table = np.kron(tableList[i], np.ones((zoom, zoom)))
            scaledTables.append(table)
        print(scaledTables)
        t = self.color_mapping(scaledTables)
        t = np.clip(t, 0, 255).astype(np.uint8)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(t))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def color_mapping(self, scaledTables):
        return np.stack((scaledTables[0], scaledTables[1], scaledTables[2]), axis=-1)


    def initialize_secondwindow(self):
        
        self.initialize_buttons()
        self.initialize_labels()

    def initialize_buttons(self):

        self.buttonList = []
        
        self.playButton = Button(self.secondframe, text="Play", command=self.play, highlightbackground=SECONDWINDOW_BG)
        self.playButton.grid(row=0, column=0)
        self.stopButton = Button(self.secondframe, text="Stop", command=self.stop, highlightbackground=SECONDWINDOW_BG)
        self.stopButton.grid(row=0, column=1)
        self.resetButton = Button(self.secondframe, text="Reset", command=self.reset, highlightbackground=SECONDWINDOW_BG)
        self.resetButton.grid(row=0, column=2)

        self.buttonList.append(self.playButton)
        self.buttonList.append(self.stopButton)
        self.buttonList.append(self.resetButton)

    def initialize_labels(self):
        self.labelMass = Label(self.secondframe, text="Mass: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelMass.place(x=10, y=40)
        self.labelCOM = Label(self.secondframe, text="Center of Mass: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelCOM.place(x=10, y=70)
        self.labelVel = Label(self.secondframe, text="Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelVel.place(x=10, y=100)
        self.labelLinVel = Label(self.secondframe, text="Linear Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelLinVel.place(x=10, y=130)
        self.labelAngle = Label(self.secondframe, text="Angle: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelAngle.place(x=10, y=160)
        self.labelAngularVel = Label(self.secondframe, text="Angular Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelAngularVel.place(x=10, y=190)

    def play(self):
        self.playFlag = 1
        print("Hai premuto play")

    def stop(self):
        self.playFlag = 0
        print("Hai premuto stop")

    def reset(self):
        self.playFlag = 2
        print("Hai premuto reset")

    def updateFps(self, realTimeFPS):
        self.labelFps.config(text="FPS: "+str(realTimeFPS)[:4])
    def updateGuiStats(self, mass, COM, vel, linVel, angle, angularVel):
        self.labelMass.config(text="Mass: "+str(mass)[:4]+" u")
        self.labelCOM.config(text="COM_x: "+str(COM[1])[:4]+"px, COM_y: "+str(COM[0])[:4]+" px")
        self.labelVel.config(text="V_x: "+str(vel[1])[:4]+"px/f V_y: "+str(vel[0])[:4]+" px/f")
        self.labelLinVel.config(text="|V|: "+str(linVel)[:4]+" px/f")
        self.labelAngle.config(text="Angle: "+str(angle)[:4]+" rad")
        self.labelAngularVel.config(text="AngularVel: "+str(angularVel)[:4]+" rad/f")

