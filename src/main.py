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
        len = 90
        self.channel.make_kernel_function(m=0.5, s=0.15, kernel_len=27, table_len=len)
        #table inizialitazion
        self.channel.initialize_table(mode="orbium", rows=len, cols=len)

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

            '''Il manager aggiorna la griglia e poi avvia la stampa tramite la GUI'''
            self.channel.update_channel()
        
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