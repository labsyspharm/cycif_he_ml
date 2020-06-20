import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

if __name__ == '__main__':
    df = pd.read_csv('../data/aligned_feature.csv')
    X = df.sample(n=int(1e4))\
            [['DNA6', 'CD20']].values
    d = stats.gaussian_kde(X.T)(X.T)
    sk = np.argsort(d)
    X, d = X[sk, :], d[sk]

    plt.scatter(X[:, 0], X[:, 1], c=d, cmap='coolwarm', s=1)
    plt.xlabel('DNA6')
    plt.ylabel('CD20')
    plt.show()
