import pandas as pd
import numpy as np
from math import ceil
import pathlib

class CSVProcessor:

    MAX_ROWS = 30
    MAX_COLS = 30
                                           # self.r_agr, self.r_rem, self.c_agr, self.c_rem
    def __init__(self, fname, limits = [], prev_params = [], method='mean'):
        self.method = method
        self.nrows = 0
        self.ncols = 0
        self.r_agr = 1
        self.c_agr = 1
        self.r_rem = 1
        self.c_rem = 1
        self.tr_nrows = 0
        self.tr_ncols = 0
        self.fname = fname
        self.limits = limits
        self.prev_params = prev_params

        if prev_params:
            self.r_agr = prev_params[0]
            self.r_rem = prev_params[1]
            self.c_agr = prev_params[2]
            self.c_rem = prev_params[3]

        # check if absolute
        if len(fname.split('/\\')) != 1:
            cur_path = str(pathlib.Path(__file__).parent.absolute())
            fname = cur_path + '/' + fname 

        self._preprocess(fname)

    def _preprocess(self, fname: str):

        #print("self.limits:")
        #print(self.limits)

        min_rows = None
        max_rows = None
        max_cols = 0

        if self.limits:
            
            min_rows = self.limits[0] * self.r_agr
            max_rows  = (self.limits[1] - 1) * self.r_agr

            if self.limits[1] == self.tr_nrows and self.r_rem:
                max_rows += self.r_rem 
            else:
                max_rows += self.r_agr

            max_cols  = (self.limits[3] - 1) * self.c_agr

            if self.limits[3] == self.tr_ncols and self.c_rem:
                max_cols += self.c_rem
            else:
                max_cols += self.c_agr

                
        print("min_rows:", min_rows)
        print("max_rows:", max_rows)
        if min_rows and max_rows:
            max_rows -= min_rows

        self.res = pd.read_csv(fname,
              sep=';',
              #dtype=np.float16,
              index_col=0,
              skiprows=min_rows,
              nrows=max_rows,
              engine='c')

        #self.res = self.res.dropna() 
        print("self.res")
        print(self.res)

        self.res = self.res.reset_index(drop = True)

        if self.limits:
            self.res = self.res.iloc[:, slice(self.limits[2] * self.c_agr, max_cols)]

        self.res.columns = range(self.res.columns.size)


        print("self.res")
        print(self.res)

        self.nrows, self.ncols = self.res.shape

        ifrows = self.nrows > self.MAX_ROWS
        ifcols = self.ncols > self.MAX_COLS

        self._agr_func(ifrows, ifcols) 

        if (self.method == 'mean'):
            self._mean(ifrows, ifcols)

        if not ifrows:
            self.r_agr = 1
            self.r_rem = 1

        if not ifcols:
            self.c_agr = 1
            self.c_rem = 1

    
    def get_params(self):
        return [self.r_agr, self.r_rem, self.c_agr, self.c_rem]

    def _agr_func(self, ifrows, ifcols):

        method_name = 'sum' if self.method == 'mean' else self.method
        if ifrows:
            self.r_agr = ceil(self.nrows / self.MAX_ROWS)
            self.r_rem = self.nrows % self.r_agr
            #self.res = self.res.groupby(self.res.index // self.r_agr).sum()
            self.res = getattr(self.res.groupby(self.res.index // self.r_agr), method_name)()

        if not ifcols:
            return

        self.c_agr = ceil(self.ncols / self.MAX_COLS)
        self.c_rem = self.ncols % self.c_agr
        cols = self.res.columns.astype(np.int16)
        #self.res = self.res.groupby(cols // self.c_agr, axis=1).sum()
        self.res = getattr(self.res.groupby(cols // self.c_agr, axis=1), method_name)()

        if not ifrows and not ifcols:
            self.tr_nrows, self.tr_ncols = self.nrows, self.ncols
            return

        self.tr_nrows, self.tr_ncols = self.res.shape


    def _mean(self, ifrows, ifcols):

        # Spaghetti code
        r, c = self.tr_nrows, self.tr_ncols 

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
            print("self.res.values[i]")
            print(self.res.values[i])
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


