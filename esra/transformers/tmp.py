from entity_linker import *
import pickle

pickle_path = '../../pickle/arxiv_cscl_200_cleaned.pickle'

with open(pickle_path, 'rb') as f:
    documents = pickle.load(f)

entities = []
ent_set = set()
vectors = []

for doc in documents:
    doc_entities = doc['entities']
    for entity in doc_entities:
        ent = entity[:2]
        ent = tuple(ent)
        if ent not in ent_set:
            ent_set.add(ent)
            entities.append(ent)
            vector = generate_vector(ent[1])
            vectors.append(vector)

print(len(entities), len(vectors))

ent_vec = {'vectors':vectors, 'entities': entities}

with open('vector_200.pickle', 'wb') as f:
    pickle.dump(ent_vec,f)

# import numpy as np
# import os
# import pickle

# try:
#     from annoy import AnnoyIndex
# except:
#     raise ImportError("Unable to load annoy")


# # Constant var
# DIMENTIONS = 768
# NUM_TREE = 10
# NUM_NEIGHBOR = 5
# SIMILARITY_THRESHOLD = 0.9

# class Entity_Linker:
#     """
#         Class for link document entities to KG entities.
        
#         Run BERT on this module is never an option
#     """

#     def __init__(self, kg_pickle:str, document_pickle:str):
#         with open(kg_pickle, 'rb') as f:
#             vec_n_ent =  pickle.load(f)
#             self.kg_vectors = vec_n_ent['vectors']
#             self.kg_entities = vec_n_ent['entities']
#         with open(document_pickle, 'rb') as f:
#             vec_n_ent2 =  pickle.load(f)
#             self.doc_vectors = vec_n_ent2['vectors']
#             self.doc_entities = vec_n_ent2['entities']
    
#     def _save_tree(self, f_name='vec.ann'):
#         """
#             Save vector tree
#         """
#         t = AnnoyIndex(DIMENTIONS, 'angular') # init angular(cosine) index
        
#         for i,v in enumerate(self.kg_vectors):
#             t.add_item(i,v)
        
#         t.build(NUM_TREE)
#         t.save(f_name)
    
#     def _save_pickle(self, pickle_path):
#         with open(pickle_path, 'rb') as f:
#             save_dict = dict(
#                 vectors = self.vectors,
#                 entities = self.entities 
#             )
#             pickle.dump(f) 
    
#     def cosine_similarity(self, a, b):
#         na = np.linalg.norm(a)
#         nb = np.linalg.norm(b)
#         return (a @ b.T)/(na*nb)

#     def vector_similarity(self, f_name='vec.ann'):
#         """ 
#             generate index of KG entity that doc link to
#             if unlinkable then reptresent with -1
#         """
#         self._save_tree()
#         # load tree
#         if not os.path.exists(f_name):
#             raise FileNotFoundError("Missing tree file")
#         t = AnnoyIndex(DIMENTIONS, 'angular')
#         t.load(f_name)

#         # store index
#         kg_indexes = []

#         # for each document entity
#         for doc_vector in self.doc_vectors:
#             input_vector = doc_vector
#             k_indexes = t.get_nns_by_vector(
#                 input_vector,
#                 NUM_NEIGHBOR,
#                 search_k=-1,
#                 include_distances=False
#             )
#             # kg_indexes.append(k_indexes)
#             # check cosine similarity
#             max_cos_sim = self.cosine_similarity(
#                 input_vector,
#                 np.array(t.get_item_vector(k_indexes[0]))
#             )
#             if max_cos_sim < SIMILARITY_THRESHOLD: 
#                 kg_indexes.append([-1])
#             else:
#                 # select node with max cosine similarity
#                 kg_indexes.append(k_indexes)
#         print(kg_indexes)
#         return kg_indexes

#     def word_structure_matching(self, document_entities):
        
#         return None
    
#     def doc_entity_linking(self):
#         emb_idx = self.vector_similarity()
#         for i,e in enumerate(self.doc_entities):
#             print("###")
#             print(e)
#             print("Link to")
#             for idx in emb_idx[i]:
#                 if idx == -1:
#                     print("UNLINKABLE")
#                     break
#                 else:
#                     print(self.kg_entities[idx])


# # debug
# if __name__ == '__main__':
#     kg_path = '../../pickle/vector_200.pickle'
#     document_path = '../../pickle/new_doc.pickle'
#     # test init
#     linker = Entity_Linker(kg_path,document_path)
#     linker.doc_entity_linking()
