from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2

SECONDWINDOW_BG = "white"


class Gui:
    def __init__(self, WIDTH, HEIGHT, FPS, window, tabLen):
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
        self.saveFlag = 0 #flag for save button
        self.nextFlag = 0 #flag for next button
        self.prevFlag = 0 #flag for prev button
        self.clickFlag = 0
        self.lastClickFlag = 0, 0
        self.zoom = 4
        self.tabLen = tabLen
        self.canvasDimensions = self.zoom*self.tabLen, self.zoom*self.tabLen

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
        self.canvas = Canvas(self.mainframe, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.click)

    def mainloop_gui(self, tableList):
        self.printTable(tableList)
        
    
    def printTable(self, tableList, padx=0, pady=0):
        scaledTables = []
        for i in range(len(tableList)):
            table = np.kron(tableList[i], np.ones((self.zoom, self.zoom)))
            scaledTables.append(table)

        t = (0.299*scaledTables[0]+0.587*scaledTables[1]+0.114*scaledTables[2])*255
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(t))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def color_mapping(self, table):
        # Normalizza la tabella dei valori tra 0 e 255
        norm_table = (table*255).astype(np.uint8)
        
        # Applica la mappa dei colori plasma
        colored_table = cv2.applyColorMap(norm_table, cv2.COLORMAP_INFERNO)
        return colored_table

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
        self.saveButton = Button(self.secondframe, text="Save", command=self.saveFunction, highlightbackground=SECONDWINDOW_BG)
        self.saveButton.grid(row=1, column=0)
        self.nextButton = Button(self.secondframe, text="Next", command=self.nextFunction, highlightbackground=SECONDWINDOW_BG)
        self.nextButton.grid(row=1, column=2)
        self.prevButton = Button(self.secondframe, text="Prev", command=self.prevFunction, highlightbackground=SECONDWINDOW_BG)
        self.prevButton.grid(row=1, column=1)

        self.buttonList.append(self.playButton)
        self.buttonList.append(self.stopButton)
        self.buttonList.append(self.resetButton)
        self.buttonList.append(self.saveButton)
        self.buttonList.append(self.prevButton)
        self.buttonList.append(self.nextButton)

    def initialize_labels(self):
        padding = 30
        self.labelMass = Label(self.secondframe, text="Mass: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelMass.place(x=10, y=40+padding)
        self.labelCOM = Label(self.secondframe, text="Center of Mass: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelCOM.place(x=10, y=70+padding)
        self.labelVel = Label(self.secondframe, text="Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelVel.place(x=10, y=100+padding)
        self.labelLinVel = Label(self.secondframe, text="Linear Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelLinVel.place(x=10, y=130+padding)
        self.labelAngle = Label(self.secondframe, text="Angle: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelAngle.place(x=10, y=160+padding)
        self.labelAngularVel = Label(self.secondframe, text="Angular Velocity: ", font=("Helvetica", 16), highlightbackground=SECONDWINDOW_BG)
        self.labelAngularVel.place(x=10, y=190+padding)

    def saveFunction(self):
        self.saveFlag = 1
        print("Hai premuto save")

    def nextFunction(self):
        self.nextFlag = 1
        print("Hai premuto next")
    
    def prevFunction(self):
        self.prevFlag = 1
        print("Hai premuto prev")

    def play(self):
        self.playFlag = 1
        print("Hai premuto play")

    def stop(self):
        self.playFlag = 0
        print("Hai premuto stop")

    def reset(self):
        self.playFlag = 2
        print("Hai premuto reset")

    def click(self, event):
        self.clickFlag = 1
        self.lastClickFlag = event.x, event.y
        print("Hai cliccato col tasto sinistro nella posizione: ", event.x, event.y)

    def updateFps(self, realTimeFPS):
        self.labelFps.config(text="FPS: "+str(realTimeFPS)[:4])
    def updateGuiStats(self, mass, COM, vel, linVel, angle, angularVel):
        self.labelMass.config(text="Mass: "+str(mass)[:4]+" u")
        self.labelCOM.config(text="COM_x: "+str(COM[1])[:4]+"px, COM_y: "+str(COM[0])[:4]+" px")
        self.labelVel.config(text="V_x: "+str(vel[1])[:4]+"px/f V_y: "+str(vel[0])[:4]+" px/f")
        self.labelLinVel.config(text="|V|: "+str(linVel)[:4]+" px/f")
        self.labelAngle.config(text="Angle: "+str(angle)[:4]+" rad")
        self.labelAngularVel.config(text="AngularVel: "+str(angularVel)[:4]+" rad/f")

