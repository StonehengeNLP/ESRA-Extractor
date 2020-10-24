def remove_generic(data):
    '''
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
  
    '''

    whitelist = [] #add whitelist here
    entities = data['entities']
    relations = data['relations']
    deleted_entities_idx = []
  
    # entities is list of entity
    # entity => [type,name,old_idx]
    for (i,entity) in enumerate(entities):
        entities[i] = [entity[0],entity[1],i]
    
    # find and collect idx of must delete entities
    for entity in entities:
        if entity[0] == 'Generic' and entity[1] not in whitelist:
            deleted_entities_idx.append(entity[2])

    # remove Generic from entites
    entities = [entity for entity in entities if entity[2] not in deleted_entities_idx]

    # create entities_mapping from old_idx to new_idx
    # entity => [type,name]
    entities_mapping = {}
    for (i,entity) in enumerate(entities):
        entities_mapping[entity[2]] = i
        entities[i] = [entity[0],entity[1]]

    # remove relations that associated with deleted entites
    relations = [relation for relation in relations if (relation[1] not in deleted_entities_idx \
        and relation[2] not in deleted_entities_idx)]

    # map the old_idx in relation to new_idx
    for (i,relation) in enumerate(relations):
        relations[i] = [relation[0],entities_mapping[relation[1]],entities_mapping[relation[2]]]

    return {'entities':entities,'relations':relations}
    

# # for testing this module
# data = {'entities': [['Task', 'language understanding'],
#   ['Method', 'convolutional architecture'],
#   ['Method', 'Dynamic Convolutional Neural Network'],
#   ['Task', 'semantic modelling'],
#   ['Method', 'Dynamic k-Max Pooling'],
#   ['Method', 'global pooling operation'],
#   ['OtherScientificTerm', 'feature graph'],
#   ['OtherScientificTerm', 'parse tree'],
#   ['Generic', 'experiment'],
#   ['Task', 'multi-class sentiment prediction'],
#   ['Task', 'six-way question classification'],
#   ['Task', 'Twitter sentiment prediction'],
#   ['OtherScientificTerm', 'distant supervision'],
#   ['Abbreviation', 'DCNN']],
#  'relations': [['HYPONYM-OF', 2, 1],
#   ['HYPONYM-OF', 2, 1],
#   ['USED-FOR', 4, 2],
#   ['USED-FOR', 7, 2],
#   ['EVALUATE-FOR', 8, 2],
#   ['HYPONYM-OF', 9, 8],
#   ['CONJUNCTION', 9, 10],
#   ['CONJUNCTION', 9, 11],
#   ['HYPONYM-OF', 10, 8],
#   ['CONJUNCTION', 10, 11],
#   ['HYPONYM-OF', 11, 8],
#   ['USED-FOR', 12, 11],
#   ['REFER-TO', 13, 2]]}

# print(remove_generic(data))