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
        '''eventi aciclici (preprocessing)'''
        #creazione kernel convoluzione
        self.channel.kernel()
        self.gui.print_table(self.channel.kernel_)

        #creazione funzione di crescita
        self.channel.growth()
        
        
        '''loop manager per gli eventi ciclici'''
        #self.manager_loop(self.channel.kernel_)
        
        
        '''mainloop tkinter'''
        self.gui.root.mainloop()

    def manager_loop(self, table_prova):
        
        #self.gui.mainloop_gui(table_prova)
        self.gui.root.after(TIME, self.manager_loop, table_prova)


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
        
    def print_table(self, raw_table, padx=10, pady=10):
        table, somma = raw_table
        table = self.matrix_scaling(table, 20)
        table = self.color_mapping(table, somma)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(table))
        self.canvas.create_image(padx, pady, anchor="nw", image=self.img)
    
    def color_mapping(self, table, somma):
        #Inverto il processo di normalizzazione rimoltiplicando per la somma dei valori del kernel
        table *= somma
        colored_table = plt.cm.plasma(table)
        colored_table = (colored_table[:, :, :3] * 255).astype(np.uint8)
        return colored_table

    def matrix_scaling(self, matrix, alpha):
        m = np.asarray(matrix)
        matrice_espansa = np.zeros((m.shape[0]*alpha, m.shape[1]*alpha))
        #print(matrice_espansa)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(alpha):
                    for g in range(alpha):
                        matrice_espansa[(i*alpha)+k][(j*alpha)+g] = m[i][j]

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
        #Viene invocata la classe kernel che si occupa di modellare i kernel
        #m=media, s=varianza, len=diametro gaussian-bell
        k = Kernel()
        #self.kernel_ = k.create_2dBell(m=0.5, s=0.15, len=21)
        self.kernel_ = k.create_2dgaussian_classic(m=0.5, s=0.15, len=21)

    def growth(self, m_, s_, U_):
        bell = lambda x, m, s: np.exp(-((x-m)/s)**2 / 2)
        return bell(U_, m_, s_)*2-1


class Kernel:
    def __init__(self):
        self.sigma = None
        self.m = None
        self.len = None
        self.kernel = None
    
    #Funziona
    def create_2dgaussian_classic(self, m, s, len):
        radius = len//2
        K = np.zeros((len, len))
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                distance = math.sqrt(x**2+y**2)
                n_distance = distance / radius
                K[x+radius][y+radius] = np.exp(-((n_distance-m)/s)**2 / 2);  
        
        somma = np.sum(K)
        K /= somma
        return K, somma
    
    #Ritorna il kernel e la somma per la normalizzazione per rinvertire e stampare
    def create_2dBell(self, m, s, len) -> tuple:
        if len==None:
            len = 6*s+1
        R = len//2
        bell = lambda x, m, s: np.exp(-((x-m)/s)**2 / 2)
        x, y = np.ogrid[-R:R, -R:R]
        D = np.sqrt(x**2 + y**2)
        D = D / R
        K = bell(D, m, s)
        print(K)
        somma = np.sum(K)
        self.kernel = K / somma
        return self.kernel, somma
    
    def create_2dRingLikeKernel(self):
        K = np.asarray([[0.5, 0.3, 0.1], [0, 1, 0], [0, 0, 0], [0, 1, 0]])
        return K

    


m = Main()
m.world()