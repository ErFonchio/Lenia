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


    def initialize_table(self, mode="aquarium", rows=64, cols=64):
        table = np.zeros((rows, cols))

        '''3 channels -> table of dimension 2*2*3'''
        '''adjacency matrix 3*3 (a channel can communicate with itself or with other two)'''
        '''array of kernels'''
        '''each kernel has relative radius, parameter Bk, source channel i, destination channel j,
        corresponding growth function with parameter m and s.'''

        '''for each kernel k:
            - calculate convolution between K and channel i
            - apply growth mapping to the wheighted sums
            - add small portion of the result to channel j.
        '''

        self.table = table

    def update_channel(self): 
        '''FFT'''
        transformed_kernel = np.fft.fft2(np.fft.fftshift(self.kernel))
        U = np.real(np.fft.ifft2(transformed_kernel * np.fft.fft2(self.table)))
        self.table = np.clip(self.table + (1/self.delta)*self.make_growth_function(m=0.15, s=0.015, U=U), 0, self.states)
        
        
    def update_channel_GOL(self):
        U = scipy.signal.convolve2d(self.table, self.kernel, mode='same', boundary='wrap')
        self.table = self.make_growth_function_GOL(U)
        

    def make_kernel_function(self, m, s, kernel_len, table_len):
        k = Kernel()
        k.create_2dgaussian_classic_fft(m, s, kernel_len, table_len)
        self.kernel = k.kernel

    def make_growth_function(self, m, s, U):
        g = Growth()
        return g.make_bell(m, s, U)
    
    def make_growth_function_GOL(self, table):
        return (self.table & (table==2)) | (table==3)



