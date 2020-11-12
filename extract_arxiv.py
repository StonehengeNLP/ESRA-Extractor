import esra
import json
import glob
import pickle
import pandas as pd

from esra.extractors import ESRAE 
from esra.utils import nlp_split

for filename in glob.glob('./data/mag/*.json'):
    print(filename)
    
    with open(filename) as f:
        data = json.load(f)

    abstracts = [doc['ABS'] for doc in data]
    ids = [doc['Id'] for doc in data]
    r = ESRAE.extract(abstracts)
    
    # label their id
    for doc, id in zip(r, ids):
        doc['id'] = id

    with open(f'data/pickle/{filename[6:-4]}.pickle', 'wb') as f:
        pickle.dump(r, f)
