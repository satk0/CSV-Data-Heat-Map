import tkinter as tk
from tkinter import (
    ttk,
    Frame
)
from tkinter.messagebox import showinfo
import seaborn as sbn
import matplotlib
from csvprocessor import CSVProcessor

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('My Awesome App')
        self.geometry('1000x700')
        
        self.graph_frame = Frame(self, width = 600, height = 600)
        self.graph_frame.grid(row=0, column=0)
        self.toolbar_frame = Frame(self, width = 200, height = 700)
        self.toolbar_frame.grid(row=0, column=1)
        
        # label
        self.label = ttk.Label(self.toolbar_frame, text='Hello, Tkinter!')
        self.label.grid(row = 0, column = 0)

        # button
        self.button = ttk.Button(self.toolbar_frame, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.grid(row = 1, column = 0)



    def button_clicked(self):
        fname = "11.csv"
        self.csv_processor = CSVProcessor(fname)
        self._create_figure()
        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



    def _create_figure(self):
        self.figure = Figure(figsize=(6, 6), dpi=100)
        # create axes
        axes = self.figure.add_subplot()
         
        sbn.heatmap(self.csv_processor.res, ax = axes)


        



# JAK OGARNAC ZEBY SIE NIE DODAWALY WYKRESY NIE POTRZEBNIEEE ! ! ! ! ! !
if __name__ == "__main__":
    app = App()
    app.mainloop()
