import sys
from tkinter import *
import math
from Gui import Gui
from Channels import Channel
import time
import numpy as np
from PIL import Image, ImageTk

WIDTH = 900
HEIGHT = 600
FPS = 2
TIME = int(1000/FPS)


class Main():
    def __init__(self):
        self.tk = Tk()
        self.kernel_list = []
        self.growth_function = []   
        self.channels = []
        self.table = None
        self.gui = Gui(WIDTH, HEIGHT, FPS, self.tk)
        self.channel = Channel(WIDTH, HEIGHT, self.tk)


    def world(self):   
        self.manager_loop()
        self.gui.root.mainloop()

    def manager_loop(self):
        table_prova = np.random.rand(100, 100)*255
        self.gui.mainloop_gui(table_prova)
        self.gui.root.after(TIME, self.manager_loop)

        
m = Main()
m.world()