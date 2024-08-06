import numpy as np
import math

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
                distance = math.sqrt(x**2 + y**2)
                n_distance = distance / radius
                K[x+radius][y+radius] = np.exp(-((n_distance-m)/s)**2 / 2)
        
        somma = np.sum(K)
        K /= somma
        self.kernel = K
        return K, somma
    
    def create_2dgaussian_classic_fft(self, m, s, R, r, B, kernel_len, table_len):
        # R: radius
        # B: array of kernel's spikes
        K = np.zeros((kernel_len, kernel_len))
        for x in range(-R, R+1):
            for y in range(-R, R+1):
                distance = math.sqrt(x**2 + y**2)
                n_distance = distance / R*len(B)
                K[x+R][y+R] = np.exp(-((n_distance-m)/s)**2 / 2)
        
        somma = np.sum(K)
        K /= somma
        '''initalizing kernel with table_len dimension for fft'''
        self.kernel = np.zeros((table_len, table_len))
        '''putting significative values in the heart of the kernel'''
        self.kernel[table_len//2-R:table_len//2+R+1, table_len//2-R:table_len//2+R+1] = K

        return self.kernel, somma

    def create_2dGameOfLifeKernel(self):
        self.kernel = [[1,1,1], [1,0,1], [1,1,1]]
