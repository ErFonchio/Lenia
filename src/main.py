from tkinter import *
from Gui import Gui
from Channels import Channel
from Statistics import Statistics
from Kernel import Kernel
from Growth import Growth
import time
import numpy as np
import json
import random

WIDTH = 1000 
HEIGHT = 600
FPS = 256
TIME = int(1000/FPS)

'''exctracting patterns'''


'''new batch from results1.json'''
with open("src/results1.json", "r") as f3:
    results = f3.readlines()

results = [json.loads(line) for line in results]

pattern = []
for i in range(len(results)):
        if (results[i]["mass"] < 1500) and (results[i]["ColorR"] > 0) and (results[i]["ColorG"] > 0) and (results[i]["ColorB"] > 0):
            pattern.append(results[i])

random.shuffle(pattern)
print(len(pattern))

cells = [
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.49,1.0,0,0.03,0.49,0.49,0.28,0.16,0.03,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.6,0.47,0.31,0.58,0.51,0.35,0.28,0.22,0,0,0,0,0], [0,0,0,0,0,0,0.15,0.32,0.17,0.61,0.97,0.29,0.67,0.59,0.88,1.0,0.92,0.8,0.61,0.42,0.19,0,0,0], [0,0,0,0,0,0,0,0.25,0.64,0.26,0.92,0.04,0.24,0.97,1.0,1.0,1.0,1.0,0.97,0.71,0.33,0.12,0,0], [0,0,0,0,0,0,0,0.38,0.84,0.99,0.78,0.67,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.95,0.62,0.37,0,0], [0,0,0,0,0.04,0.11,0,0.69,0.75,0.75,0.91,1.0,1.0,0.89,1.0,1.0,1.0,1.0,1.0,1.0,0.81,0.42,0.07,0], [0,0,0,0,0.44,0.63,0.04,0,0,0,0.11,0.14,0,0.05,0.64,1.0,1.0,1.0,1.0,1.0,0.92,0.56,0.23,0], [0,0,0,0,0.11,0.36,0.35,0.2,0,0,0,0,0,0,0.63,1.0,1.0,1.0,1.0,1.0,0.96,0.49,0.26,0], [0,0,0,0,0,0.4,0.37,0.18,0,0,0,0,0,0.04,0.41,0.52,0.67,0.82,1.0,1.0,0.91,0.4,0.23,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0.45,0.89,1.0,0.66,0.35,0.09,0], [0,0,0.22,0,0,0,0.05,0.36,0.6,0.13,0.02,0.04,0.24,0.34,0.1,0,0.04,0.62,1.0,1.0,0.44,0.25,0,0], [0,0,0,0.43,0.53,0.58,0.78,0.9,0.96,1.0,1.0,1.0,1.0,0.71,0.46,0.51,0.81,1.0,1.0,0.93,0.19,0.06,0,0], [0,0,0,0,0.23,0.26,0.37,0.51,0.71,0.89,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.42,0.06,0,0,0], [0,0,0,0,0.03,0,0,0.11,0.35,0.62,0.81,0.93,1.0,1.0,1.0,1.0,1.0,0.64,0.15,0,0,0,0,0], [0,0,0,0,0,0,0.06,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.05,0.09,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.28,0.42,0.44,0.34,0.18,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.34,1.0,1.0,1.0,1.0,1.0,0.91,0.52,0.14,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.17,0.75,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.35,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22,0.92,1.0,1.0,1.0,1.0,1.0,1.0,0.59,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.71,0.16], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.67,0.83,0.85,1.0,1.0,1.0,1.0,1.0,1.0,0.68,0.17], [0,0,0,0,0,0,0,0,0,0,0,0,0.21,0.04,0.12,0.58,0.95,1.0,1.0,1.0,1.0,1.0,0.57,0.13], [0,0,0,0,0,0,0,0,0,0,0,0.07,0,0,0,0.2,0.64,0.96,1.0,1.0,1.0,0.9,0.24,0.01], [0,0,0,0,0,0,0,0,0,0,0.13,0.29,0,0,0,0.25,0.9,1.0,1.0,1.0,1.0,0.45,0.05,0], [0,0,0,0,0,0,0,0,0,0,0.13,0.31,0.07,0,0.46,0.96,1.0,1.0,1.0,1.0,0.51,0.12,0,0], [0,0,0,0,0,0,0,0,0.26,0.82,1.0,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.3,0.05,0,0,0], [0,0,0,0,0,0,0,0,0.28,0.74,1.0,0.95,0.87,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.07,0.69,1.0,1.0,1.0,1.0,1.0,0.96,0.25,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.4,0.72,0.9,0.83,0.7,0.56,0.43,0.14,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.25,0.37,0.44,0.37,0.24,0.11,0.04,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.19,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.75,0.4,0.15,0,0,0,0], [0,0,0,0,0,0,0,0,0.14,0.48,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.4,0,0,0,0], [0,0,0,0,0,0,0,0,0.62,0.78,0.94,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0], [0,0,0,0,0,0,0,0.02,0.65,0.98,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.78,0,0,0,0], [0,0,0,0,0,0,0,0.15,0.48,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.79,0.05,0,0,0], [0,0,0,0,0,0,0.33,0.56,0.8,1.0,1.0,1.0,0.37,0.6,0.94,1.0,1.0,1.0,1.0,0.68,0.05,0,0,0], [0,0,0,0,0.35,0.51,0.76,0.89,1.0,1.0,0.72,0.15,0,0.29,0.57,0.69,0.86,1.0,0.92,0.49,0,0,0,0], [0,0,0,0,0,0.38,0.86,1.0,1.0,0.96,0.31,0,0,0,0,0.02,0.2,0.52,0.37,0.11,0,0,0,0], [0,0,0.01,0,0,0.07,0.75,1.0,1.0,1.0,0.48,0.03,0,0,0,0,0,0.18,0.07,0,0,0,0,0], [0,0.11,0.09,0.22,0.15,0.32,0.71,0.94,1.0,1.0,0.97,0.54,0.12,0.02,0,0,0,0,0,0,0,0,0,0], [0.06,0.33,0.47,0.51,0.58,0.77,0.95,1.0,1.0,1.0,1.0,0.62,0.12,0,0,0,0,0,0,0,0,0,0,0], [0.04,0.4,0.69,0.88,0.95,1.0,1.0,1.0,1.0,1.0,0.93,0.68,0.22,0.02,0,0,0.01,0,0,0,0,0,0,0], [0,0.39,0.69,0.91,1.0,1.0,1.0,1.0,1.0,0.85,0.52,0.35,0.24,0.17,0.07,0,0,0,0,0,0,0,0,0], [0,0,0.29,0.82,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.29,0.02,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.2,0.51,0.77,0.96,0.93,0.71,0.4,0.16,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.08,0.07,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0]]]

class Main():
    def __init__(self):
        self.tk = Tk()
        self.kernelList = []
        self.kernelWeights = []
        self.kernelSpecs = []
        self.g = Growth()
        self.channels = []
        self.table = None
        self.tabLen = 128
        self.gui = Gui(WIDTH, HEIGHT, FPS, self.tk, self.tabLen)
        self.stats = Statistics()
        self.start = 0
        self.end = 0
        self.count = 0 
        self.i = 0

    def world(self):
        '''preprocessing'''
        self.preprocessing(pattern[self.i])

        '''loop manager for computation and rendering'''
        self.manager_loop()
        
        '''mainloop for tkinter engine'''
        self.tk.mainloop() 
        
    def manager_loop(self):

        if self.gui.playFlag == 1:
            '''fps update'''
            self.end = time.time()
            self.gui.updateFps(1/(self.end-self.start))
            self.start = time.time()

            '''stats update'''
            self.stats.updateStats([self.channels[0].table, self.channels[1].table, self.channels[2].table])
            self.gui.updateGuiStats(mass=self.stats.tableMass, COM=self.stats.COM_RGB, 
                                    vel=self.stats.vel, linVel=self.stats.LinVel, 
                                    angle=self.stats.ang, angularVel=self.stats.angularVel)
            '''Il manager aggiorna la griglia e poi avvia la stampa tramite la GUI'''
            for i in range(len(self.kernelList)):
                src = self.kernelList[i].channelSrc #src index
                dst = self.kernelList[i].channelDst #dst index
                G = self.channels[src].convolveAndGrowChannel(kernel=self.kernelList[i].kernel, growthFunction=self.g.make_bell, m=self.kernelList[i].m, s=self.kernelList[i].s)
                self.channels[dst].updateChannel(G, self.kernelList[i].weight)

            for i in range(len(self.channels)):
                self.channels[i].updateChannel2()

            if self.gui.saveFlag == 1:
                with open("src/saved.txt", "a") as f:
                    f.write(str(pattern[self.i]) + "\n")
                self.gui.saveFlag = 0
            elif self.gui.nextFlag == 1 and self.i < (len(pattern)-1):
                self.i += 1
                self.preprocessing(pattern[self.i])
                self.gui.nextFlag = 0
            elif self.gui.prevFlag == 1 and self.i > 0:
                self.i -= 1
                self.preprocessing(pattern[self.i])
                self.gui.prevFlag = 0
            elif self.gui.clickFlag == 1:
                radius = 32
                self.channels[0].putRandomValues(self.gui.lastClickFlag, radius, self.gui.canvasDimensions)
                self.channels[1].putRandomValues(self.gui.lastClickFlag, radius, self.gui.canvasDimensions)
                self.channels[2].putRandomValues(self.gui.lastClickFlag, radius, self.gui.canvasDimensions)
                self.gui.clickFlag = 0
                

            '''il manager avvia il loop della gui'''
            self.gui.mainloop_gui([self.channels[0].table, self.channels[1].table, self.channels[2].table]) #La gui non ha i permessi di modifica sui channel
        
        elif self.gui.playFlag == 2:
            self.channels[0].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[0])
            self.channels[1].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[1])
            self.channels[2].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[2])
            self.gui.playFlag = 1
        
        '''viene richiamata la funzione manager_loop dopo [TIME] tempo'''
        self.tk.after(TIME, self.manager_loop)

    def preprocessing(self, pattern):

        '''extracting specs'''
        delta = pattern['T']
        radius = pattern['R']

        '''kernel list'''
        self.kernelSpecs = pattern['kernels']
        self.kernelList = []
        for spec in self.kernelSpecs:
            kernel = Kernel(weight=spec['h'], c0=spec['c0'], c1=spec['c1'], m=spec['m'], s=spec['s'])
            kernel.create_2dgaussian_classic_fft(R=radius, r=spec['r'], B=spec['b'], table_len=self.tabLen)
            self.kernelList.append(kernel)

        '''Channels RGB'''
        self.channels = [
            Channel(self.tk, delta),
            Channel(self.tk, delta),
            Channel(self.tk, delta)]
        
        self.channels[0].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[0])
        self.channels[1].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[1])
        self.channels[2].initialize_table(rows=self.tabLen, cols=self.tabLen, table=cells[2])



if __name__ == "__main__":

    m = Main()
    m.world()