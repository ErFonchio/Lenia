from tkinter import *
from Gui import Gui
from Channels import Channel
from Statistics import Statistics
import time
import cProfile
import pstats

WIDTH = 1000
HEIGHT = 600
FPS = 30
TIME = int(1000/FPS)


class Main():
    def __init__(self):
        self.tk = Tk()
        self.kernel_list = []
        self.growth_function = []   
        self.channels = []
        self.table = None
        self.gui = Gui(WIDTH, HEIGHT, FPS, self.tk)
        self.channel = Channel(WIDTH, HEIGHT, self.tk)
        self.stats = Statistics()

        self.start = 0
        self.end = 0

    def world(self):

        '''preprocessing'''
        #kernel initialization
        {"kernel": [{"b":[1],"m":0.272,"s":0.0595,"h":0.138,"r":0.91,"c0":0,"c1":0},
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
        {"b":[1],"m":0.201,"s":0.0786,"h":0.278,"r":0.82,"c0":2,"c1":1}]}
        
        len = 90
        self.channel.make_kernel_function(m=0.5, s=0.15, kernel_len=27, table_len=len)
        #table inizialitazion
        self.channel.initialize_table(mode="aquarium", rows=len, cols=len)

        '''loop manager per gli eventi ciclici'''
        self.manager_loop()
        
        '''mainloop tkinter'''
        self.gui.root.mainloop() 
        

    def manager_loop(self):
        if self.gui.playFlag == 1:
            
            '''fps update'''
            self.end = time.time()
            self.gui.updateFps(1/(self.end-self.start))
            self.start = time.time()

            '''stats update'''
            self.stats.updateStats(self.channel.table)
            self.gui.updateGuiStats(mass=self.stats.tableMass, COM=self.stats.COM, 
                                    vel=self.stats.vel, linVel=self.stats.LinVel, 
                                    angle=self.stats.ang, angularVel=self.stats.angularVel)

            '''Il manager aggiorna la griglia e poi avvia la stampa tramite la GUI'''
            #self.channel.update_channel()
            '''for kernel in listakernel inizializzata:
                - calculate convolution between K and channel i
                - apply growth mapping to the wheighted sums
                - add small portion dt * hk/H of the result to channel j.
            '''
        
            '''il manager avvia il loop della gui'''
            self.gui.mainloop_gui(self.channel.table) #La gui non ha i permessi di modifica sui channel
        
        elif self.gui.playFlag == 2:
            len = 90
            self.channel.initialize_table(mode="orbium", rows=len, cols=len)
            self.gui.playFlag = 1
        
        '''viene richiamata la funzione manager_loop dopo [TIME] tempo'''
        self.gui.root.after(TIME, self.manager_loop)


if __name__ == "__main__":

    '''test per profiling'''
    profiler = cProfile.Profile()
    profiler.enable()
    
    m = Main()
    m.world()

    '''test profiling'''
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
    stats.dump_stats('profile_results.prof')