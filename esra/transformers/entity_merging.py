from typing import List, Dict
import numpy as np
import copy
from fuzzywuzzy import fuzz


def __coref_handler(
    cluster:List[int], 
    entities:List[str]
    ) -> (int, List[int]):
    """
        Handler funciton for coreference singularization. Return list of
        entity index to drop and index of cluster representator(head).
        
    """
    max_length = -1
    head = -1
    subs = []
    for idx in cluster:
        entity = entities[idx]
        # check entity's type, ignore `generic` type
        # if entity[0].lower() != "generic":
        length = len(entity[1])
        if length > max_length:
            max_length = length
            head = idx
    subs = cluster.copy()
    subs.remove(head)
    return (head, subs) 

def __relation_handler(
    coref_dict:Dict,
    dups_cluster:List,
    relations:List
    ) -> List:
    """
        Handler function for cleaning entity in coreference cluster
    """
    def indexer(idx:int, combine):
        """
            Find new index in new entities list
        """
        subtractor = len(combine[combine < idx])
        return idx - subtractor

    # relation [type, idx0, idx1]
    combine = np.array(list(set(
        list(dups_cluster.keys()) + list(coref_dict.keys())
        )))
    new_relations = []
    for relation in relations:
        idx1,idx2 = relation[1], relation[2]
        if relation[1] in dups_cluster:
            idx1 = dups_cluster[relation[1]]            
        if relation[2] in dups_cluster:
            idx2 = dups_cluster[relation[2]]            
        if relation[1] in coref_dict:
            idx1 = coref_dict[relation[1]]            
        if relation[2] in coref_dict:
            idx2 = coref_dict[relation[2]]            

        relation[1] = indexer(
            idx1,
            combine
        )
        relation[2] = indexer(
            idx2,
            combine
        )

        new_relations.append(relation)
    return new_relations  

def __entity_handler(
    # TODO: average the entities confidence score
    coref_dict:Dict,
    dups_cluster:List,
    entities:List
    ) -> List:
    coref_keys = set(coref_dict.keys())
    dup_keys = set(dups_cluster.keys())
    combine = coref_keys | dup_keys
    return [entity for (i,entity) in enumerate(entities) if (
        i not in combine
        )]

def __find_all_dups(target:str, entities:List[str]) -> int:
    """
        Find all occurence of entity in entities list 
    """
    indexes = []
    for (i,entity) in enumerate(entities):
        if entity[:2] == target[:2]: # and entity[0].lower() != "generic"
            indexes.append(i)
    return indexes

def __get_new_score(entities,occurences):
    max_score = -1
    for dup_idx in occurences:
        if entities[dup_idx][2] > max_score:
            max_score = entities[dup_idx][2]
    return max_score

def __get_substring_score(str1,str2):
    if len(str1) >= len(str2):
        long_str = str1.lower()
        short_str = str2.lower()
    else:
        long_str = str2.lower()
        short_str = str1.lower()

    if short_str in long_str:
        score = 1.0
    else:
        score = fuzz.partial_ratio(str1,str2)/100

    return score

def __get_all_pair_score(entities,coref_cluster):
    all_pairs = []
    for i in range(len(coref_cluster)):
        for j in range(i,len(coref_cluster)):
            idx1 = coref_cluster[i]
            idx2 = coref_cluster[j]
            if idx1 != idx2:
                score = __get_substring_score(entities[idx1][1],entities[idx2][1])
                all_pairs.append([idx1,idx2,score])
                # all_pairs.append([entities[idx1][1],entities[idx2][1],score]) #for test
    return all_pairs

def __merge_cluster_dict(dict):
    list_cluster = [item[1] for item in dict.items()]
    merged = False
    while not merged: 
        merged = True
        results = []
        while list_cluster: #
            common,rest = list_cluster[0], list_cluster[1:]
            list_cluster = []
            for x in rest:
                if x.isdisjoint(common):
                    list_cluster.append(x)
                else:
                    merged = False
                    common |= x
            results.append(common)
        list_cluster = results

    return list_cluster


def __handle_coref_cluster(entities,coref_cluster,threshold=0.6):
    pronoun_list = ['they','those','it','them','these','he','she','i','we','you','our','there','us','him','her','me']
    for idx in coref_cluster:
        if entities[idx][1] in pronoun_list:
            return [coref_cluster]
    all_pairs = __get_all_pair_score(entities,coref_cluster)
    clusters = {}
    for idx1,idx2,score in all_pairs:
        if score > threshold:
            if idx1 in clusters.keys():
                clusters[idx1].add(idx2)
            else:
                clusters[idx1] = set([idx1,idx2])
            if idx2 in clusters.keys():
                clusters[idx2].add(idx1)
            else:
                clusters[idx2] = set([idx2,idx1])
        else:
            if idx1 not in clusters.keys():
                clusters[idx1] = set([idx1])
            if idx2 not in clusters.keys():
                clusters[idx2] = set([idx2])
    clusters_list = __merge_cluster_dict(clusters)
    clusters_list = [list(cluster) for cluster in clusters_list if len(cluster) > 1]
    return clusters_list
  

def coreference_handler(model_output: Dict) -> Dict:
    output = copy.deepcopy(model_output)
    coref_clusters = output.get("coreferences", [])
    entities = output.get("entities", [])
    relations = output.get("relations", [])
    
    # find all dups
    # passed = set()
    dups_cluster = dict()
    # for x in entities:
    #     if tuple(x) not in passed:
    #         passed.add(tuple(x))
    #         occurences = __find_all_dups(x,entities)
    #         if len(occurences) > 1:
    #             for dup_idx in occurences[1:]:
    #                 dups_cluster[dup_idx] = occurences[0]
    
    # find all coref cluster
    coref_dict = dict()
    new_coref_clusters = []
    for coref_cluster in coref_clusters:
        new_coref_cluster_list = __handle_coref_cluster(entities,coref_cluster)
        for new_coref_cluster in new_coref_cluster_list:
            new_coref_clusters.append(new_coref_cluster)

    # # start of validate test
    # val_coref = []
    # val_new_coref = []

    # for coref_cluster in coref_clusters:
    #     temp = []
    #     for idx in coref_cluster:
    #         temp.append(entities[idx][1])
    #     val_coref.append(temp)
    
    # for new_coref_cluster in new_coref_clusters:
    #     temp = []
    #     for idx in coref_cluster:
    #         temp.append(entities[idx][1])
    #     val_new_coref.append(temp)
    # print(val_coref,val_new_coref)
    # # end of validate test

    coref_clusters = new_coref_clusters
    for cluster in coref_clusters:
        head, subs = __coref_handler(cluster,entities)
        for sub in subs:
            coref_dict[sub] = head

    new_entities = __entity_handler(
        coref_dict,
        dups_cluster,
        entities
    )

    new_relations = __relation_handler(
        coref_dict,
        dups_cluster,
        relations
        )
    
    return {
        "entities": new_entities,
        "relations": new_relations
    }

def duplicate_entity_handler(model_output: Dict) -> Dict:
    output = copy.deepcopy(model_output)
    # coref_clusters = output.get("coreferences", [])
    entities = output.get("entities", [])
    relations = output.get("relations", [])
    
    # find all dups
    passed = set()
    dups_cluster = dict()
    for x in entities:
        type, name, *args = x
        if (type, name) not in passed:
            passed.add((type, name))
            occurences = __find_all_dups(x, entities)
            if len(occurences) > 1:
                entities[occurences[0]] = [entities[occurences[0]][0],entities[occurences[0]][1],__get_new_score(entities,occurences)]
                for dup_idx in occurences[1:]:
                    dups_cluster[dup_idx] = occurences[0]
    
    # find all coref cluster
    coref_dict = dict()
    # for cluster in coref_clusters:
    #     head, subs = __coref_handler(cluster,entities)
    #     for sub in subs:
    #         coref_dict[sub] = head

    new_entities = __entity_handler(
        coref_dict,
        dups_cluster,
        entities
    )

    new_relations = __relation_handler(
        coref_dict,
        dups_cluster,
        relations
        )
    return {
        "entities": new_entities,
        "relations": new_relations
    }
