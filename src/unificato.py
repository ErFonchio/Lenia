import sys
from tkinter import *
import math
from Channels import Channel
import time
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

WIDTH = 1000
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
        table_prova = np.random.rand(100, 100)*255  
        self.channel.kernel()
        self.gui.print_table(self.channel.kernel_*255)
        #self.manager_loop(table_prova)
        self.gui.root.mainloop()

    def manager_loop(self, table_prova):
        
        self.gui.mainloop_gui(table_prova)
        self.gui.root.after(TIME, self.manager_loop)


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

        self.root.maxsize(self.width, self.height)
        mainframe = Frame(self.root, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        mainframe.grid(row=0, column=0, padx=10, pady=10)
        secondframe = Frame(self.root, width=self.SECONDFRAME_W, height=self.SECONDFRAME_H, bg="white")
        secondframe.grid(row=0, column=1, padx=10, pady=10)
        self.img = None
        self.canvas = Canvas(mainframe, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.canvas.pack()

    def mainloop_gui(self, table):
        self.print_table(table)
        
    def print_table(self, table):
        table = self.matrix_scaling(table, 5)
        table = self.color_mapping(table)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(table).convert('RGB'))
        self.canvas.create_image(10, 10, anchor="nw", image=self.img)
    
    def color_mapping(self, table):
        # Normalize the table values to the range [0, 1]
        normalized_table = table / 255.0
        
        # Create a custom colormap using violet colors
        #colors = [(1, 1, 1), (0.5, 0, 1)]  # From white to violet RGB
        #colors = [(0, 0, 1), (0.5, 0, 1)]  #violet-blue
        #colors = [(1, 0, 0), (0.5, 0, 1)]
        colors = [(1, 1, 1), (0, 0, 0)] #grigi
        cmap = mcolors.LinearSegmentedColormap.from_list("my_colormap", colors)
        
        # Apply the colormap to the normalized table
        colored_table = cmap(normalized_table)
        
        # Convert to RGB values in the range [0, 255]
        colored_table = (colored_table[:, :, :3] * 255).astype(np.uint8)
        
        return colored_table

    def matrix_scaling(self, matrix, alfa):
        matrice_espansa = np.repeat(np.repeat(matrix, alfa, axis=0), alfa, axis=1)
        return matrice_espansa
    
class Channel:
    def __init__(self, WIDTH, HEIGHT, tk): 
        self.flag_update = True
        self.WIDTH = WIDTH
        self.height = HEIGHT
        self.table_width = 100
        self.table_height = 100
        self.tk = tk
        self.kernel_shape = [None,None]
        self.kernel_ = None
        self.growth_function = None
        self.table = np.random.randint(2, size=(self.table_width, self.table_height))

    def update_channel(self): ...

    def kernel(self, k=None, a=None, b=None, w=None, r=None):

        sigma = 10
        self.kernel_shape[0] = 6*sigma+1
        self.kernel_shape[1] = 6*sigma+1
        self.kernel_ = np.empty(self.kernel_shape)
        radius = 3*sigma

        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1): 
                self.kernel_[x][y] = (1/(2*math.pi*pow(sigma, 2)))*math.exp(-(pow(x, 2)+pow(y, 2))/(2*pow(sigma, 2)))
        #self.kernel_ = self.kernel_/np.sum(self.kernel_)
        self.kernel_ *= 255
        print(self.kernel_)

    def growth(self): ...

class Kernel:
    def __init__(self, k, a, b, w, r):
        ...


m = Main()
m.world()