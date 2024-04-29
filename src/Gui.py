from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt


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
        self.print_table(table, fit=False)
        
    def print_table(self, table, padx=10, pady=10, fit=False):
        scale_size_width = 5
        scale_size_height = 5
        if fit:
            scale_size_width = int((self.MAINFRAME_W)//len(table))
            scale_size_height = int((self.MAINFRAME_H)//len(table[0]))

        scaled_table = self.matrix_scaling(table, alpha_w=scale_size_width, alpha_h=scale_size_height)
        table = self.color_mapping(scaled_table)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(table))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)

    def print_kernel(self, kernel, padx=10, pady=10):
        kernel = self.matrix_scaling(kernel, 30, 30)
        kernel = self.color_mapping(kernel)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(kernel))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def color_mapping(self, table):
        colored_table = plt.cm.plasma(table)
        colored_table = (colored_table[:, :, :3] * 255).astype(np.uint8)
        return colored_table

    def matrix_scaling(self, matrix, alpha_w, alpha_h):
        m = matrix

        matrice_espansa = np.zeros((m.shape[0]*alpha_w, m.shape[1]*alpha_h))
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(alpha_w):
                    for g in range(alpha_h):
                        matrice_espansa[(i*alpha_w)+k][(j*alpha_h)+g] = m[i][j]

        return matrice_espansa

