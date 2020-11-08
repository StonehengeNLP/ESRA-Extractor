from entity_linker import *
import pickle

pickle_path = '../../pickle/arxiv_cscl_200_cleaned.pickle'

with open(pickle_path, 'rb') as f:
    documents = pickle.load(f)

entities = []
ent_set = set()
vectors = []

for doc in data:
    doc_entities = doc['entities']
    for entity in doc_entities:
        ent = entity[:2]
        ent = tuple(ent)
        if ent not in ent_set:
            ent_set.add(ent)
            entities.append(ent)
            vector = generate_vector(ent)
            vectors.append(vector)

print(len(entities), len(vectors))

ent_vec = {'vectors':vectors, 'entities': entities}

with open('vector_200.pickle', 'wb') as f:
    pickle.dump(ent_vec,f)