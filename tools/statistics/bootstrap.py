__author__ = 'Ronaldo'

import pandas as pd
import numpy as np
import random

def bootstrap_resample(X, n=None):
    """ Bootstrap resample an array_like
    Parameters
    ----------
    X : array_like
      data to resample
    n : int, optional
      length of resampled array, equal to len(X) if n==None
    Results
    -------
    returns X_resamples
    """
    if isinstance(X, pd.Series):
        X = X.copy()
        X.index = range(len(X.index))
    if n == None:
        n = len(X)

    resample_i = np.floor(np.random.rand(n)*len(X)).astype(int)
    X_resample = np.array(X[resample_i])  # TODO: write a test demonstrating why array() is important
    return X_resample


def some(x, n):
    return x.ix[random.sample(x.index, n)]

def resample_pandas(df, n, replace=True):
    #np version 1.7 only
    #print np.version.version
    return df.loc[np.random.choice(df.index, n, replace=replace)]
