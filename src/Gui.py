from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import matplotlib.pyplot as plt
import io

SECONDWINDOW_BG = "#52535c"
LABEL_BG = SECONDWINDOW_BG
FONT_SIZE = 15
FONT = "Helvetica"


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
        self.zoom = 2
        self.tabLen = tabLen
        self.canvasDimensions = self.zoom*self.tabLen, self.zoom*self.tabLen
        self.patternSavedFlag = 0

        '''initializing the four frames'''
        self.root.maxsize(self.width, self.height)
        self.mainframe = Frame(self.root, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.mainframe.grid(row=0, column=0, padx=0, pady=0)

        self.labelFps = Label(self.mainframe, text="FPS: "+str(self.FPS), font=("Helvetica", 16))
        self.labelFps.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        self.firstFrame = Frame(self.mainframe, width=self.canvasDimensions[0], height=self.canvasDimensions[0])
        self.secondFrame = Frame(self.mainframe, width=self.canvasDimensions[0], height=self.canvasDimensions[0])
        self.thirdFrame = Frame(self.mainframe, width=self.canvasDimensions[0], height=self.canvasDimensions[0])
        self.fourthFrame = Frame(self.mainframe, width=self.canvasDimensions[0], height=self.canvasDimensions[0])

        self.firstFrame.grid(row=1, column=0, padx=0, pady=0)
        self.secondFrame.grid(row=1, column=1, padx=0, pady=0)
        self.thirdFrame.grid(row=2, column=0, padx=0, pady=0)
        self.fourthFrame.grid(row=2, column=1, padx=0, pady=0)


        self.secondframe = Frame(self.root, width=self.SECONDFRAME_W, height=self.SECONDFRAME_H, bg=SECONDWINDOW_BG)
        self.secondframe.grid_propagate(False)
        self.secondframe.grid(row=0, column=1, padx=0, pady=0)
        
        self.initialize_secondwindow()
        
        self.imgFirstFrame = None
        self.canvasFirstFrame = Canvas(self.firstFrame, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvasFirstFrame.pack()
        
        self.imgSecondFrame = None
        self.canvasSecondFrame = Canvas(self.secondFrame, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvasSecondFrame.pack()
        
        self.imgThirdFrame = None
        self.canvasThirdFrame = Canvas(self.thirdFrame, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvasThirdFrame.pack()
        
        self.imgFourthFrame = None
        self.canvasFourthFrame = Canvas(self.fourthFrame, width=self.canvasDimensions[0], height=self.canvasDimensions[1])
        self.canvasFourthFrame.pack()

        self.canvasFirstFrame.bind("<Button-1>", self.click)

    def mainloop_gui(self, tableList, G, U):
        self.printTable(tableList)
        self.printG(G)
        self.printU(U)

    def plotGrowthFunction(self, parametersList):
        '''Create subplots of the growth function'''
        width = self.canvasDimensions[0]/100
        height = self.canvasDimensions[1]/100  
        fig, ax = plt.subplots(figsize=(width, height))

        '''cycle through the parameters list and plot the growth function'''
        for params in parametersList:
            mean, std_dev = params
            x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
            y = (np.exp(-((x-mean)/std_dev)**2 / 2)*2)-1
            ax.plot(x, y)

        '''Design changes'''
        ax.tick_params(axis='both', which='major', labelsize=8)

        '''Image saving'''
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        '''Image loading'''
        img = Image.open(buf)
        self.imgFourthFrame = ImageTk.PhotoImage(img)

        '''Display the image'''
        self.canvasFourthFrame.create_image(0, 0, anchor="nw", image=self.imgFourthFrame)

        '''closing buffer'''
        buf.close()
        

    def printU(self, tableList, padx=0, pady=0):
        scaledTables = []
        for i in range(len(tableList)):
            table = np.kron(tableList[i], np.ones((self.zoom, self.zoom)))
            scaledTables.append(table)

        scaledTables = np.array(scaledTables)
        scaledTables = np.transpose(scaledTables, (1, 2, 0))
        scaledTables = cv2.normalize(scaledTables, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        self.imgThirdFrame =  ImageTk.PhotoImage(image=Image.fromarray(scaledTables, 'RGB'))
        self.canvasThirdFrame.create_image(padx, pady, anchor="nw", image=self.imgThirdFrame)

    def printG(self, tableList, padx=0, pady=0):
        scaledTables = []
        for i in range(len(tableList)):
            table = np.kron(tableList[i], np.ones((self.zoom, self.zoom)))
            scaledTables.append(table)

        scaledTables = np.array(scaledTables)
        scaledTables = np.transpose(scaledTables, (1, 2, 0))
        scaledTables = cv2.normalize(scaledTables, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        self.imgSecondFrame =  ImageTk.PhotoImage(image=Image.fromarray(scaledTables, 'RGB'))
        self.canvasSecondFrame.create_image(padx, pady, anchor="nw", image=self.imgSecondFrame)
    
    def printTable(self, tableList, padx=0, pady=0):
        scaledTables = []
        for i in range(len(tableList)):
            '''fast method to scale the table'''
            table = np.kron(tableList[i], np.ones((self.zoom, self.zoom)))
            scaledTables.append(table)

        '''trasform to array, transpose in new shape for cv2 normalization'''
        scaledTables = np.array(scaledTables)
        scaledTables = np.transpose(scaledTables, (1, 2, 0))
        scaledTables = cv2.normalize(scaledTables, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        '''create RGB image'''
        self.imgFirstFrame = ImageTk.PhotoImage(image=Image.fromarray(scaledTables, 'RGB'))
        self.canvasFirstFrame.create_image(padx, pady, anchor="nw", image=self.imgFirstFrame)

    def initialize_secondwindow(self):
        self.initialize_buttons()
        self.initialize_labels()

    def initialize_buttons(self):

        self.buttonList = []

        '''empty columns to center buttons'''
        self.secondframe.grid_columnconfigure(0, weight=1)
        self.secondframe.grid_columnconfigure(4, weight=1)
        
        self.playButton = Button(self.secondframe, text="Play", command=self.play, highlightbackground=SECONDWINDOW_BG)
        self.playButton.grid(row=0, column=1)
        self.stopButton = Button(self.secondframe, text="Stop", command=self.stop, highlightbackground=SECONDWINDOW_BG)
        self.stopButton.grid(row=0, column=2)
        self.resetButton = Button(self.secondframe, text="Reset", command=self.reset, highlightbackground=SECONDWINDOW_BG)
        self.resetButton.grid(row=0, column=3)
        self.saveButton = Button(self.secondframe, text="Save", command=self.saveFunction, highlightbackground=SECONDWINDOW_BG)
        self.saveButton.grid(row=1, column=1)
        self.nextButton = Button(self.secondframe, text="Next", command=self.nextFunction, highlightbackground=SECONDWINDOW_BG)
        self.nextButton.grid(row=1, column=3)
        self.prevButton = Button(self.secondframe, text="Prev", command=self.prevFunction, highlightbackground=SECONDWINDOW_BG)
        self.prevButton.grid(row=1, column=2)

        self.buttonList.append(self.playButton)
        self.buttonList.append(self.stopButton)
        self.buttonList.append(self.resetButton)
        self.buttonList.append(self.saveButton)
        self.buttonList.append(self.prevButton)
        self.buttonList.append(self.nextButton)

    def initialize_labels(self):
        padding = 40
        self.labelMass = Label(self.secondframe, text="Mass: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelMass.place(x=10, y=40+padding)
        self.labelCOM = Label(self.secondframe, text="Center of Mass: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelCOM.place(x=10, y=70+padding)
        self.labelVel = Label(self.secondframe, text="Velocity: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelVel.place(x=10, y=100+padding)
        self.labelLinVel = Label(self.secondframe, text="Linear Velocity: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelLinVel.place(x=10, y=130+padding)
        self.labelAngle = Label(self.secondframe, text="Angle: ", font=("Helvetica", FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelAngle.place(x=10, y=160+padding)
        self.labelAngularVel = Label(self.secondframe, text="Angular Velocity: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelAngularVel.place(x=10, y=190+padding)
        self.labelVariance = Label(self.secondframe, text="Variance: ", font=("Helvetica", FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelVariance.place(x=10, y=220+padding)
        self.labelVarianceVelocity = Label(self.secondframe, text="Variance Velocity: ", font=(FONT, FONT_SIZE), highlightbackground=SECONDWINDOW_BG, bg=SECONDWINDOW_BG)
        self.labelVarianceVelocity.place(x=10, y=250+padding)

    def saveFunction(self):
        self.saveFlag = 1

    def nextFunction(self):
        self.nextFlag = 1
    
    def prevFunction(self):
        self.prevFlag = 1

    def play(self):
        self.playFlag = 1

    def stop(self):
        self.playFlag = 0

    def reset(self):
        self.playFlag = 2

    def click(self, event):
        self.clickFlag = 1
        self.lastClickFlag = event.x, event.y

    def updateFps(self, realTimeFPS):
        self.labelFps.config(text="FPS: "+str(realTimeFPS)[:4])
    def updateGuiStats(self, mass, COM, vel, linVel, angle, angularVel, variance, varianceVel):
        self.labelMass.config(text="Mass: "+str(mass)[:4]+" u")
        self.labelCOM.config(text="COM_x: "+str(COM[1])[:4]+"px, COM_y: "+str(COM[0])[:4]+" px")
        self.labelVel.config(text="V_x: "+str(vel[1])[:6]+"px/f V_y: "+str(vel[0])[:6]+" px/f")
        self.labelLinVel.config(text="|V|: "+str(linVel)[:6]+" px/f")
        self.labelAngle.config(text="Angle: "+str(angle)[:6]+"°")
        self.labelAngularVel.config(text="AngularVel: "+str(angularVel)[:6]+" grades/f")
        self.labelVariance.config(text="Variance x1000: "+str(variance)[:4])
        self.labelVarianceVelocity.config(text="VarianceVel x1000: "+str(varianceVel)[:4])


