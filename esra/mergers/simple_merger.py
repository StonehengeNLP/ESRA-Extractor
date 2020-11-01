import pickle
import os, sys
import numpy as np

sys.path.append("../transformers/")

from entity_linker import *


def add_paperid(list_obj):
    """
        (Temporary function) add paper_id to object

        params:

            - list_obj: list of object

        return:

            -  list_obj: list of obj that already add paper_id

    """
    with open('paper_id.txt','r') as f:
        current_paper_id = int(f.read().strip())
    for obj in list_obj:
        current_paper_id += 1
        obj['paper_id'] = current_paper_id
    with open('paper_id.txt','w') as f:
        f.write(str(current_paper_id))
    print('Finish assign paper_id to object.')
    return list_obj



def obj2triples(obj):
    """
        Convert a object data to triples list.

        params:

            - obj: object data same as data object in module 6.

        return:

            - tuple(paper_id,triples): 

                - paper_id: paper_id to be key of triples.

                - triples: list of triples from this object.
                triple in list format: [(et,en),rt,(et,en)] 

    """
    paper_id = obj['paper_id']
    entities = obj['entities']
    relations = obj['relations']
    triples = []

    for relation_type,from_idx,to_idx in relations:
        new_triple = []
        new_triple.append((entities[from_idx][0],entities[from_idx][1]))
        new_triple.append(relation_type)
        new_triple.append((entities[to_idx][0],entities[to_idx][1]))
        triples.append(new_triple)
    return (paper_id,triples)



def objects_to_triples(list_obj):
    """
        Covert mutiple object to list(triples list).

        params:

            - list_obj: mutiple object.

        return:

            - list_triples: list of triples_list of each obj.

    """
    list_triples = []
    for obj in list_obj:
        list_triples.append(obj2triples(obj))
    return list_triples


def existing_in_kg(triple,existing_kg):
    """
        Checking that the triple is in exsiting KG or not.

        params:

            - triple: specific triple that want to check.

            - existing_kg: Existing KG.
            A triple in existing_kg :
            [[(et,en),rt,(et,en)],set([paper_id1,paper_id2])] 

        return:

            - (Boolean,idx):

                - Boolean: True -> Exist, False -> not exist.

                - idx: return index of matched triple. If not,
                return -1.

    """
    if len(existing_kg) == 0:
        return (False,-1)
    else:
        existing_kg = np.array(existing_kg)
        for idx,existing_triple in enumerate(existing_kg[:,0]):
            if triple == existing_triple:
                return (True,idx)
        return (False,-1)



def merging_to_kg(list_triples,existing_kg):
    """
        Merge papaers to existing KG.

        params:

            - list_triples: list of triples lidt of all papers.

            - existing_kg: Existing KG.
            A triple in existing_kg :
            [[(et,en),rt,(et,en)],set([paper_id1,paper_id2])]

        return: 

            - existing_kg: Existing KG which already merged.
    """
    for paper_id,triples in list_triples:
        for triple in triples:
            check_existing,idx = existing_in_kg(triple,existing_kg)
        if check_existing == True:
            existing_kg[idx][1].add(paper_id)
        else:
            existing_kg.append([triple,set([paper_id])])
    return existing_kg

#if you want to restart the flow please uncomment and run this code below:
with open('paper_id.txt','w') as f:
        f.write('-1')

# read extracted data that pass through the whole of module 6
with open('../../pickle/triple_CNN_10_cleaned.pickle','rb') as f:
    list_data = pickle.load(f)

# prepare data
list_data = add_paperid(list_data) # add id to paper only for this example

# create exising KG
existed_list_data = list_data[0:-1] # paper_id 0-8 assign to be exising KG
existed_list_triples = objects_to_triples(existed_list_data) # change data object to triple
existing_kg = []
existing_kg = merging_to_kg(existed_list_triples,existing_kg) # create existing KG

# simulate the case that we add new paper
new_data = list_data[-1:] # paper_id 9 assign to be new paper that going to merge to KG

## Entity linking  ##

# load vectors and entities of existing KG
with open("../../pickle/vector_9.pickle", "rb") as f:
    tmp = pickle.load(f)
    vectors = tmp["vectors"]
    entities = tmp["entities"]

# check if tree exist
if not os.path.exists("vec.ann"):
    save_tree(vectors)

# link document entities to KG entities
link_indexes = doc_kg_linking(new_data["entities"])

# Test print link
print("## Entity linking ##")

for i,kg_idx in enumerate(link_indexes):
    if kg_idx != -1:
        print(
            f"%s link to %s" % (new_data["entities"][i][1], entities[kg_idx])
        )
    else:
        print("Unlink")

print("## End ##")

## 


new_list_triples = objects_to_triples(new_data) 
existing_kg = merging_to_kg(new_list_triples,existing_kg) # merge new paper to existing KG

print(existing_kg)
