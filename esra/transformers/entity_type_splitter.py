def entity_type_split(data):
    """
        Make entity type to be node and add new relations
        called 'IS-A'

        params:

            - data: data object
        
        return:

            - new_data: new data object that are more
             likes triple

    """
    entities = data['entities']
    relations = data['relations']

    new_entities = []
    entity_types = []
    unique_entity_types = []
    mapping = {}

    for idx,entity in enumerate(entities):
        entity_type,entity_name = entity
        new_entities.append(entity_name)
        entity_types.append([entity_type,idx])
        unique_entity_types.append(entity_type)

    unique_entity_types = list(dict.fromkeys(unique_entity_types))

    for entity_type in unique_entity_types:
        if entity_type not in new_entities:
            idx = len(new_entities)
            new_entities.append(entity_type)
            mapping[entity_type] = idx

    for entity_type,idx in entity_types:
        relations.append(['IS-A',idx,mapping[entity_type]])

    new_data = {'entities':new_entities,'relations':relations}

    return new_data