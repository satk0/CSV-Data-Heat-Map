import pandas as pd
import numpy as np
from math import ceil
import pathlib

class CSVProcessor:

    MAX_ROWS = 30
    MAX_COLS = 30

    def __init__(self, fname):
        self.nrows = 0
        self.ncols = 0
        self.r_agr = 0
        self.c_agr = 0
        self.r_rem = 0
        self.c_rem = 0
        self.fname = fname


        cur_path = str(pathlib.Path(__file__).parent.absolute())
        fname = cur_path + '/' + fname 
        print("test:")
        print(fname)
        self._preprocess(fname)

    def _preprocess(self, fname: str):
        self.res = pd.read_csv(fname,
                          sep=';',
                          dtype=np.float16,
                          index_col=0,
                          engine='c' 
                          )

        self.nrows, self.ncols = self.res.shape

        ifrows = self.nrows < self.MAX_ROWS
        ifcols = self.ncols < self.MAX_COLS

        self._sum(ifrows, ifcols) 
        self._mean(ifrows, ifcols)

    def _sum(self, ifrows, ifcols):
        if ifrows:
            self.r_agr = ceil(self.nrows / self.MAX_ROWS)
            self.r_rem = self.nrows % self.r_agr
            self.res = self.res.groupby(self.res.index // self.r_agr).sum()

        if not ifcols:
            return

        self.c_agr = ceil(self.ncols / self.MAX_COLS)
        self.c_rem = self.ncols % self.c_agr
        cols = self.res.columns.astype(np.int16)
        self.res = self.res.groupby(cols // self.c_agr, axis=1).sum()


    def _mean(self, ifrows, ifcols):

        # Spaghetti code
        if not ifrows and not ifcols:
            return

        r, c = self.res.shape

        common_dividor = self.r_agr * self.c_agr
        rt_dividor = common_dividor
        lb_dividor = common_dividor

        for i in range(r - 1):
            for j in range(c - 1):
                self.res.values[i][j] /= common_dividor

        # right top
        if self.c_rem:
            rt_dividor = self.c_rem * self.r_agr

        for i in range(r - 1):
            self.res.values[i][-1] /= rt_dividor

        # left bottom
        if self.r_rem:
            lb_dividor = self.r_rem * self.c_agr

        for j in range(c - 1):
            self.res.values[-1][j] /= lb_dividor

        if self.r_rem and self.c_rem: 
            self.res.values[-1][-1] /= (self.r_rem * self.c_rem) 
        elif not self.r_rem and self.c_rem:
            self.res.values[-1][-1] /= lb_dividor
        elif self.r_rem and not self.c_rem:
            self.res.values[-1][-1] /= rt_dividor
        else:
            self.res.values[-1][-1] /= common_dividor






#fname = "11.csv"

#npmain = NpMain(fname)
#npmain.show()
#print("agr: r -", r_agr, " -c- ", c_agr)
