import pandas as pd
import numpy as np

fname = "10.csv"
arr = pd.read_csv(fname,
                  sep=';',
                  dtype=np.float16,
                  index_col=0,
                  engine='c' 
                  )


#use .apply
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
for row in arr.itertuples():
    print(row)
