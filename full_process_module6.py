import pickle

from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter

filename = './pickle/arxiv_cscl_200.pickle'
 
with open(filename, 'rb') as f:
    list_data = pickle.load(f)

list_valid_data = []
list_invalid_data = []
pp = Post_processor()
cc = CycleCounter(threshold=3)

for (i,data) in enumerate(list_data):

    # > all field except entity, relation and coref were deleted
    # > this just by-pass them, and i'wll fix it later
    meta = {k:v for k, v in data.items() if k not in {'entities', 'relations', 'coreferences'}}
    
    data = coreference_handler(data)
    data = pp.post_processing(data)
    data = remove_generic(data)
    data = merge_conjuction_relation(data)
    data = duplicate_entity_handler(data)
    data = abbreviation_split(data)
    data = cc.drop_self_loops(data)
    
    # > paste metadata here
    data.update(meta)

    if cc.cyclic_validate(data):
        list_invalid_data.append(data)
    else:
        list_valid_data.append(data)
    
dot = filename.rfind('.')
out_filename = f'{filename[:dot]}_cleaned{filename[dot:]}'
print(out_filename)
with open(out_filename,'wb') as f:
    pickle.dump(list_valid_data,f)
    print("Done!")
