# Candidate entities generator

import torch
import numpy as np
import os
try:
    from transformers import *
except:
    raise ImportError("Unable to load transformers")

try:
    from annoy import AnnoyIndex
except:
    raise ImportError("Unable to load annoy")


# SciBERT pretrained model folder is in transformers/

# init Scibert model
tokenizer = AutoTokenizer.from_pretrained(
    'scibert_scivocab_uncased/'
    )
model = AutoModel.from_pretrained(
    'scibert_scivocab_uncased/',
    output_hidden_states=True
    )
model.eval()

# Constant var
DIMENTIONS = 768
NUM_TREE = 10
NUM_NEIGHBOR = 3
SIMILARITY_THRESHOLD = 0.9

def generate_vector(entity_name:str) -> np.ndarray:
    """
        Return entity name embedding numpy array
    """
    tokens = tokenizer.encode(entity_name, return_tensors='pt')
    with torch.no_grad():
        model_output = model(tokens)
    hidden_states = model_output[2]
    # create sentence embedding frim hidden states 
    out = hidden_states[-2][0].mean(dim=0)
    return out.detach().numpy()
    
def save_tree(vectors, f_name='vec.ann'):
    """
        Save vector tree
    """
    t = AnnoyIndex(DIMENTIONS, 'angular') # init angular(cosine) index
    
    for i,v in enumerate(vectors):
        t.add_item(i,v)
    
    t.build(NUM_TREE)
    t.save(f_name)

def cosine_similarity(a,b):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    return (a @ b.T)/(na*nb)     

def doc_kg_linking(document_entities, f_name='vec.ann'):
    """
        generate index of KG entity that doc link to
        if unlinkingable then reptresent with -1
    """
    # load tree
    if not os.path.exists(f_name):
        raise FileNotFoundError("Missing tree file")
    t = AnnoyIndex(DIMENTIONS, 'angular')
    t.load(f_name)

    # store index
    kg_indexes = []

    # for each document entity
    for entity in document_entities:
        input_vector = generate_vector(entity[1])
        k_indexes = t.get_nns_by_vector(
            input_vector,
            NUM_NEIGHBOR,
            search_k=-1,
            include_distances=False
        )
        # check cosine similarity
        max_cos_sim = cosine_similarity(
            input_vector,
            np.array(t.get_item_vector(k_indexes[0]))
        )
        if max_cos_sim < SIMILARITY_THRESHOLD: 
            kg_indexes.append(-1)
        else:
            # select node with max cosine similarity
            kg_indexes.append(k_indexes[0])

    return kg_indexes