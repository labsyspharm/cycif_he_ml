import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/aligned_feature.csv')
plt.scatter(df['DNA6'], df['CD20'])
plt.show()
