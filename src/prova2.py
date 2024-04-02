import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

root = tk.Tk()

def scala_matrice(matrice, alfa):
    matrice_espansa = np.repeat(np.repeat(matrice, alfa, axis=0), alfa, axis=1)
    return matrice_espansa

array = np.random.rand(100, 100)*255
array = scala_matrice(array, 2)

img =  ImageTk.PhotoImage(image=Image.fromarray(array))

canvas = tk.Canvas(root,width=1000,height=1000)
canvas.pack()
canvas.create_image(20,20, anchor="center", image=img)

root.mainloop()