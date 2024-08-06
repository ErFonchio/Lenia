from tkinter import *
import numpy as np
from Kernel import Kernel
from Growth import Growth
import random

class Channel:
    def __init__(self, WIDTH, HEIGHT, tk, T): 
        self.flag_update = True
        self.WIDTH = WIDTH
        self.height = HEIGHT
        self.table_width = 50
        self.table_height = 50
        self.tk = tk
        self.table = None
        self.states = 1
        self.delta = T #l'inversa determina l'incremento temporale


    def initialize_table(self, mode, rows, cols, table):
        # if table != None:
        #     self.table = [[random.randint(0,1) for i in range (rows)] for j in range(cols)]
        # else:
        #     self.table = table
        self.table = np.ones((rows, cols))
        
    

    def convolveAndGrowChannel(self, growthFunction, kernel, m, s):
        '''FFT'''
        transformed_kernel = np.fft.fft2(np.fft.fftshift(kernel))
        U = np.real(np.fft.ifft2(transformed_kernel * np.fft.fft2(self.table)))
        G = (1/self.delta)*growthFunction(m=m, s=s, U=U)
        return G

    def updateChannel(self, G, weight): 
        self.table = np.clip(self.table+weight*G, 0, self.states)
    



