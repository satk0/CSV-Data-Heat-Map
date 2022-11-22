import seaborn as sbn
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("test.csv", sep=';', index_col=0)
#dataset = sbn.load_dataset("glue").pivot("Model", "Task", "Score")
print(dataset)
sbn.heatmap(dataset)

plt.show()


