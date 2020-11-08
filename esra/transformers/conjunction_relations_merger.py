def __split_conj_relation(relations):
    """
        split all relation into to list 
            - list of conjction pair
            - list or other relation
        
        parmas:

            - relations: list of all relation
        
        return:

            - list_conj: list of all conjuction pair collect
            in form of [[1,2],[2,3],[1,3]]

            - other_relations: list of other relations collect
            in form of list of [relation_type,from_idx,to_idx]

    """

    list_conj = []
    other_relations = []

    for relation in relations:
        if relation[0].upper() == 'CONJUNCTION':
            list_conj.append([relation[1],relation[2]])
        else:
            other_relations.append(relation)
            
    return list_conj, other_relations



def __merge(list_conj):
    """
        merge conjunction pair into conjuction group

        params:

            - list_conj: list of all conjuction collect
            in form of [[1,2],[2,3],[1,3]]
        
        return:

            - list_conj_group: list of conjunction group
          
    """

    list_conj = [set(conj) for conj in list_conj]
    merged = False
    while not merged: 
        merged = True
        results = []
        while list_conj: #
            common,rest = list_conj[0], list_conj[1:]
            list_conj = []
            for x in rest:
                if x.isdisjoint(common):
                    list_conj.append(x)
                else:
                    merged = False
                    common |= x
            results.append(common)
        list_conj = results

    list_conj_group = list_conj
    return list_conj_group




def __get_entity_mapping(list_conj_group,entities):
    """
        Get mapping of entity to itself group

        params:
            
            - list_conj_group: list of conjunction group

            - entities: entities from data
        
        return:

            - entities_mapping: dict of mapping entity to
            itself group.

    """

    entities_mapping = {}
    for i in range(len(entities)):
        entities_mapping[i] = [i]
    
    for group in list_conj_group:
        for idx in group:
            entities_mapping[idx] = list(group)
    
    return entities_mapping



def __get_new_relations(entity_mapping, other_relations):
    """
        Retrieve new relations that related on conjunction group

        params:

            - entity_mapping: map of entity to conjunction group

            - other_relations: relations that delete all conjunction
            relations
        
        return:

            - new_relations: new relations that generate from
            relation that asscociated to conjunction group.

    """

    new_relations = []

    for relation in other_relations:
        r0, r1, r2, r3 = relation
        
        if len(entity_mapping[r1]) > 1 and len(entity_mapping[r2]) == 1:
            new_relations += [[r0, idx, r2, r3] for idx in entity_mapping[r1] if idx != r1]
        elif len(entity_mapping[r1]) == 1 and len(entity_mapping[r2]) > 1:
            new_relations += [[r0, r1, idx, r3] for idx in entity_mapping[r2] if idx != r2]
        elif len(entity_mapping[r1]) > 1 and len(entity_mapping[r2]) > 1:
            for idx_1 in entity_mapping[r1]:
                for idx_2 in entity_mapping[r2]:
                    if idx_1 != r1 or idx_2 != r2:
                        new_relations.append([r0, idx_1, idx_2, r3])

    return new_relations

def merge_conjuction_relation(data):
    """
        Retrive the outcome data of conjuction relations
        merger. This is the main function.

        params:

            - data: data object 

        return: 
            
            - data object that clear all conjunction relations and
            handle all associated relations already.

    """

    entities = data['entities']
    relations = data['relations']
    list_conj, other_relations  = __split_conj_relation(relations)
    list_conj_group = __merge(list_conj)
    entities_mapping = __get_entity_mapping(list_conj_group,entities)
    new_relations = __get_new_relations(entities_mapping,other_relations)
    relations =  other_relations + new_relations

    # find mean of duplicated relations
    d = {}
    for *x, r3 in relations:
        x = tuple(x)
        if x not in d:
            d[x] = []
        d[x] += [r3]
        
    # remove duplicates
    relations = [list(x) + [sum(d[x])/len(d[x])] for x in d]

    return {'entities': entities,'relations': relations}