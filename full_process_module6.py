from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter

data = {'coreferences': [[2, 3], [2, 5, 8, 10, 18], [3, 12]],
        'entities': [['Task', 'language understanding'],
                    ['Method', 'convolutional architecture'],
                    ['Method', 'Dynamic Convolutional Neural Network'],
                    ['Method', 'Dynamic Convolutional Neural Network ( DCNN )'],
                    ['Task', 'semantic modelling'],
                    ['Generic', 'network'],
                    ['Method', 'Dynamic k-Max Pooling'],
                    ['Method', 'global pooling operation'],
                    ['Generic', 'network'],
                    ['OtherScientificTerm', 'feature graph'],
                    ['Generic', 'network'],
                    ['OtherScientificTerm', 'parse tree'],
                    ['Metric', 'DCNN'],
                    ['Generic', 'experiments'],
                    ['Task', 'multi-class sentiment prediction'],
                    ['Task', 'six-way question classification'],
                    ['Task', 'Twitter sentiment prediction'],
                    ['OtherScientificTerm', 'distant supervision'],
                    ['Generic', 'network']],
        'relations': [['HYPONYM-OF', 2, 1],
                    ['HYPONYM-OF', 3, 1],
                    ['USED-FOR', 6, 5],
                    ['USED-FOR', 11, 10],
                    ['EVALUATE-FOR', 13, 12],
                    ['HYPONYM-OF', 14, 13],
                    ['CONJUNCTION', 14, 15],
                    ['CONJUNCTION', 14, 16],
                    ['HYPONYM-OF', 15, 13],
                    ['CONJUNCTION', 15, 16],
                    ['HYPONYM-OF', 16, 13],
                    ['USED-FOR', 17, 16]]}

pp = Post_processor()
cc = CycleCounter(threshold=3)

data = coreference_handler(data)
data = pp.post_processing(data)
data = remove_generic(data)
data = merge_conjuction_relation(data)
data = duplicate_entity_handler(data)
data = abbreviation_split(data)

if cc.cyclic_validate(data):
    print('Invalid graph')
else:
    print('Valid graph')

print(data)
