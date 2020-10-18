def abbreviation_split(data):
    """
        Split the entity that indluding abbreviation preserve
        its entity type and create the REFER-TO relation.
            ex. 'Convolution Neural Network ( CNN )' to 
                - 'Convolution Neural Network' -> issue_entity
                - 'CNN' -> abbrevate_entity

        params
            
            - data: {'entities':[entity_type, entity_name],
                     'relations':[relation_type, from_index, to_index]}

        output:
        
            - data: data object same as input format.
    """
    entities = data['entities']
    relations = data['relations']
    entities_length = len(entities)

    for (idx,entity) in enumerate(entities):
      if '(' in entity[1] and ')' in entity[1]:
        issue_entity = entity[1].strip()
        open_bracket_idx = issue_entity.find('(')
        abbrevate_entity = issue_entity[open_bracket_idx+1:-1].strip()
        issue_entity = issue_entity[:open_bracket_idx].strip()

        #replace the full one on original idx
        entities[idx] = [entity[0],issue_entity]

        #add abbreviation entity with same enttity type
        entities.append(['Abbreviation',abbrevate_entity])

        #add REFER-TO relation link abbreviation to full one
        relations.append(['REFER-TO',entities_length,idx])

        entities_length = len(entities)
        
    data['entities'] = entities
    data['relations'] = relations

    return data

# #for testing abbreviation_splitter module
# data = {'entities': [['OtherScientificTerm', 'black-box nature'],
#               ['Method', 'deep learning models'], 
#               ['Generic', 'methods'],
#               ['Generic', 'models'],
#               ['Method', 'model-agnostic and model-specific explanation methods'],
#               ['Method', 'Convolution Neural Network ( CNN )'],
#               ['Task', 'text classification'],
#               ['Task', 'human-grounded evaluations'],
#               ['OtherScientificTerm', 'model behavior'],
#               ['Method', 'model predictions'],
#               ['Method', 'explanation methods'],
#               ['Generic', 'methods']],
#        'relations':[['USED-FOR', 5, 2],
#               ['USED-FOR', 3, 5],
#               ['USED-FOR', 1, 7]]
#         }

# print(abbreviation_split(data))