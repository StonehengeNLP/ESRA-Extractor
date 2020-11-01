def map_paper_to_data(data):
    """
        Create new entities('Paper') and relations from extracted
        entities to paper('APPEAR-IN').

        params:

            - data: object that included 'entities', 'relations' and 
            'paper_id'

        return:

            - data: data obj that already added 'Paper' entity and
             'APPEAR-IN' relations .

    """
    entities = data['entities']
    relations = data['relations']
    paper_id = data['paper_id']
    
    #add paper entity
    entities.append(['Paper',str(paper_id)])
    paper_entity_idx = len(entities)-1

    #add new relation
    for (i,entity) in entities:
        if i != paper_entity_idx:
            relations.append(['APPEAR-IN',i,paper_entity_idx])
    
    return {'entities':entities,'relations':relations,'paper_id':paper_id}

# data = {'entities': [['OtherScientificTerm', 'black-box nature'],
#                             ['Method', 'deep learning models'], 
#                             ['Generic', 'methods'],
#                             ['Generic', 'models'],
#                             ['Method', 'model-agnostic and model-specific explanation methods'],
#                             ['Method', 'CNNs'],
#                             ['Task', 'text classification'],
#                             ['Task', 'human-grounded evaluations'],
#                             ['OtherScientificTerm', 'model behavior'],
#                             ['Method', 'model predictions'],
#                             ['Method', 'explanation methods'],
#                             ['Generic', 'methods']],
#             'relations':[['USED-FOR', 1, 2],
#                             ['USED-FOR', 2, 3],
#                             ['USED-FOR', 6, 7]],
#             'paper_id': '101'
#         }

# print(link_paper_entities(data))

