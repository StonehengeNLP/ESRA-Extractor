"""
    Test file for various experiment run

    Tasks include:
        - Generate base KG embedding vector and save to pickle
                - Added pickle of 9 example document as a base KG
        - attemp to do entity linking
            - calculate embedding vector of document entities
            - find K candidate entities from KG
            - Set threshold for cosine similarity score in order to 
              validate 


"""

# imports
import pickle

from esra.transformers.entity_linking.generator import *

PICKLE_PATH = "pickle/vectors_9.pickle"

if __name__ == "__main__":
    # load pickle
    with open(PICKLE_PATH, "rb") as f:
        v = pickle.load(f)
        vectors = v['vectors']
        entities = v['entities']
    
    # create  and save tree 
    save_tree(vectors)
    