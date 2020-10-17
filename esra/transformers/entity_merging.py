from typing import List, Dict


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
        if entity[0].lower() != "generic":
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
    # relation [type, idx0, idx1]
    new_relations = []
    for relation in relations:
        if relation[1] in dups_cluster:
            relation[1] = dups_cluster[relation[1]]
        if relation[2] in dups_cluster:
            relation[2] = dups_cluster[relation[2]]
        if relation[1] in coref_dict:
            relation[1] = coref_dict[relation[1]]
        if relation[2] in coref_dict:
            relation[2] = coref_dict[relation[2]]

        new_relations.append(relation)
    return new_relations 

def __entity_handler(
    coref_dict:Dict,
    dups_cluster:List,
    entities:List
    ) -> List:
    """
        Filter out dup and coref entity
    """
    coref_keys = set(coref_dict.keys())
    dup_keys = set(dups_cluster.keys())
    combine = coref_keys | dup_keys
    return [entity for (i,entity) in enumerate(entities) if (
        i not in combine
        )]

def __find_all_dups(target:str,entities:List[str]) -> int:
    """
        Find all occurence of entity in entities list 
    """
    indexes = []
    for (i,entity) in enumerate(entities):
        if entity == target:
            indexes.append(i)
    return indexes

    
def merge_entity(output: Dict) -> Dict:
    """
        Function for cleaning output from model. Deleting and merging 
        entities
    """
    coref_clusters = output.get("coreferences", [])
    entities = output.get("entities", [])
    relations = output.get("relations", [])
    
    # find all dups
    passed = set()
    dups_cluster = dict()
    for x in entities:
        if tuple(x) not in passed:
            passed.add(tuple(x))
            occurences = __find_all_dups(x,entities)
            if len(occurences) > 1:
                for dup_idx in occurences:
                    dups_cluster[dup_idx] = occurences[0]
    
    # find all coref cluster
    coref_dict = dict()
    for cluster in coref_clusters:
        head, subs = __coref_handler(cluster,entities)
        for sub in subs:
            coref_dict[sub] = head
    
    new_relations = __relation_handler(
        coref_dict,
        dups_cluster,
        relations
        )
    new_entities = __entity_handler(
        coref_dict,
        dups_cluster,
        entities
    )
    return {
        "entities": new_entities,
        "relations": new_relations
    }