import pickle

from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter

with open('./pickle/triple_CNN_10.pickle', 'rb') as f:
    list_data = pickle.load(f)

list_valid_data = []
list_invalid_data = []
pp = Post_processor()
cc = CycleCounter(threshold=3)

for (i,data) in enumerate(list_data):

    data = coreference_handler(data)
    data = pp.post_processing(data)
    data = remove_generic(data)
    data = merge_conjuction_relation(data)
    data = duplicate_entity_handler(data)
    data = abbreviation_split(data)

    if cc.cyclic_validate(data):
        list_invalid_data.append(data)
    else:
        list_valid_data.append(data)

with open('./pickle/triple_CNN_10_cleaned.pickle','wb') as f:
        pickle.dump(list_valid_data,f)
        print("Done!")