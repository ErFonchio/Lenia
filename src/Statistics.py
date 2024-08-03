from tkinter import *
import numpy as np

'''alle stats è lasciato il calcolo delle statistiche'''

class Statistics:
    def __init__(self): 
        self.table = None
        self.tableMass = 0
        self.COM = [0,0]
        self.vel = [0,0]

    def updateStats(self, table):
        self.mass(table)
        self.velocity(table) #velocity always before center of mass 
        self.centerOfMass(table)
        print("Mass: ", self.tableMass, "Center of Mass: ", self.COM, "Velocity: ", self.vel)

    def mass(self, table):
        self.tableMass = table.sum()

    def centerOfMass(self, table):
        indices = np.indices(table.shape)
        self.COM = [np.sum(indices[dim] * table) / self.tableMass for dim in range(table.ndim)]
        if self.COM[0] > table.shape[0]:
            print(self.COM[0])
            exit(0)

    def velocity(self, table):
        '''calculates velocity by confronting the center of mass of two consecutive timesteps'''
        indices = np.indices(table.shape)
        actualCOM = [np.sum(indices[dim] * table) / self.tableMass for dim in range(table.ndim)]
        '''pac-man effect is taken into account'''
        self.vel = [min(abs(actualCOM[dim] - self.COM[dim]), table.shape[dim]-abs(actualCOM[dim] - self.COM[dim])) for dim in range(table.ndim)]