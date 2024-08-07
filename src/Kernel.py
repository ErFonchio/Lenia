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
    
    def create_2dgaussian_classic_fft(self, R, r, B, kernel_len, table_len):
        # R: radius
        # B: array of kernel's spikes
        # n_distance: normalized distance
        # r: relative radius
        mid = table_len // 2
        self.kernel = np.zeros((table_len, table_len))
        for x in range(-mid, mid):
            for y in range(-mid, mid):
                distance = math.sqrt(x**2 + y**2)
                n_distance = (distance / R*len(B)) / r
                self.kernel[x+mid][y+mid] = ((n_distance<len(B)) * B[np.minimum(int(n_distance),len(B)-1)] * np.exp(-((n_distance-0.5)/0.15)**2 / 2))# da rivedere
        self.kernel /= np.sum(self.kernel)
        return self.kernel

