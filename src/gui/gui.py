import tkinter as tk
from tkinter import (
    ttk,
    Frame
)
from tkinter import filedialog
import seaborn as sbn
import matplotlib
from matplotlib.patches import Rectangle
import pathlib

from ..back.csvprocessor import CSVProcessor

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from math import ceil, floor

class App(tk.Tk):

    METHODS = {
        "Średnia": 'mean',
        "Max": 'max',
        "Min": 'min',
        "Suma": 'sum'
    }
    COLORS = {
        "flare": ["rocket", "rocket_r"]
    }

    def __init__(self):
        super().__init__()


        self.csv_processor = None
        self.cur_color = 'flare'
        self.is_color_reversed = 0

        self.pressed = False
        self.pos = [0, 0]
        self.rec_patch = None
        self.fpath = ''

        self.cur_method = 'mean'

        self.origin = [0, 0]
        
        # graph width and height in pixels
        self.graph_mes = [700, 600]
        #                   x0  y0   x1  y1
        self.graph_rect = [0.1, 0.1, 0.8, 0.95]

        self.prev_csv_procs = []

        self.title('CSV Heat Map')
        self.geometry('1000x700')

        # Frames
        self.graph_frame = Frame(self, width = self.graph_mes[0], height = self.graph_mes[1])
        self.graph_frame.grid(row=0, column=0)

        self.graph_tool_frame = Frame(self, width = 100, height = 100)
        self.graph_tool_frame.grid(row=1, column=0)

        self.toolbar_frame = Frame(self, width = 200, height = 700)
        self.toolbar_frame.grid(row=0, column=1)
        
        # labels
        self.fname_label = ttk.Label(self.toolbar_frame, text='')
        self.fname_label.grid(row = 0, column = 0)
        self.info_label = ttk.Label(self.toolbar_frame, text='')
        self.info_label.grid(row = 2, column = 0)
        self.loading_label = ttk.Label(self.graph_tool_frame, text='Ładowanie...')
        self.color_label = ttk.Label(self.toolbar_frame, text='Kolor:')
        self.save_label = ttk.Label(self.toolbar_frame, text='')

        # buttons
        self.load_button = ttk.Button(self.toolbar_frame, text='Załaduj plik')
        self.load_button['command'] = self.button_clicked
        self.load_button.grid(row = 1, column = 0)

        # under graph
        self.back_button = ttk.Button(self.graph_tool_frame, text='Cofnij', command=self.back_csv_proc)

        # switch colors button
        self.switch_button = ttk.Button(self.toolbar_frame)
        self.switch_button['command'] = self.switch_btn_clicked

        # save to png file button
        self.save_button = ttk.Button(self.toolbar_frame)
        self.save_button['command'] = self.save_btn_clicked

        # combobox
        self.agregation = tk.StringVar()
        self.agr_chosen = ttk.Combobox(self.toolbar_frame, state="readonly",width=20, textvariable=self.agregation)

        self.agr_chosen['values'] = ('Suma',
                                     'Średnia',
                                     'Max',
                                     'Min')

        self.agr_chosen.set('Średnia')
        self.agregation.trace('w', self.on_combobox_changed)

    def save_btn_clicked(self):
        self.figure.savefig(self.fname + '.png')
        self.save_label['text'] = 'zapisano zdjecie!'


    def switch_btn_clicked(self):
        if self.is_color_reversed:
            self.is_color_reversed = 0 
            self.switch_button['text'] = "Normalny"
        else: 
            self.is_color_reversed = 1
            self.switch_button['text'] = "Odwrócony"

        if self.fpath != '':
            for widgets in self.graph_frame.winfo_children():
                  widgets.destroy()

        self._draw_figure()

    def on_combobox_changed(self, *args):
        chosen = self.agregation.get()
        self.cur_method = App.METHODS[chosen]
        # reset
        # self.prev_csv_procs = []
        if not self.csv_processor:
            return
        
        limits, prev_params = self.csv_processor.limits, self.csv_processor.prev_params
        del self.prev_csv_procs[-1]

        self.load_heatmap(self.fpath, limits, prev_params)


    def mouse_pressed(self, event):
        self.pressed = True

    def mouse_released(self, event):
        
        if not self.csv_processor: return 

        rect_y = [self.rect_oy, self.rect_oy + self.rect_height]
        min_rows, max_rows = floor(min(rect_y)), ceil(max(rect_y))
        print("min_rows, max_rows:")
        print(min_rows, max_rows)
        
        rect_x = [self.rect_ox, self.rect_ox + self.rect_width]
        min_cols, max_cols = floor(min(rect_x)), ceil(max(rect_x))

        print("min_cols, max_cols")
        print(min_cols, max_cols)
        self.load_heatmap(
                self.fpath,
                [
                    min_rows, max_rows,
                    min_cols, max_cols
                ],
                self.csv_processor.get_params()
        )

        self.origin = [0, 0]
        self.pressed = False

    def button_clicked(self):

        if self.rec_patch is not None:
            self.rec_patch.remove()
            self.rec_patch = None
            self.figure_canvas.draw()
        
            
        cur_path = str(pathlib.Path(__file__).parent.absolute().parent)
        fpath = filedialog.askopenfilename(initialdir = cur_path, 
                                           title = "Wybierz Plik",
                                           filetypes = (("Text files", "*.csv"), ("all files", "*.*")))
        if not fpath: return
        if fpath == self.fpath: return 
        
        self.agr_chosen.set('Średnia')
        self.agr_chosen.grid(row=3, column=0)
        self.color_label.grid(row=4, column=0)
        self.switch_button['text'] = "Normalny"
        self.switch_button.grid(row=5, column=0)
        self.save_button['text'] = "Zapisz"
        self.save_button.grid(row=6, column=0)
        self.save_label.grid(row=7, column=0)

        # reset important values 
        self.cur_method = 'mean'
        self.is_color_reversed = 0
        self.prev_csv_procs = []

        self.load_heatmap(fpath)

        print("agregacja:", self.agregation.get())

        self.fname = pathlib.Path(fpath).stem
        fname = self.fname
        if len(fname) > 35:
            fname = fname[:16] + '...' + fname[-16:]
        # 35

        self.fname_label['text'] = "Nazwa bieżącego pliku:\n" + fname
        #self.back_button['text'] = "Cofnij"
        
    def back_csv_proc(self):
        self.load_heatmap(fpath = self.fpath, back = True)
                                # [rmin, rmax, cmin, cmax] # [r_agr, r_rem, c_agr, c_rem]
    def load_heatmap(self, fpath, limits = [], prev_params = [], back = False):

        if self.fpath != '':
            for widgets in self.graph_frame.winfo_children():
                  widgets.destroy()

        self.fpath = fpath

        # future idea: if reapeat parameter is to true, repeat heatmap(regenerate)


        if not back:
            self.loading_label.grid(row=0, column=0)
            self.csv_processor = CSVProcessor(self.fpath, limits, prev_params, self.cur_method)
            self.prev_csv_procs.append(self.csv_processor)
            self.loading_label.grid_forget()
        else:
            del self.prev_csv_procs[-1]
            self.csv_processor = self.prev_csv_procs[-1]

            if (self.csv_processor.method != self.cur_method):
                limits, prev_params = self.csv_processor.limits, self.csv_processor.prev_params
                self.csv_processor = CSVProcessor(self.fpath, limits, prev_params, self.cur_method)
                self.prev_csv_procs[-1] = self.csv_processor


        if len(self.prev_csv_procs) > 1:
            self.back_button.grid(row = 0, column = 0)
        else:
            self.back_button.grid_forget() 

        print("self.prev_csv_procs")
        print(self.prev_csv_procs)

        self._draw_figure()


    def _draw_figure(self):

        # reset text on button
        self.save_label['text'] = ''
        
        self._create_figure()

        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.figure_canvas.draw()

        self.figure_canvas.get_tk_widget().bind('<Button-1>', self.mouse_pressed)
        self.figure_canvas.get_tk_widget().bind('<ButtonRelease-1>', self.mouse_released)
        self.figure_canvas.get_tk_widget().bind('<Motion>', self._mouse_hold)

        self.heatmap_info()


    def _mouse_hold(self, event):

        if not self.pressed:
            return

        self.pos = [event.x, self.graph_mes[1] - event.y]


        if self.pos[0] < self.graph_rect[0] * self.graph_mes[0]:
            self.pos[0] = self.graph_rect[0] * self.graph_mes[0]
        elif self.pos[0] > self.graph_rect[2] * self.graph_mes[0]:
            self.pos[0] = self.graph_rect[2] * self.graph_mes[0]
        if self.pos[1] < self.graph_rect[1] * self.graph_mes[1]:
            self.pos[1] = self.graph_rect[1] * self.graph_mes[1]
        elif self.pos[1] > self.graph_rect[3] * self.graph_mes[1]:
            self.pos[1] = self.graph_rect[3] * self.graph_mes[1]

        print("self.pos:")
        print(self.pos)

        if 0 in self.origin:
            self.origin = self.pos.copy()
            print("origin pos:")
            print(self.origin)

        self.mouse_selection()


    def mouse_selection(self):

        if not self.csv_processor:
            return 

        print("self.csv_processor.tr_ncols:")
        print(self.csv_processor.tr_ncols)
        print("self.csv_processor.tr_nrows")
        print(self.csv_processor.tr_nrows)
        self.rect_ox = self.csv_processor.tr_ncols * (self.origin[0] - self.graph_rect[0] * self.graph_mes[0]) 
        self.rect_ox /= ((self.graph_rect[2] - self.graph_rect[0]) * self.graph_mes[0])

        print("self.csv_processor")
        print(self.csv_processor.tr_nrows)
        print("self.rect_ox")
        print(self.rect_ox)

        self.rect_oy = self.csv_processor.tr_nrows * (self.origin[1] - self.graph_rect[1] * self.graph_mes[1])
        self.rect_oy /= ((self.graph_rect[3] - self.graph_rect[1]) * self.graph_mes[1])
        self.rect_oy = self.csv_processor.tr_nrows - self.rect_oy

        self.rect_width = self.csv_processor.tr_ncols * (self.pos[0] - self.origin[0]) 
        self.rect_width /= ((self.graph_rect[2] - self.graph_rect[0]) * self.graph_mes[0])

        self.rect_height = self.csv_processor.tr_nrows * -(self.pos[1] - self.origin[1]) 
        self.rect_height /= ((self.graph_rect[3] - self.graph_rect[1]) * self.graph_mes[1])

        if self.rec_patch is not None:
            self.rec_patch.remove()

        self.rec_patch = Rectangle(
                (
                    self.rect_ox, 
                    self.rect_oy
                ),
                self.rect_width,
                self.rect_height, 
                fc = 'none',
                color="green",
                linewidth = 5
                )

        self.axes.add_patch(self.rec_patch)
        self.figure_canvas.draw()

    def heatmap_info(self):

        if not self.csv_processor: return

        mtext = "Informacje o heatmapie:\n\n" 
        mtext += "Oryginalnie:\n"
        mtext += "ilosc wierszy: " 
        mtext += str(self.csv_processor.nrows) + "\nilosc kolumn: " 
        mtext += str(self.csv_processor.ncols) + "\n"
        mtext += "\n Po transformacji:\n"
        mtext += "ilosc wierszy: " 
        mtext += str(self.csv_processor.tr_nrows) + '\n'
        mtext += "ilosc kolumn: " 
        mtext += str(self.csv_processor.tr_ncols) + "\n"
        mtext += "\nIlość oryginalnych wieszy na wysokość:" 
        mtext += str(self.csv_processor.r_agr) + '\n'
        mtext += "(Ostatni wiersz: " 
        mtext += str(self.csv_processor.r_rem) + ")\n"
        mtext += "\nIlość oryginalnych kolumn na szerokość:" 
        mtext += str(self.csv_processor.c_agr) + "\n"
        mtext += "(Ostatnia kolumna: " 
        mtext += str(self.csv_processor.c_rem) + ")\n"
        self.info_label.config(text = mtext)

    def _create_figure(self):
        # should not be used alone, better call: self._draw_figure()
        if not self.csv_processor: return

        self.figure = Figure(figsize=(self.graph_mes[0]/100, self.graph_mes[1]/100), dpi=100)
        # create axes
        ax_rect = self.graph_rect.copy()
        ax_rect[2] -= ax_rect[0]
        ax_rect[3] -= ax_rect[1]
        print(ax_rect)

        self.axes = self.figure.add_axes(ax_rect)
        print("rect:", self.graph_rect[2])
        colorbar_ax = self.figure.add_axes(
                [
                    self.graph_rect[2] + 0.02, 
                    self.graph_rect[1],
                    0.08, 
                    self.graph_rect[3] - self.graph_rect[1]
                 ]
        )

        print("cmap:", App.COLORS[self.cur_color][self.is_color_reversed])
        sbn.heatmap(
                self.csv_processor.res,
                cmap = App.COLORS[self.cur_color][self.is_color_reversed],
                cbar_ax = colorbar_ax,
                ax = self.axes,
            )

        print("pos:")
        print("bottom-left:")
        print("x =", self.graph_rect[0] * self.graph_mes[0], "| y =", self.graph_rect[1] * self.graph_mes[1])
        print("top-right:")
        print("x = ", self.graph_rect[2] * self.graph_mes[0], "| y = ", self.graph_rect[3] * self.graph_mes[1])


if __name__ == "__main__":
    app = App()
    app.mainloop()
