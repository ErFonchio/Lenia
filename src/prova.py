from tkinter import *
from PIL import Image,ImageTk
import numpy as np

#Create an instance of tkinter frame
win = Tk()

#Set the geometry of tkinter frame
win.geometry("1000x1000")

#Create a canvas




def print_table(table, root):
        altezza, larghezza = table.shape
        image = Image.new('RGB', (larghezza, altezza))
        for y in range(altezza):
            for x in range(larghezza):
                colore = color_mapping(table[y, x])
                image.putpixel((x, y), colore)


        photo = ImageTk.PhotoImage(image)
        im = ImageTk.PhotoImage(Image.open("Screenshot 2024-04-01 alle 19.33.19.png"))
        canvas = Canvas(root, width=1000, height=1000)

        canvas.create_image(10, 10, image=im, anchor=SW)
        canvas.pack()
        
def color_mapping(value):
        r = int(value * 255)
        b = 255 - r
        colore = (r, 0, b)
        return colore


#Load an image in the script
img= ImageTk.PhotoImage(Image.open("Screenshot 2024-04-01 alle 19.33.19.png"))

#Add image to the Canvas Items
#canvas.create_image(10,10,anchor=NW,image=img)
table = np.random.rand(10, 10)
print_table(table, win)

win.mainloop()

