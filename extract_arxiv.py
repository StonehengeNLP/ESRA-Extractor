import esra
import json
import glob
import pickle
import pandas as pd

from esra.extractors import ESRAE 
from esra.utils import nlp_split

for filename in glob.glob('arxiv/*.csv')[-1:]:
    print(filename)
    
    df = pd.read_csv(filename)
    abstracts = df.abstract.to_list()
    r = ESRAE.extract(abstracts)

    with open(f'pickle/{filename[6:-4]}.pickle', 'wb') as f:
        pickle.dump(r, f)