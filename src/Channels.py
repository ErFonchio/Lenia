from tkinter import *
import numpy as np
import scipy
from Kernel import Kernel
from Growth import Growth

class Channel:
    def __init__(self, WIDTH, HEIGHT, tk): 
        self.flag_update = True
        self.WIDTH = WIDTH
        self.height = HEIGHT
        self.table_width = 50
        self.table_height = 50
        self.tk = tk
        self.kernel_shape = [None,None]
        self.kernel = None
        self.growth_function = None
        self.table = None
        self.states = 1
        self.delta = 10 #l'inversa determina l'incremento temporale


    def initialize_table(self, mode=None):
        
        rows = 64
        cols = 64

        w_radius = rows//10
        h_radius = cols//10
        start_row = rows//2-w_radius
        end_row = rows//2+w_radius
        start_col = cols//2-h_radius
        end_col = rows//2+h_radius

        #initialize zero table
        table = np.zeros((rows, cols))
        
        if mode=="orbium":
            cells = np.asarray([[0,0,0,0,0,0,0.1,0.14,0.1,0,0,0.03,0.03,0,0,0.3,0,0,0,0], 
                     [0,0,0,0,0,0.08,0.24,0.3,0.3,0.18,0.14,0.15,0.16,0.15,0.09,0.2,0,0,0,0], 
                     [0,0,0,0,0,0.15,0.34,0.44,0.46,0.38,0.18,0.14,0.11,0.13,0.19,0.18,0.45,0,0,0], 
                     [0,0,0,0,0.06,0.13,0.39,0.5,0.5,0.37,0.06,0,0,0,0.02,0.16,0.68,0,0,0], 
                     [0,0,0,0.11,0.17,0.17,0.33,0.4,0.38,0.28,0.14,0,0,0,0,0,0.18,0.42,0,0], 
                     [0,0,0.09,0.18,0.13,0.06,0.08,0.26,0.32,0.32,0.27,0,0,0,0,0,0,0.82,0,0], 
                     [0.27,0,0.16,0.12,0,0,0,0.25,0.38,0.44,0.45,0.34,0,0,0,0,0,0.22,0.17,0], 
                     [0,0.07,0.2,0.02,0,0,0,0.31,0.48,0.57,0.6,0.57,0,0,0,0,0,0,0.49,0], 
                     [0,0.59,0.19,0,0,0,0,0.2,0.57,0.69,0.76,0.76,0.49,0,0,0,0,0,0.36,0], 
                     [0,0.58,0.19,0,0,0,0,0,0.67,0.83,0.9,0.92,0.87,0.12,0,0,0,0,0.22,0.07], 
                     [0,0,0.46,0,0,0,0,0,0.7,0.93,1,1,1,0.61,0,0,0,0,0.18,0.11], 
                     [0,0,0.82,0,0,0,0,0,0.47,1,1,0.98,1,0.96,0.27,0,0,0,0.19,0.1], 
                     [0,0,0.46,0,0,0,0,0,0.25,1,1,0.84,0.92,0.97,0.54,0.14,0.04,0.1,0.21,0.05], 
                     [0,0,0,0.4,0,0,0,0,0.09,0.8,1,0.82,0.8,0.85,0.63,0.31,0.18,0.19,0.2,0.01], 
                     [0,0,0,0.36,0.1,0,0,0,0.05,0.54,0.86,0.79,0.74,0.72,0.6,0.39,0.28,0.24,0.13,0], 
                     [0,0,0,0.01,0.3,0.07,0,0,0.08,0.36,0.64,0.7,0.64,0.6,0.51,0.39,0.29,0.19,0.04,0], 
                     [0,0,0,0,0.1,0.24,0.14,0.1,0.15,0.29,0.45,0.53,0.52,0.46,0.4,0.31,0.21,0.08,0,0], 
                     [0,0,0,0,0,0.08,0.21,0.21,0.22,0.29,0.36,0.39,0.37,0.33,0.26,0.18,0.09,0,0,0], 
                     [0,0,0,0,0,0,0.03,0.13,0.19,0.22,0.24,0.24,0.23,0.18,0.13,0.05,0,0,0,0], 
                     [0,0,0,0,0,0,0,0,0.02,0.06,0.08,0.09,0.07,0.05,0.01,0,0,0,0,0]])
            
            table[start_row:start_row+cells.shape[0], start_col:start_col+cells.shape[1]] = cells
        else:
            table[start_row:end_row, start_col:end_col] = np.random.rand(end_row-start_row, end_col-start_col)
        
        self.table = table

    def update_channel(self): 
        '''FFT'''
        transformed_kernel = np.fft.fft2(np.fft.fftshift(self.kernel))
        U = np.real(np.fft.ifft2(transformed_kernel * np.fft.fft2(self.table)))
        self.table = np.clip(self.table + (1/self.delta)*self.make_growth_function(m=0.15, s=0.015, U=U), 0, self.states)
        
        '''Classical convolution'''
        #U = scipy.signal.convolve2d(self.table, self.kernel, mode='same', boundary='wrap')
        #self.table = np.clip(self.table + (1/self.delta)*self.make_growth_function(m=0.15, s=0.015, U=U), 0, self.states)

    def update_channel_GOL(self):
        U = scipy.signal.convolve2d(self.table, self.kernel, mode='same', boundary='wrap')
        self.table = self.make_growth_function_GOL(U)
        

    def make_kernel_function(self, m, s, kernel_len, table_len):
        k = Kernel()
        #k.create_2dgaussian_classic(m, s, kernel_len)
        k.create_2dgaussian_classic_fft(m, s, kernel_len, table_len)
        self.kernel = k.kernel

    def make_growth_function(self, m, s, U):
        g = Growth()
        return g.make_bell(m, s, U)
    
    def make_growth_function_GOL(self, table):
        return (self.table & (table==2)) | (table==3)



