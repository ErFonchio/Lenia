from tkinter import *
import numpy as np

class Statistics:
    def __init__(self): 
        self.table = None
        self.tableMass = 0
        self.COM_RGB = [0,0]
        self.vel = [0,0]
        self.LinVel = 0
        self.linVelLowFilter = 0.0
        self.angularVelLowFilter = 0.0
        self.varVelLowFilter = 0.0
        self.filterConstant = 0.2
        self.ang = 0
        self.angularVel = 0
        self.var = 0.0
        self.varVel = 0.0

    def updateStats(self, table):
        self.mass(table)
        self.varianceVelocity(table)
        self.variance(table)
        self.velocity(table) #velocity always before center of mass 
        self.velocityLowFilter()
        self.centerOfMass(table)
        self.angularVelocity()
        self.angularVelocityLowFilter()
        self.angle()

    def velocityLowFilter(self):
        if self.tableMass > 0.01:
            self.linVelLowFilter = self.linVelLowFilter + self.filterConstant * (self.LinVel - self.linVelLowFilter)
        else:
            self.linVelLowFilter = 0

    def angularVelocityLowFilter(self):
        if self.tableMass > 0.01:
            self.angularVelLowFilter = self.angularVelLowFilter + self.filterConstant * (self.angularVel - self.angularVelLowFilter)
        else:
            self.angularVelLowFilter = 0

    def varianceVelocityLowFilter(self):
        if self.tableMass > 0.01:
            '''(1 - constant) * old + constant * new'''
            self.varVelLowFilter = self.varVelLowFilter + self.filterConstant * (self.varVel - self.varVel)
        else:
            self.varVelLowFilter = 0
    def mass(self, table):
        self.tableMass = table[0].sum()+table[1].sum()+table[2].sum()

    def centerOfMass(self, table):
        if self.tableMass > 0.01:
            indices = np.indices(table[0].shape)
            actualCOM_R = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]
            actualCOM_G = [np.sum(indices[dim] * table[1]) / self.tableMass for dim in range(table[0].ndim)]
            actualCOM_B = [np.sum(indices[dim] * table[2]) / self.tableMass for dim in range(table[0].ndim)]
            self.COM_RGB = [(actualCOM_R[0]+actualCOM_G[0]+actualCOM_B[0])/3, (actualCOM_R[1]+actualCOM_G[1]+actualCOM_B[1])/3]
        else:
            self.COM_RGB = [0,0]

    def velocity(self, table):
        '''calculates velocity by confronting the center of mass of two consecutive timesteps'''
        indices = np.indices(table[0].shape)
        if self.tableMass > 0.01:
            actualCOM_R = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]
            actualCOM_G = [np.sum(indices[dim] * table[1]) / self.tableMass for dim in range(table[0].ndim)]
            actualCOM_B = [np.sum(indices[dim] * table[2]) / self.tableMass for dim in range(table[0].ndim)]
            actualCOM_RGB = [(actualCOM_R[0]+actualCOM_G[0]+actualCOM_B[0])/3, (actualCOM_R[1]+actualCOM_G[1]+actualCOM_B[1])/3]

            '''pac-man effect is taken into account'''
            self.vel = [actualCOM_RGB[dim] - self.COM_RGB[dim] for dim in range(table[0].ndim)]
            self.LinVel = np.sqrt(self.vel[0]**2 + self.vel[1]**2)
            return self.LinVel
        else:
            self.vel = [0,0]
            self.LinVel = 0
            return self.LinVel
    
    def angle(self):
        self.ang = np.degrees(np.arctan2(self.vel[1], self.vel[0]))%360

    def angularVelocity(self):
        if self.mass != 0:
            new_ang = np.degrees(np.arctan2(self.vel[1], self.vel[0]))%360
            delta_ang = new_ang - self.ang
            if delta_ang < -180:
                delta_ang += 360
            elif delta_ang > 180:
                delta_ang -= 360
            self.angularVel = delta_ang
        else:
            self.angularVel = 0

    def variance(self, channels):
        self.var = np.var([channels[0], channels[1], channels[2]])*1000
        return self.var
    def varianceVelocity(self, channels):
        self.varVel = np.var([channels[0], channels[1], channels[2]])*1000-self.var

