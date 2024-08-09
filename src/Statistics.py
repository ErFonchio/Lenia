from tkinter import *
import numpy as np

'''alle stats è lasciato il calcolo delle statistiche'''

class Statistics:
    def __init__(self): 
        self.table = None
        self.tableMass = 0
        self.COM = [0,0]
        self.vel = [0,0]
        self.LinVel = 0
        self.ang = 0
        self.angularVel = 0

    def updateStats(self, table):
        self.mass(table)
        self.velocity(table) #velocity always before center of mass 
        self.centerOfMass(table)
        self.angularVelocity()
        self.angle()
        

    def mass(self, table):
        self.tableMass = table[0].sum()+table[1].sum()+table[2].sum()

    def centerOfMass(self, table):
        indices = np.indices(table[0].shape)
        self.COM = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]

    def velocity(self, table):
        '''calculates velocity by confronting the center of mass of two consecutive timesteps'''
        indices = np.indices(table[0].shape)
        actualCOM = [np.sum(indices[dim] * table[0]) / self.tableMass for dim in range(table[0].ndim)]
        '''pac-man effect is taken into account'''
        self.vel = [min(abs(actualCOM[dim] - self.COM[dim]), table.shape[dim]-abs(actualCOM[dim] - self.COM[dim])) for dim in range(table.ndim)]
        self.LinVel = np.sqrt(self.vel[0]**2 + self.vel[1]**2)
    def angle(self):
        self.ang = np.arctan(self.vel[1]/self.vel[0])
    def angularVelocity(self):
        self.angularVel = np.arctan(self.vel[1]/self.vel[0])-self.ang