# Candidate entities generator

import torch
import numpy as np
import os
try:
    from transformers import *
except:
    raise ImportError("Unable to load transformers")

try:
    import annoy
except:
    raise ImportError("Unable to load annoy")

# init Scibert model
tokenizer = AutoTokenizer.from_pretrained(
    'allenai/scibert_scivocab_uncased'
    )
model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')

# Constant var
DIMENTIONS = 768
NUM_TREE = 10

def generate_vector(entity_name:str) -> np.ndarray:
    """
        Return entity name embedding numpy array
    """
    with torch.no_grad():
        out = model(entity_name)[0].mean(dim=1).view(-1)
    return out.detach().numpy()
    
def save_tree(vectors, f_name='vec.ann'):
    """
        Save vector tree
    """
    t = AnnoyIndex(DIMENTIONS, 'angular') # init angular(cosine) index
    
    for i,v in vectors:
        t.add_item(i,v)
    
    t.build(NUM_TREE)
    t.save(f_name)

def search_knn(input_vector, k=10, f_name="vec.ann"):
    """
        Return indexes of KNN sorted by similarity

        params:

            - input_vector(np.ndarray): input search vector

            - k(int): number of neighbor
    """

    # tree
    if not os.path.exists(f_name):
        raise FileNotFoundError("Missing tree file")

    t = AnnoyIndex(DIMENTIONS, 'angular')
    t.load(f_name)
    result_indexes = t.get_nns_by_vector(
        input_vector,
        k,
        search_k=-1,
        include_distances=False
        )
    return result_indexes