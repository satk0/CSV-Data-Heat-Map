from tkinter import *
from tkinter import filedialog
import seaborn as sbn
import pandas as pd
import matplotlib.pyplot as plt

from main import HeatMapHandler

a= Tk()
a.title('Wizualizacja plików .csv')
a.geometry("600x200")
a.resizable(width=False, height=False)
bg = PhotoImage(file = "uganda.png")
canvas1 = Canvas(a, width = 600,
                 height = 200)
canvas1.pack(fill = "both", expand = True)
canvas1.create_image( 0, 0, image = bg, 
                     anchor = "nw")
canvas1.create_text(300,10,font =("Comic Sans MS", 14),
                    text = "Wybierz plik .csv do utworzenia heatmapy",
                    fill="#FFFF00")


def poka():
    filetypes=(('pliki csv', '*.csv'), ('wszystkie pliki', '*.*'))
    plik1 = filedialog.askopenfile(filetypes=filetypes)
    print("plik", plik1)
    heatmap = HeatMapHandler()
    heatmap.drawHeatMap(plik1)

buton1 = Button(a, text="wybierz plik",width=160,height=32,command=poka)
img1=PhotoImage(file="przycisk1.png")
buton1.config(image=img1)
buton1.place(x=431, y=161)

buton2 = Button(a, text="anuluj",width=160,height=32, command=a.destroy)
img2=PhotoImage(file="przycisk2.png")
buton2.config(image=img2)
buton2.place(x=0, y=160)



a.mainloop()
