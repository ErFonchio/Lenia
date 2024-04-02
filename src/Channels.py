from tkinter import *
import numpy as np

class Channel:
    def __init__(self, WIDTH, HEIGHT, tk): 
        self.flag_update = True
        self.WIDTH = WIDTH
        self.height = HEIGHT
        self.tk = tk
        self.kernel_ = None
        self.growth_function = None
        self.table = np.random.randint(2, size=(WIDTH, HEIGHT))

    def update_channel(self): ...

    def kernel(self):
        self.kernel_ = np.random.rand(100, 100)*255
    
    def growth(self): ...


