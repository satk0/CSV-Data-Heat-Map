from seaborn import heatmap
from pandas import read_csv
from matplotlib.pyplot import show

from tkinter import *
from tkinter import filedialog

a= Tk()
#a.geometry("600x200")

def poka():
    plik1 = filedialog.askopenfile()
    dataset = read_csv(plik1, sep=';', index_col=0)
    #dataset = sbn.load_dataset("glue").pivot("Model", "Task", "Score")
    print(dataset)
    heatmap(dataset)
    show()

buton1 = Button(text="wybierz plik",width=30,command=poka).pack()
#buton1.pack(anchor="w", side=BOTTOM)
buton2 = Button(a,width=30, text="Wypad!", command=a.destroy).pack()
#buton2.pack(anchor="w", side=BOTTOM)


a.mainloop()

