from typing import List, Dict
import numpy as np
import copy


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
        if entity[:2] == target[:2] and entity[0].lower() != "generic":
            indexes.append(i)
    return indexes

    
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