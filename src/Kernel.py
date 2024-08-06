import numpy as np
import math

class Kernel:
    def __init__(self, weight, c0, c1, m, s):
        self.len = None
        self.kernel = None
        self.weight = weight
        self.channelSrc = c0
        self.channelDst = c1
        self.m = m
        self.s = s
    
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
        # n_distance: normalized distance
        # r: relative radius
        K = np.zeros((kernel_len, kernel_len))
        for x in range(-R, R+1):
            for y in range(-R, R+1):
                distance = math.sqrt(x**2 + y**2)
                n_distance = (distance / R*len(B)) / r
                K[x+R][y+R] = (n_distance<len(B)) * B[np.minimum(int(n_distance),len(B)-1)] * np.exp(-((n_distance-m)/s)**2 / 2) # da rivedere
        somma = np.sum(K)
        K /= somma
        '''initalizing kernel with table_len dimension for fft'''
        self.kernel = np.zeros((table_len, table_len))
        '''putting significative values in the heart of the kernel'''
        self.kernel[table_len//2-R:table_len//2+R+1, table_len//2-R:table_len//2+R+1] = K

        return self.kernel

