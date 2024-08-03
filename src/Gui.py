from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import cv2


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
        self.mainframe = Frame(self.root, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.mainframe.grid(row=0, column=0, padx=10, pady=10)
        
        self.secondframe = Frame(self.root, width=self.SECONDFRAME_W, height=self.SECONDFRAME_H, bg="white")
        self.secondframe.grid(row=0, column=1, padx=10, pady=10)
        #self.initialize_secondwindow()
        
        self.img = None
        self.canvas = Canvas(self.mainframe, width=self.MAINFRAME_W, height=self.MAINFRAME_H)
        self.canvas.pack()

    def mainloop_gui(self, table):
        self.print_table(table, fit=False)
        
    def print_table(self, table, padx=10, pady=10, fit=False):
        zoom = 5
        scaled_table = np.kron(table, np.ones((zoom, zoom)))
        table = self.color_mapping(scaled_table)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(table))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)

    def print_kernel(self, kernel, padx=10, pady=10):
        kernel = self.matrix_scaling(kernel, 30, 30)
        kernel = self.color_mapping(kernel)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(kernel))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def color_mapping(self, table):
        # Normalizza la tabella dei valori tra 0 e 255
        norm_table = (table*255).astype(np.uint8)
        
        # Applica la mappa dei colori plasma
        colored_table = cv2.applyColorMap(norm_table, cv2.COLORMAP_INFERNO)

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

    def initialize_secondwindow(self):
        
        self.initialize_speciesmenu()

    def initialize_speciesmenu(self):
        menubar = Menu(self.secondframe)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")

        # Aggiungi il menu filemenu alla barra dei menu
        menubar.add_cascade(label="File", menu=filemenu)

        self.secondframe.config(menu=menubar)
