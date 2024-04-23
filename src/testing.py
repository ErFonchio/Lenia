import sys
from tkinter import *
import math
from Channels import Channel
import time
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

'''kernels'''

def matrix_scaling(matrix, alpha):
        print(matrix)
        matrix = np.array(matrix)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                print(matrix[i][j], end="")
            print()

        return matrix

def print_table(table, canvas):
        table = matrix_scaling(table, 5)
        table = color_mapping(table)
        img =  ImageTk.PhotoImage(image=Image.fromarray(table).convert('RGB'))
        canvas.create_image(0, 0, anchor="nw", image=img)

def create_2dBell(self, m, s):
        radius = self.len//2
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                r = math.sqrt(pow(x, 2)+pow(y, 2))
                print("x, y: ", x, y, "r :", r)
                kernel[x+radius][y+radius] = np.exp(-((r-m)/s)**2 / 2)

        return kernel

def color_mapping(table):
        colors = [(1, 1, 1), (0, 0, 0)] #grigi
        cmap = mcolors.LinearSegmentedColormap.from_list("my_colormap", colors)
        
        # Apply the colormap to the normalized table
        colored_table = cmap(table)
        
        # Convert to RGB values in the range [0, 255]
        colored_table = (colored_table[:, :, :3] * 255).astype(np.uint8)
        
        return colored_table

def create_2dRingLikeKernel():
        K = np.asarray([
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]])
        return K

tk = Tk()
img = None
canvas = Canvas(tk, width=100, height=100)
canvas.pack()
kernel = create_2dRingLikeKernel()
print_table(kernel, canvas)

tk.mainloop()