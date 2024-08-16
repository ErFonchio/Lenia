import numpy as np
import math
import numpy as np
from Kernel import Kernel
import random as rd
import time
import multiprocessing
import json
import sys

bell = lambda x, m, s: np.exp(-((x-m)/s)**2 / 2)
NUM_EXPERIMENTS = 20000
NUM_FRAME = 200
NUM_KERNELS = 15

class Statistics:
    def __init__(self): 
        self.table = None
        self.tableMass = 0
        self.COM_RGB = [0,0]
        self.vel = [0,0]
        self.LinVel = 0
        self.ang = 0
        self.angularVel = 0
        self.var = 0.0
        self.varVel = 0.0

    def updateStats(self, table):
        self.mass(table)
        self.varianceVelocity(table)
        self.variance(table)
        self.velocity(table) #velocity always before center of mass 
        self.centerOfMass(table)
        self.angularVelocity()
        self.angle()
        
    def mass(self, table):
        self.tableMass = table[0].sum()+table[1].sum()+table[2].sum()

    def centerOfMass(self, table):
        indices = np.indices(table[0].shape)
        actualCOM_R = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]
        actualCOM_G = [np.sum(indices[dim] * table[1]) / self.tableMass for dim in range(table[0].ndim)]
        actualCOM_B = [np.sum(indices[dim] * table[2]) / self.tableMass for dim in range(table[0].ndim)]
        self.COM_RGB = [(actualCOM_R[0]+actualCOM_G[0]+actualCOM_B[0])/3, (actualCOM_R[1]+actualCOM_G[1]+actualCOM_B[1])/3]

    def velocity(self, table):
        '''calculates velocity by confronting the center of mass of two consecutive timesteps'''
        indices = np.indices(table[0].shape)
        actualCOM_R = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]
        actualCOM_G = [np.sum(indices[dim] * table[1]) / self.tableMass for dim in range(table[0].ndim)]
        actualCOM_B = [np.sum(indices[dim] * table[2]) / self.tableMass for dim in range(table[0].ndim)]
        actualCOM_RGB = [(actualCOM_R[0]+actualCOM_G[0]+actualCOM_B[0])/3, (actualCOM_R[1]+actualCOM_G[1]+actualCOM_B[1])/3]

        '''pac-man effect is taken into account'''
        self.vel = [min(abs(actualCOM_RGB[dim] - self.COM_RGB[dim]), table[0].shape[dim]-abs(actualCOM_RGB[dim] - self.COM_RGB[dim])) for dim in range(table[0].ndim)]
        self.LinVel = np.sqrt(self.vel[0]**2 + self.vel[1]**2)
        return self.LinVel
    
    def angle(self):
        self.ang = np.arctan(self.vel[1]/self.vel[0])
    def angularVelocity(self):
        self.angularVel = np.arctan(self.vel[1]/self.vel[0])-self.ang
    def variance(self, channels):
        self.var = np.var([channels[0], channels[1], channels[2]])*1000
        return self.var
    def varianceVelocity(self, channels):
        self.varVel = np.var([channels[0], channels[1], channels[2]])*1000-self.var


class Kernel:
    def __init__(self, weight, c0, c1, m, s):
        self.kernel = None
        self.weight = weight
        self.channelSrc = c0
        self.channelDst = c1
        self.m = m
        self.s = s
    
    def create_2dgaussian_classic_fft(self, R, r, B, table_len):
        # R: kernel radius
        # B: array of kernel's spikes
        # n_distance: normalized distance
        # r: relative radius
        mid = table_len // 2
        R *= 0.9
        self.kernel = np.zeros((table_len, table_len))
        for x in range(-mid, mid):
            for y in range(-mid, mid):
                distance = math.sqrt(x**2 + y**2)
                n_distance = (distance / R*len(B)) / r
                self.kernel[x+mid][y+mid] = (n_distance<len(B)) * B[np.minimum(int(n_distance),len(B)-1)] * np.exp(-((n_distance%1-0.5)/0.15)**2 / 2)# da rivedere
        self.kernel /= np.sum(self.kernel)
        return self.kernel



class Channel:
    def __init__(self, T): 
        self.flag_update = True
        self.table = None
        self.tempTable = None
        self.states = 1
        self.delta = T #l'inversa determina l'incremento temporale

    def initialize_table(self, rows, cols, table):
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
        G = (1/self.delta) * (growthFunction(U, m, s)*2-1)
        return G

    def updateChannel(self, G, weight): 
        self.tempTable += weight*G
    
    def updateChannel2(self):
        self.table = np.clip(self.table+self.tempTable, 0, self.states)
        self.tempTable = np.zeros(np.shape(self.table))


pattern = {"name":"Tessellatium gyrans","R":12,"T":2,"kernels":[
        {"b":[1],"m":0.272,"s":0.0595,"h":0.138,"r":0.91,"c0":0,"c1":0},
        {"b":[1],"m":0.349,"s":0.1585,"h":0.48,"r":0.62,"c0":0,"c1":0},
        {"b":[1,1/4],"m":0.2,"s":0.0332,"h":0.284,"r":0.5,"c0":0,"c1":0},
        {"b":[0,1],"m":0.114,"s":0.0528,"h":0.256,"r":0.97,"c0":1,"c1":1},
        {"b":[1],"m":0.447,"s":0.0777,"h":0.5,"r":0.72,"c0":1,"c1":1},
        {"b":[5/6,1],"m":0.247,"s":0.0342,"h":0.622,"r":0.8,"c0":1,"c1":1},
        {"b":[1],"m":0.21,"s":0.0617,"h":0.35,"r":0.96,"c0":2,"c1":2},
        {"b":[1],"m":0.462,"s":0.1192,"h":0.218,"r":0.56,"c0":2,"c1":2},
        {"b":[1],"m":0.446,"s":0.1793,"h":0.556,"r":0.78,"c0":2,"c1":2},
        {"b":[11/12,1],"m":0.327,"s":0.1408,"h":0.344,"r":0.79,"c0":0,"c1":1},
        {"b":[3/4,1],"m":0.476,"s":0.0995,"h":0.456,"r":0.5,"c0":0,"c1":2},
        {"b":[11/12,1],"m":0.379,"s":0.0697,"h":0.67,"r":0.72,"c0":1,"c1":0},
        {"b":[1],"m":0.262,"s":0.0877,"h":0.42,"r":0.68,"c0":1,"c1":2},
        {"b":[1/6,1,0],"m":0.412,"s":0.1101,"h":0.43,"r":0.82,"c0":2,"c1":0},
        {"b":[1],"m":0.201,"s":0.0786,"h":0.278,"r":0.82,"c0":2,"c1":1}],
        "cells":[
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.49,1.0,0,0.03,0.49,0.49,0.28,0.16,0.03,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.6,0.47,0.31,0.58,0.51,0.35,0.28,0.22,0,0,0,0,0], [0,0,0,0,0,0,0.15,0.32,0.17,0.61,0.97,0.29,0.67,0.59,0.88,1.0,0.92,0.8,0.61,0.42,0.19,0,0,0], [0,0,0,0,0,0,0,0.25,0.64,0.26,0.92,0.04,0.24,0.97,1.0,1.0,1.0,1.0,0.97,0.71,0.33,0.12,0,0], [0,0,0,0,0,0,0,0.38,0.84,0.99,0.78,0.67,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.95,0.62,0.37,0,0], [0,0,0,0,0.04,0.11,0,0.69,0.75,0.75,0.91,1.0,1.0,0.89,1.0,1.0,1.0,1.0,1.0,1.0,0.81,0.42,0.07,0], [0,0,0,0,0.44,0.63,0.04,0,0,0,0.11,0.14,0,0.05,0.64,1.0,1.0,1.0,1.0,1.0,0.92,0.56,0.23,0], [0,0,0,0,0.11,0.36,0.35,0.2,0,0,0,0,0,0,0.63,1.0,1.0,1.0,1.0,1.0,0.96,0.49,0.26,0], [0,0,0,0,0,0.4,0.37,0.18,0,0,0,0,0,0.04,0.41,0.52,0.67,0.82,1.0,1.0,0.91,0.4,0.23,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0.45,0.89,1.0,0.66,0.35,0.09,0], [0,0,0.22,0,0,0,0.05,0.36,0.6,0.13,0.02,0.04,0.24,0.34,0.1,0,0.04,0.62,1.0,1.0,0.44,0.25,0,0], [0,0,0,0.43,0.53,0.58,0.78,0.9,0.96,1.0,1.0,1.0,1.0,0.71,0.46,0.51,0.81,1.0,1.0,0.93,0.19,0.06,0,0], [0,0,0,0,0.23,0.26,0.37,0.51,0.71,0.89,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.42,0.06,0,0,0], [0,0,0,0,0.03,0,0,0.11,0.35,0.62,0.81,0.93,1.0,1.0,1.0,1.0,1.0,0.64,0.15,0,0,0,0,0], [0,0,0,0,0,0,0.06,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.05,0.09,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.28,0.42,0.44,0.34,0.18,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.34,1.0,1.0,1.0,1.0,1.0,0.91,0.52,0.14,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.17,0.75,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.35,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22,0.92,1.0,1.0,1.0,1.0,1.0,1.0,0.59,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.71,0.16], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.67,0.83,0.85,1.0,1.0,1.0,1.0,1.0,1.0,0.68,0.17], [0,0,0,0,0,0,0,0,0,0,0,0,0.21,0.04,0.12,0.58,0.95,1.0,1.0,1.0,1.0,1.0,0.57,0.13], [0,0,0,0,0,0,0,0,0,0,0,0.07,0,0,0,0.2,0.64,0.96,1.0,1.0,1.0,0.9,0.24,0.01], [0,0,0,0,0,0,0,0,0,0,0.13,0.29,0,0,0,0.25,0.9,1.0,1.0,1.0,1.0,0.45,0.05,0], [0,0,0,0,0,0,0,0,0,0,0.13,0.31,0.07,0,0.46,0.96,1.0,1.0,1.0,1.0,0.51,0.12,0,0], [0,0,0,0,0,0,0,0,0.26,0.82,1.0,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.3,0.05,0,0,0], [0,0,0,0,0,0,0,0,0.28,0.74,1.0,0.95,0.87,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.07,0.69,1.0,1.0,1.0,1.0,1.0,0.96,0.25,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.4,0.72,0.9,0.83,0.7,0.56,0.43,0.14,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.25,0.37,0.44,0.37,0.24,0.11,0.04,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.19,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.75,0.4,0.15,0,0,0,0], [0,0,0,0,0,0,0,0,0.14,0.48,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.4,0,0,0,0], [0,0,0,0,0,0,0,0,0.62,0.78,0.94,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0], [0,0,0,0,0,0,0,0.02,0.65,0.98,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.78,0,0,0,0], [0,0,0,0,0,0,0,0.15,0.48,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.79,0.05,0,0,0], [0,0,0,0,0,0,0.33,0.56,0.8,1.0,1.0,1.0,0.37,0.6,0.94,1.0,1.0,1.0,1.0,0.68,0.05,0,0,0], [0,0,0,0,0.35,0.51,0.76,0.89,1.0,1.0,0.72,0.15,0,0.29,0.57,0.69,0.86,1.0,0.92,0.49,0,0,0,0], [0,0,0,0,0,0.38,0.86,1.0,1.0,0.96,0.31,0,0,0,0,0.02,0.2,0.52,0.37,0.11,0,0,0,0], [0,0,0.01,0,0,0.07,0.75,1.0,1.0,1.0,0.48,0.03,0,0,0,0,0,0.18,0.07,0,0,0,0,0], [0,0.11,0.09,0.22,0.15,0.32,0.71,0.94,1.0,1.0,0.97,0.54,0.12,0.02,0,0,0,0,0,0,0,0,0,0], [0.06,0.33,0.47,0.51,0.58,0.77,0.95,1.0,1.0,1.0,1.0,0.62,0.12,0,0,0,0,0,0,0,0,0,0,0], [0.04,0.4,0.69,0.88,0.95,1.0,1.0,1.0,1.0,1.0,0.93,0.68,0.22,0.02,0,0,0.01,0,0,0,0,0,0,0], [0,0.39,0.69,0.91,1.0,1.0,1.0,1.0,1.0,0.85,0.52,0.35,0.24,0.17,0.07,0,0,0,0,0,0,0,0,0], [0,0,0.29,0.82,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.29,0.02,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.2,0.51,0.77,0.96,0.93,0.71,0.4,0.16,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.08,0.07,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
        }

kernelList = []
delta = pattern['T']
radius = pattern['R']
kernelSpecs = pattern['kernels']
tabLen = 128

influence = [(0, 0), (0, 0), (0, 0),
             (1, 1), (1, 1), (1, 1),
             (2, 2), (2, 2), (2, 2),
             (0, 1), (0, 2), (1, 0),
             (1, 2), (2, 0), (2, 1)]
rs = [0.91, 0.62, 0.5, 0.97, 0.72, 0.8, 0.96, 0.56, 0.78, 0.79, 0.5, 0.72, 0.68, 0.82, 0.82]
bs = [[1], [1], [1, 0.25], [0, 1], [1], [round(5/6, 5), 1], [1], [1], [1], [round(11/12, 5), 1], [0.75, 1], [round(11/12, 5), 1], [1], [round(1/6, 5), 1, 0], [1]]
cells = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.49,1.0,0,0.03,0.49,0.49,0.28,0.16,0.03,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0.6,0.47,0.31,0.58,0.51,0.35,0.28,0.22,0,0,0,0,0], [0,0,0,0,0,0,0.15,0.32,0.17,0.61,0.97,0.29,0.67,0.59,0.88,1.0,0.92,0.8,0.61,0.42,0.19,0,0,0], [0,0,0,0,0,0,0,0.25,0.64,0.26,0.92,0.04,0.24,0.97,1.0,1.0,1.0,1.0,0.97,0.71,0.33,0.12,0,0], [0,0,0,0,0,0,0,0.38,0.84,0.99,0.78,0.67,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.95,0.62,0.37,0,0], [0,0,0,0,0.04,0.11,0,0.69,0.75,0.75,0.91,1.0,1.0,0.89,1.0,1.0,1.0,1.0,1.0,1.0,0.81,0.42,0.07,0], [0,0,0,0,0.44,0.63,0.04,0,0,0,0.11,0.14,0,0.05,0.64,1.0,1.0,1.0,1.0,1.0,0.92,0.56,0.23,0], [0,0,0,0,0.11,0.36,0.35,0.2,0,0,0,0,0,0,0.63,1.0,1.0,1.0,1.0,1.0,0.96,0.49,0.26,0], [0,0,0,0,0,0.4,0.37,0.18,0,0,0,0,0,0.04,0.41,0.52,0.67,0.82,1.0,1.0,0.91,0.4,0.23,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0.05,0.45,0.89,1.0,0.66,0.35,0.09,0], [0,0,0.22,0,0,0,0.05,0.36,0.6,0.13,0.02,0.04,0.24,0.34,0.1,0,0.04,0.62,1.0,1.0,0.44,0.25,0,0], [0,0,0,0.43,0.53,0.58,0.78,0.9,0.96,1.0,1.0,1.0,1.0,0.71,0.46,0.51,0.81,1.0,1.0,0.93,0.19,0.06,0,0], [0,0,0,0,0.23,0.26,0.37,0.51,0.71,0.89,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.42,0.06,0,0,0], [0,0,0,0,0.03,0,0,0.11,0.35,0.62,0.81,0.93,1.0,1.0,1.0,1.0,1.0,0.64,0.15,0,0,0,0,0], [0,0,0,0,0,0,0.06,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0.05,0.09,0.05,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.28,0.42,0.44,0.34,0.18,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.34,1.0,1.0,1.0,1.0,1.0,0.91,0.52,0.14,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.17,0.75,1.0,1.0,1.0,1.0,1.0,1.0,0.93,0.35,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.22,0.92,1.0,1.0,1.0,1.0,1.0,1.0,0.59,0.09], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.75,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.71,0.16], [0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.67,0.83,0.85,1.0,1.0,1.0,1.0,1.0,1.0,0.68,0.17], [0,0,0,0,0,0,0,0,0,0,0,0,0.21,0.04,0.12,0.58,0.95,1.0,1.0,1.0,1.0,1.0,0.57,0.13], [0,0,0,0,0,0,0,0,0,0,0,0.07,0,0,0,0.2,0.64,0.96,1.0,1.0,1.0,0.9,0.24,0.01], [0,0,0,0,0,0,0,0,0,0,0.13,0.29,0,0,0,0.25,0.9,1.0,1.0,1.0,1.0,0.45,0.05,0], [0,0,0,0,0,0,0,0,0,0,0.13,0.31,0.07,0,0.46,0.96,1.0,1.0,1.0,1.0,0.51,0.12,0,0], [0,0,0,0,0,0,0,0,0.26,0.82,1.0,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.3,0.05,0,0,0], [0,0,0,0,0,0,0,0,0.28,0.74,1.0,0.95,0.87,1.0,1.0,1.0,1.0,1.0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.07,0.69,1.0,1.0,1.0,1.0,1.0,0.96,0.25,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0.4,0.72,0.9,0.83,0.7,0.56,0.43,0.14,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.25,0.37,0.44,0.37,0.24,0.11,0.04,0,0,0,0], [0,0,0,0,0,0,0,0,0,0.19,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.75,0.4,0.15,0,0,0,0], [0,0,0,0,0,0,0,0,0.14,0.48,0.83,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.4,0,0,0,0], [0,0,0,0,0,0,0,0,0.62,0.78,0.94,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.64,0,0,0,0], [0,0,0,0,0,0,0,0.02,0.65,0.98,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.78,0,0,0,0], [0,0,0,0,0,0,0,0.15,0.48,0.93,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.79,0.05,0,0,0], [0,0,0,0,0,0,0.33,0.56,0.8,1.0,1.0,1.0,0.37,0.6,0.94,1.0,1.0,1.0,1.0,0.68,0.05,0,0,0], [0,0,0,0,0.35,0.51,0.76,0.89,1.0,1.0,0.72,0.15,0,0.29,0.57,0.69,0.86,1.0,0.92,0.49,0,0,0,0], [0,0,0,0,0,0.38,0.86,1.0,1.0,0.96,0.31,0,0,0,0,0.02,0.2,0.52,0.37,0.11,0,0,0,0], [0,0,0.01,0,0,0.07,0.75,1.0,1.0,1.0,0.48,0.03,0,0,0,0,0,0.18,0.07,0,0,0,0,0], [0,0.11,0.09,0.22,0.15,0.32,0.71,0.94,1.0,1.0,0.97,0.54,0.12,0.02,0,0,0,0,0,0,0,0,0,0], [0.06,0.33,0.47,0.51,0.58,0.77,0.95,1.0,1.0,1.0,1.0,0.62,0.12,0,0,0,0,0,0,0,0,0,0,0], [0.04,0.4,0.69,0.88,0.95,1.0,1.0,1.0,1.0,1.0,0.93,0.68,0.22,0.02,0,0,0.01,0,0,0,0,0,0,0], [0,0.39,0.69,0.91,1.0,1.0,1.0,1.0,1.0,0.85,0.52,0.35,0.24,0.17,0.07,0,0,0,0,0,0,0,0,0], [0,0,0.29,0.82,1.0,1.0,1.0,1.0,1.0,1.0,0.67,0.29,0.02,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0.2,0.51,0.77,0.96,0.93,0.71,0.4,0.16,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0.08,0.07,0.03,0,0,0,0,0,0,0,0,0,0,0,0,0]]]

def main(lock, cpu_id, counter):
    
    channels = [Channel(delta), Channel(delta), Channel(delta)]
    f = open("/Users/alessandrococcia/Desktop/Lenia Tesi/src/results1.json", "a")

    for num in range(NUM_EXPERIMENTS):

        stats = Statistics()
        
        '''new random combination'''
        new_pattern = {"name": str(cpu_id)+"-"+str(num), "T": delta, "R": radius, "mass": None, "variance": None, "averageLinearSpeed": None,
                        "averageVariance": None, "averageVarianceSpeed":None, "kernels": [], 
                       "ColorR": None, "ColorG": None, "ColorB": None, "massR": None, "massG": None, "massB": None}
        kernelList = []
        h0 = round(rd.uniform(0, 1), 5)
        h1 = round(rd.uniform(0, 1-h0), 5)
        h2 = round(1-h1-h0, 5)
        h3 = round(rd.uniform(0, 1), 5)
        h4 = round(rd.uniform(0, 1-h3), 5)
        h5 = round(1-h3-h4, 5)
        h6 = round(rd.uniform(0, 1), 5)
        h7 = round(rd.uniform(0, 1-h6), 5)
        h8 = round(1-h7-h6, 5)
        h9 = round(rd.uniform(0, 1), 5)
        h10 = round(1-h9, 5)
        h11 = round(rd.uniform(0, 1), 5)
        h12 = round(1-h11, 5)
        h13 = round(rd.uniform(0, 1), 5)
        h14 = round(1-h13, 5)
        
        H = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14]
        ms = []
        ss = []

        for i in range(NUM_KERNELS):

            m = round(rd.uniform(0.1, 0.5), 5)
            s = round(rd.uniform(0.03, 0.18), 5)
            ms.append(m)
            ss.append(s)

            new_pattern["kernels"].append({"b": bs[i], "m": m, "s": s, "h": H[i], "r": rs[i], "c0": influence[i][0], "c1": influence[i][1]})
        
            kernel = Kernel(weight=H[i], c0=influence[i][0], c1=influence[i][1], m=m, s=s)
            kernel.create_2dgaussian_classic_fft(R=radius, r=rs[i], B=bs[i], table_len=tabLen)
            kernelList.append(kernel)
                

        channels[0].initialize_table(rows=tabLen, cols=tabLen, table=cells[0])
        channels[1].initialize_table(rows=tabLen, cols=tabLen, table=cells[1])
        channels[2].initialize_table(rows=tabLen, cols=tabLen, table=cells[2])

        averageSpeed = 0
        averageVariance = 0
        averageVarianceSpeed = 0

        for _ in range(NUM_FRAME):
            stats.updateStats([channels[0].table, channels[1].table, channels[2].table])
            for r in range(len(kernelList)):
                src = kernelList[r].channelSrc #src index
                dst = kernelList[r].channelDst #dst index
                G = channels[src].convolveAndGrowChannel(kernel=kernelList[r].kernel, growthFunction=bell, m=kernelList[r].m, s=kernelList[r].s)
                channels[dst].updateChannel(G, kernelList[r].weight)
            
            for c in range(len(channels)):
                channels[c].updateChannel2()
            
            averageSpeed += stats.LinVel
            averageVariance += stats.var
            averageVarianceSpeed += stats.varVel
                
        '''what are the results?'''
        R = channels[0].table
        G = channels[1].table
        B = channels[2].table
        area = R.shape[0]*R.shape[1]
        massR = R.sum()
        massG = G.sum()
        massB = B.sum()
        mass = massR+massG+massB
        variance = np.var([R, G, B])
        ColorR, ColorG, ColorB = massR/area, massG/area, massB/area #density of each table
        new_pattern["mass"] = round(mass, 5)
        new_pattern["variance"] = round(variance, 5)
        new_pattern["ColorR"] = round(ColorR, 5)
        new_pattern["ColorG"] = round(ColorG, 5)
        new_pattern["ColorB"] = round(ColorB, 5)
        new_pattern["averageLinearSpeed"] = round(averageSpeed/NUM_FRAME, 5)
        new_pattern["averageVariance"] = round(averageVariance/NUM_FRAME, 5)
        new_pattern["averageVarianceSpeed"] = round(averageVarianceSpeed/NUM_FRAME, 5)

        with lock:
            f.write(json.dumps(new_pattern)+"\n")
            counter.value += 1
            # Stampa il progresso sovrascrivendo la riga precedente
            print(f"\rTask completati: {counter.value}", end="")
            sys.stdout.flush()  # Assicura che la stampa avvenga immediatamente

    f.close()

if __name__ == "__main__":
    processes = []
    num_processes = 8
    lock = multiprocessing.Lock()
    counter = multiprocessing.Value("i", 0)
    
    for n in range(num_processes):
        p = multiprocessing.Process(target=main, args=(lock, n, counter,))
        processes.append(p)

    # Avvia tutti i processi
    start = time.time()
    for p in processes:
        p.start()
    
    # Aspetta che tutti i processi finiscano
    for p in processes:
        p.join()

    end = time.time()

    print("Tutti i processi sono stati completati.")
