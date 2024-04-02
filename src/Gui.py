from tkinter import *
from PIL import Image, ImageTk
import numpy as np

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

    def mainloop_gui(self, table):

        self.root.maxsize(self.width, self.height)
        mainframe = Frame(self.root, width=self.MAINFRAME_W, height=self.MAINFRAME_H, bg="blue")
        mainframe.grid(row=0, column=0, padx=5, pady=10)
        secondframe = Frame(self.root, width=self.SECONDFRAME_W, height=self.SECONDFRAME_H, bg="lightblue")
        secondframe.grid(row=0, column=1, padx=5, pady=10)

        self.print_table(table, mainframe)

        
    def print_table(self, table, window):
        table = self.matrix_scaling(table, 2)
        img =  ImageTk.PhotoImage(image=Image.fromarray(table))
        canvas = Canvas(window, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        
        #label = Label(window, image = img)
        #label.pack()

        #canvas.pack()
        #canvas.create_image(10, 10, anchor="center", image=img)
        print("ok")
        
    def color_mapping(self, value):
        r = int(value * 255)
        b = 255 - r
        colore = (r, 0, b)
        return colore

    def matrix_scaling(self, matrix, alfa):
        matrice_espansa = np.repeat(np.repeat(matrix, alfa, axis=0), alfa, axis=1)
        return matrice_espansa
