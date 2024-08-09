from tkinter import *
import numpy as np
from Kernel import Kernel
from Growth import Growth
import random

class Channel:
    def __init__(self, tk, T): 
        self.flag_update = True
        self.tk = tk
        self.table = None
        self.tempTable = None
        self.states = 1
        self.delta = T #l'inversa determina l'incremento temporale


    def initialize_table(self, rows, cols, table):
        if table == None:
            self.table = np.random.rand(rows,cols)
            self.tempTable = np.zeros(rows, cols)
        else:
            self.table = np.zeros((rows, cols))
            self.tempTable = np.zeros((rows, cols))
            tableRow, tableCol = np.shape(table)
            start_row = (rows - tableRow) // 2
            start_col = (cols - tableCol) // 2

            self.table[start_row:start_row + tableRow, start_col:start_col + tableCol] = table


    def convolveAndGrowChannel(self, growthFunction, kernel, m, s):
        '''FFT'''
        transformed_kernel = np.fft.fft2(np.fft.fftshift(kernel))
        U = np.real(np.fft.ifft2(transformed_kernel * np.fft.fft2(self.table)))
        G = (1/self.delta) * growthFunction(m=m, s=s, U=U)
        return G

    def updateChannel(self, G, weight): 
        self.tempTable += weight*G
    
    def updateChannel2(self):
        self.table = np.clip(self.table+self.tempTable, 0, self.states)
        self.tempTable = np.zeros(np.shape(self.table))
        
    



