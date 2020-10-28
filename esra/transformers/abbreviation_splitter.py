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