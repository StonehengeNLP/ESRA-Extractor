import os
import pandas as pd

DATA_PATH = './data/'
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)


def insert(df: pd.DataFrame):
    filename = DATA_PATH + 'aa.csv'
    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename)