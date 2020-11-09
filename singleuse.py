import sys
import pandas as pd
import pickle

from esra.transformers.entity_linker import * 
from esra.extractors import ESRAE 
from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter
 

if __name__ == '__main__':
    
    abstracts = [
        """Natural language processing covers a wide variety of tasks predicting syntax, semantics, and information content, and usually each type of output is generated with specially designed architectures. In this paper, we provide the simple insight that a great variety of tasks can be represented in a single unified format consisting of labeling spans and relations between spans, thus a single task-independent model can be used across different tasks. We perform extensive experiments to test this insight on 10 disparate tasks spanning dependency parsing (syntax), semantic role labeling (semantics), relation extraction (information content), aspect based sentiment analysis (sentiment), and many others, achieving performance comparable to state-of-the-art specialized models. We further demonstrate benefits of multi-task learning, and also show that the proposed method makes it easy to analyze differences and similarities in how the model handles different tasks. Finally, we convert these datasets into a unified format to build a benchmark, which provides a holistic testbed for evaluating future models for generalized natural language analysis."""
    ]
    
    
    r = ESRAE.extract(abstracts)
    print(r) #
    list_valid_data = []
    list_invalid_data = []
    pp = Post_processor()
    cc = CycleCounter(threshold=3)

    for (i,data) in enumerate(r):

        # > all field except entity, relation and coref were deleted
        # > this just by-pass them, and i'wll fix it later
        # meta = {k:v for k, v in data.items() if k not in {'entities', 'relations', 'coreferences'}}
        
        data = coreference_handler(data)
        data = pp.post_processing(data)
        data = remove_generic(data)
        data = merge_conjuction_relation(data)
        data = duplicate_entity_handler(data)
        data = abbreviation_split(data)
        data = cc.drop_self_loops(data)
        
        # > paste metadata here
        # data.update(meta)

        if cc.cyclic_validate(data):
            list_invalid_data.append(data)
        else:
            list_valid_data.append(data)
    
    print(list_valid_data)
    print(list_invalid_data)

    entities = []
    ent_set = set()
    vectors = []

    for doc in list_valid_data:
        doc_entities = doc['entities']
        for entity in doc_entities:
            ent = entity[:2]
            ent = tuple(ent)
            if ent not in ent_set:
                ent_set.add(ent)
                entities.append(ent)
                vector = generate_vector(entity_name=ent[1])
                vectors.append(vector)
    
    ent_vec = {'vectors':vectors, 'entities': entities}

    with open('new_doc.pickle', 'wb') as f:
        pickle.dump(ent_vec,f)
        print('save pickle')
    # dot = filename.rfind('.')
    # out_filename = f'{filename[:dot]}_cleaned{filename[dot:]}'
    # print(out_filename)
    # with open(out_filename,'wb') as f:
    #     pickle.dump(list_valid_data,f)
    #     print("Done!")
