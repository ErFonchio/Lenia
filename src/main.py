from tkinter import *
from Gui import Gui
from Channels import Channel

WIDTH = 1000
HEIGHT = 600
FPS = 120
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

    def world(self):
        '''eventi aciclici (preprocessing)'''
        #kernel initialization
        self.channel.make_kernel_function(m=0.5, s=0.15, kernel_len=27, table_len=64)
        #table inizialitazion
        self.channel.initialize_table(mode="orbium")

        '''loop manager per gli eventi ciclici'''
        self.manager_loop()
        
        '''mainloop tkinter'''
        self.gui.root.mainloop() 

    def manager_loop(self):

        '''Il manager aggiorna la griglia e poi avvia la stampa tramite la GUI'''
        self.channel.update_channel()
        
        '''il manager avvia il loop della gui'''
        self.gui.mainloop_gui(self.channel.table) #La gui non ordina/manipola i channel, gli viene dato tutto dal manager

        '''viene richiamata la funzione manager_loop dopo [TIME] tempo'''
        self.gui.root.after(TIME, self.manager_loop)


        
m = Main()
m.world()