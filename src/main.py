import seaborn as sbn
import pandas as pd
import matplotlib.pyplot as plt
import re
from math import ceil
from operator import add
from pprint import pprint

MAX_COLS = 30
MAX_ROWS = 30

#MAX_COLS = 2
#MAX_ROWS = 2

def average_data(fname: str, nrows: int, ncols: int):
    #https://stackoverflow.com/questions/9602856/most-efficient-way-to-split-strings-in-python
    # try regex
    averaged = []
    ravgs = []

    RCOUNT_LIMIT = ceil(nrows/MAX_ROWS)
    CCOUNT_LIMIT = ceil(ncols/MAX_COLS)
    print("RCOUNT_LIMIT:")
    print(RCOUNT_LIMIT)
    NEW_ROW_COUNT = ceil(MAX_ROWS // RCOUNT_LIMIT)
    NEW_COL_COUNT = ceil(MAX_COLS // CCOUNT_LIMIT)

     # CALCULATE FOR NOT SCALED LIST !!!!!!!!!!!!!!
    SCALE = NEW_COL_COUNT*NEW_ROW_COUNT
    COMMON = RCOUNT_LIMIT * CCOUNT_LIMIT
    
    CREMAINER = ncols % CCOUNT_LIMIT
    if not CREMAINER:
        CREMAINER = CCOUNT_LIMIT
    RREMAINER = nrows % RCOUNT_LIMIT
    if not RREMAINER:
        RREMAINER = RCOUNT_LIMIT

    REM_COL_DIVIDER = CREMAINER * RCOUNT_LIMIT
    REM_ROW_DIVIDER = RREMAINER * CCOUNT_LIMIT
    REM_CR_DIVIDER = CREMAINER * RREMAINER
    
    
    
    
    with open(fname) as file:
        # skip the first line (if there is anything defined there)
        file.readline()

        for iline, line in enumerate(file):
             
            start = 0

            #nums.append([])
            
            rnums = []
            rcount = 0
            #ccount = 0

            sum_value = 0

            for index, char in enumerate(line):
                if (char in [';', '\n']):
                    try:
                        if (rcount == CCOUNT_LIMIT):
                            #nums[iline].append(sum_value)
                            rnums.append(sum_value)

                            sum_value = 0 
                            rcount = 0

                        #nums[iline].append(float(line[start:index]))
                        sum_value += float(line[start:index])
                        start = index + 1
                        rcount += 1
                        

                    except Exception as e:
                        if not start:
                            start = index + 1
                            continue
                        exit("Error: Błąd pliku, szczegóły błędu: {}".format(e))
            if rcount:
                sum_value = sum_value
                #nums[iline].append(sum_value)
                rnums.append(sum_value)
            
            # add two lists:
            tmp_index = iline//RCOUNT_LIMIT

            if len(averaged) == tmp_index:
                averaged.append(rnums)
                continue
               # temp solution, need to check: https://stackoverflow.com/questions/8244915/how-do-you-divide-each-element-in-a-list-by-an-int 

            # sumed by rows:
            averaged[tmp_index] = list(map(add, averaged[tmp_index], rnums))

            
            
    # main
    for i in range(len(averaged) - 1):
        for j in range(len(averaged[i]) - 1):
            averaged[i][j] /= COMMON

    #left_down
    for j in range(len(averaged[-1]) - 1):
        averaged[-1][j] /= REM_ROW_DIVIDER
    #right_up 
    for i in range(len(averaged) - 1):
        averaged[i][-1] /= REM_COL_DIVIDER
    # right_down
    print("averaged[-1][-1]", averaged[-1][-1])
    averaged[-1][-1] /= REM_CR_DIVIDER

    return averaged




def preprocess(fname: str):
    ncols = 0
    nrows = 0

    # https://stackoverflow.com/questions/9629179/python-counting-lines-in-a-huge-10gb-file-as-fast-as-possible
    with open(fname, "rb") as file:
        ncols = file.readline().count(bytes(";",'utf-8')) 
        nrows = sum(1 for _ in file)

    print("cols count: {}".format(ncols))
    print("rows count: {}".format(nrows))
    
    
    if ((nrows <= MAX_ROWS) or (ncols <= MAX_COLS)):
        return None

    return average_data(fname, nrows, ncols)

#fname = "data/ex.csv"
class HeatMapHandler:

    def __init__(self):
        self.fname = None
        
    def drawHeatMap(self, fname):
        self.fname = fname 
        #fname = "500_0_30.csv"
        res = preprocess(self.fname)
        if res is None:
            dataset = pd.read_csv(self.fname, sep=';', index_col=0)
        else:
            series_list = []
            for e in res:
                series_list.append(pd.Series(e))
            dataset = pd.DataFrame(series_list)

#dataset = sbn.load_dataset("glue").pivot("Model", "Task", "Score")
        print(dataset)
        sbn.heatmap(dataset)

        plt.show()

heatmap = HeatMapHandler()
heatmap.drawHeatMap("1000df.csv")
