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
        data = json.load(f)[0:1000]

    abstracts = [doc['ABS'] for doc in data]
    ids = [doc['Id'] for doc in data]
    r = ESRAE.extract(abstracts)
    
    # label their id
    for doc, id in zip(r, ids):
        doc['id'] = id

    with open('data/pickle/data_5000_1.pickle', 'wb') as f:
        pickle.dump(r, f)
    # slash = filename.rfind('/')
    # dot = filename.rfind('.')
    # with open(f'data/pickle/{filename[slash+1:dot]}.pickle', 'wb') as f:
    #     pickle.dump(r, f)
