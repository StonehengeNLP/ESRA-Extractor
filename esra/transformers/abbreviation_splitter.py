import re
import copy 
import numpy as np
import Levenshtein

def _find_abbrv(list_of_candidate):
    """return the index of abbreviation from the given candidates"""
    # for trivial case
    for i, c in enumerate(list_of_candidate):
        if c == c.upper():
            return i
    # for complicated case
    distances = [Levenshtein.distance(c, c.upper()) for c in list_of_candidate]
    return np.argmin(distances)

def abbreviation_split(data):
    data = copy.deepcopy(data)
    entities = data['entities']
    relations = data['relations']
    
    for i, entity in enumerate(entities):
        candidate_name = re.split(r'[(|)]', entity[1])
        candidate_name = [n.strip() for n in candidate_name if len(n) > 1]

        # when the abbriviation was found
        if len(candidate_name) > 1:
            j = _find_abbrv(candidate_name[:2])
            abbrv = candidate_name.pop(j)
            entity[1] = ' '.join(candidate_name)
            len_entities = len(entities)
            entities.append(['Abbreviation', abbrv, 1.0])
            
            # in the case of parentheses are on the edge
            if len(candidate_name) == 1:
                relations.append(['Refer-to', len_entities, i, 1.0])
            
            # in the case of parentheses are in the middle
            else:
                entities.append([entity[0], candidate_name[0], entity[2]])
                relations.append(['Refer-to', len_entities, len_entities+1, 1.0])
    return data

'''
def abbreviation_split(data):
    """
        Split the entity that indluding abbreviation preserve
        its entity type and create the Refer-to relation.
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
        stripped_entity = entity[1].strip()
        open_bracket_idx = stripped_entity.find('(')
        close_bracket_idx = stripped_entity.find(')')
        abbrevate_entity = stripped_entity[open_bracket_idx+1:close_bracket_idx].strip()
        issue_entity = stripped_entity[:open_bracket_idx].strip()
        if close_bracket_idx < len(stripped_entity)-1:
            issue_entity += stripped_entity[close_bracket_idx+1:]

        #replace the full one on original idx
        entities[idx] = [entity[0],issue_entity]

        #add abbreviation entity with same enttity type
        entities.append(['Abbreviation',abbrevate_entity])

        #add Refer-to relation link abbreviation to full one
        relations.append(['Refer-to',entities_length,idx])

        entities_length = len(entities)
        
    data['entities'] = entities
    data['relations'] = relations

    return data
# '''