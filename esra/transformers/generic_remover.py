import copy

def remove_generic(data):
    """
        This module will clear the generic type entities
        that not included in whitelist

        params:

            - data: data object that already passed 
            the coreference, singularization, 
            conjunction split, and abbreviation 
            split module.

        return:

            - data: data object that remove generic type
            entities which is not in whitelist.
  
    """

    whitelist = [] # TODO: add whitelist here
    entities = copy.deepcopy(data['entities'])
    relations = copy.deepcopy(data['relations'])
    
    generics = []
    for i, entity in enumerate(entities):
        if entity[0] == 'Generic':
            generics += [i]
            
    # create mapping
    mapping = []
    j = 0
    for i in range(len(entities)):
        if j < len(generics) and generics[j] == i:
            mapping += [-1]
            j += 1
        else:
            mapping += [i - j]
        
    # remove generic entities
    entities = [entity for i, entity in enumerate(entities) if i not in generics]
    
    # refine relations
    for relation in relations:
        relation[1] = mapping[relation[1]]
        relation[2] = mapping[relation[2]]
        
    # remove generic related relations
    relations = [relation for relation in relations if relation[1] != -1 and relation[2] != -1]
    
    '''
    # deleted_entities_idx = []
  
    # # entities is list of entity
    # # entity => [type, name, confidence, old_idx]
    # for (i,entity) in enumerate(entities):
    #     entities[i] = [entity[0],entity[1],i]
    
    # # find and collect idx of must delete entities
    # for entity in entities:
    #     if entity[0] == 'Generic' and entity[1] not in whitelist:
    #         deleted_entities_idx.append(entity[2])

    # # remove Generic from entites
    # entities = [entity for entity in entities if entity[2] not in deleted_entities_idx]

    # # create entities_mapping from old_idx to new_idx
    # # entity => [type,name]
    # entities_mapping = {}
    # for (i,entity) in enumerate(entities):
    #     entities_mapping[entity[2]] = i
    #     entities[i] = [entity[0],entity[1]]

    # # remove relations that associated with deleted entites
    # relations = [relation for relation in relations if (relation[1] not in deleted_entities_idx \
    #     and relation[2] not in deleted_entities_idx)]

    # # map the old_idx in relation to new_idx
    # for (i,relation) in enumerate(relations):
    #     relations[i] = [relation[0],entities_mapping[relation[1]],entities_mapping[relation[2]]]
    '''
    return {'entities': entities, 'relations': relations}
    