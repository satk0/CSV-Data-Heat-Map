import seaborn as sbn
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("test.csv", sep=';', index_col=0)
#dataset = sbn.load_dataset("glue").pivot("Model", "Task", "Score")
print(dataset)

#od bialego do niebieskiego
#sbn.heatmap(dataset, cmap="Blues")

#od bialego do czerwonego
#sbn.heatmap(dataset, cmap="Reds")

#od niebieskiego do czerwonego
sbn.heatmap(dataset, cmap="RdBu_r")

plt.show()


