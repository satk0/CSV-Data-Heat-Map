import numpy as np
import pandas as pd
from tqdm import tqdm

M = 11
N = 10



rng = np.random.default_rng()

rnd_arr = 2000 * rng.random((M, N), dtype=np.float32).astype(np.float16) - 1000

DF = pd.DataFrame(rnd_arr)

'''
chunks = np.array_split(DF.index, 100)

fname = "11.csv"
for chunk, subset in enumerate(tqdm(chunks)):
    if chunk == 0:
        DF.loc[subset].to_csv(fname, mode='w', sep=';')
    else:
        DF.loc[subset].to_csv(fname, header=None, mode='a', sep=';')
'''
