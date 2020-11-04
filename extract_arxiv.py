import esra
import json
import glob
import pandas as pd

from esra.extractors import ESRAE 


for filename in glob.glob('arxiv/*.csv'):
    df = pd.read_csv(filename)
    abstracts = df.abstract.to_list()
    
    r = ESRAE.extract(abstracts)

    with open(f'{filename[:-4]}.pickle', 'wb') as f:
        pickle.dump(r, f)