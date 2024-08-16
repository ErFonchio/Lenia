from tkinter import *
import numpy as np

'''alle stats è lasciato il calcolo delle statistiche'''

class Statistics:
    def __init__(self): 
        self.table = None
        self.tableMass = 0
        self.COM_RGB = [0,0]
        self.vel = [0,0]
        self.LinVel = 0
        self.ang = 0
        self.angularVel = 0
        self.var = 0
        self.varVel = 0

    def updateStats(self, table):
        self.mass(table)
        self.variance(table)
        self.varianceVelocity(table)
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
        self.var = np.var([channels[0], channels[1], channels[2]])
        return self.var
    def varianceVelocity(self, channels):
        self.varVel = np.var([channels[0], channels[1], channels[2]])-self.var
        return self.varVel


