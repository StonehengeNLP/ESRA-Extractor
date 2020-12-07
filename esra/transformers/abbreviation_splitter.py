import re
import copy 
import numpy as np
import Levenshtein

def _find_abbrv(list_of_candidate):
    """return the index of abbreviation from the given candidates"""

    # check length of both texts to classify main_text and abbreviation
    if len(list_of_candidate[0]) > len(list_of_candidate[1]):
        return 1
    else:
        return 0

def _lcs(x,y):
    m = len(x) 
    n = len(y)
    
    L = [[None]*(n + 1) for i in range(m + 1)] 

    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif x[i-1] == y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1])    
    return L[m][n] 

def _is_abbreviation(list_of_candidate):
    j = _find_abbrv(list_of_candidate)
    abbrv = list_of_candidate[j]
    main_text = list_of_candidate[abs(j-1)]
    return True if _lcs(main_text,abbrv)/len(abbrv) > 0.66 else False


def abbreviation_split(data):
    data = copy.deepcopy(data)
    entities = data['entities']
    relations = data['relations']
    
    for i, entity in enumerate(entities):
        candidate_name = re.split(r'[(|)]', entity[1])
        candidate_name = [n.strip() for n in candidate_name if len(n) > 1]

        # when the abbriviation was found
        if len(candidate_name) > 1:
            if _is_abbreviation(candidate_name[:2]): #abbreviation case
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

            else: #related content case
                related_content = candidate_name.pop(1)
                entity[1] = ' '.join(candidate_name)

                len_entities = len(entities)
                entities.append(['OtherScientificTerm', related_content, entity[2]])
                
                # in the case of parentheses are on the edge
                if len(candidate_name) == 1:
                    relations.append(['Related-to', len_entities, i, 0.25])
                
                # in the case of parentheses are in the middle
                else:
                    entities.append([entity[0], candidate_name[0], entity[2]])
                    relations.append(['Related-to', len_entities, len_entities+1, 0.25])
                
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