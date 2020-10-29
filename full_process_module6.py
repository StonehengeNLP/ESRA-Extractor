import pickle

from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter

with open('triple_CNN_10.pickle', 'rb') as f:
        list_data = pickle.load(f)

list_valid_data = []
list_invalid_data = []
pp = Post_processor()
cc = CycleCounter(threshold=3)

for (i,data) in enumerate(list_data):
    print(i)
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

print(len(list_valid_data))

# data = {'entities': [['OtherScientificTerm', 'convolutional network depth'], ['Metric', 'accuracy'], ['Task', 'large-scale image recognition setting'], ['OtherScientificTerm', 'networks'], ['Generic', 'architecture'], ['Method', 'convolution filters'], ['Material', 'ImageNet Challenge 2014 submission'], ['OtherScientificTerm', 'localisation and classification tracks'], ['Generic', 'representations'], ['Generic', 'datasets'], ['Generic', 'they'], ['Method', 'ConvNet models'], ['Method', 'deep visual representations'], ['Task', 'computer vision']], 'relations': [['Used-for', 0, 2], ['Evaluate-for', 1, 3], ['Evaluate-for', 2, 3], ['Used-for', 8, 9], ['Used-for', 11, 12], ['Used-for', 12, 13]], 'coreferences': [[8, 10]]}
# data = coreference_handler(data)
# data = pp.post_processing(data)
#     data = remove_generic(data)
#     data = merge_conjuction_relation(data)
#     data = duplicate_entity_handler(data)
#     data = abbreviation_split(data)

# print(data)