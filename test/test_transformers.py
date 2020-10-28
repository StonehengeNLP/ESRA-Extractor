from ..esra.transformers.abbreviation_splitter import abbreviation_split
from ..esra.transformers.conjunction_relations_merger import merge_conjuction_relation

def test_abbreviation_split():
    data_in = {'entities': [['OtherScientificTerm', 'black-box nature'],
                            ['Method', 'deep learning models'], 
                            ['Generic', 'methods'],
                            ['Generic', 'models'],
                            ['Method', 'model-agnostic and model-specific explanation methods'],
                            ['Method', 'Convolution Neural Network ( CNN ) challenge'],
                            ['Task', 'text classification'],
                            ['Task', 'human-grounded evaluations'],
                            ['OtherScientificTerm', 'model behavior'],
                            ['Method', 'model predictions'],
                            ['Method', 'explanation methods'],
                            ['Generic', 'methods']],
                'relations':[['USED-FOR', 5, 2],
                            ['USED-FOR', 3, 5],
                            ['USED-FOR', 1, 7]]}
    data_out = {'entities': [['OtherScientificTerm', 'black-box nature'], 
                            ['Method', 'deep learning models'], 
                            ['Generic', 'methods'], 
                            ['Generic', 'models'],
                            ['Method', 'model-agnostic and model-specific explanation methods'], 
                            ['Method', 'Convolution Neural Network challenge'], 
                            ['Task', 'text classification'], 
                            ['Task', 'human-grounded evaluations'], 
                            ['OtherScientificTerm', 'model behavior'],
                            ['Method', 'model predictions'],
                            ['Method', 'explanation methods'],
                            ['Generic', 'methods'],
                            ['Abbreviation', 'CNN']],
                'relations': [['USED-FOR', 5, 2],
                            ['USED-FOR', 3, 5],
                            ['USED-FOR', 1, 7],
                            ['Refer-to', 12, 5]]}
    assert data_out == abbreviation_split(data_in)
    
# for testing normal case
def test_merge_conjuction_relation_normal():
    data_in = {'entities': [['Task', 'language understanding'],
                        ['Method', 'convolutional architecture'],
                        ['Method', 'Dynamic Convolutional Neural Network'],
                        ['Task', 'semantic modelling'],
                        ['Method', 'Dynamic k-Max Pooling'],
                        ['Method', 'global pooling operation'],
                        ['OtherScientificTerm', 'feature graph'],
                        ['OtherScientificTerm', 'parse tree'],
                        ['Task', 'multi-class sentiment prediction'],
                        ['Task', 'six-way question classification'],
                        ['Task', 'Twitter sentiment prediction'],
                        ['OtherScientificTerm', 'distant supervision'],
                        ['Abbreviation', 'DCNN']],
            'relations': [['HYPONYM-OF', 2, 1],
                        ['HYPONYM-OF', 2, 1],
                        ['USED-FOR', 4, 2],
                        ['USED-FOR', 7, 2],
                        ['CONJUNCTION', 8, 9],
                        ['CONJUNCTION', 8, 10],
                        ['CONJUNCTION', 9, 10],
                        ['USED-FOR', 11, 10],
                        ['REFER-TO', 12, 2]]}
    data_out = {'entities': [['Task', 'language understanding'], 
                             ['Method', 'convolutional architecture'],
                             ['Method', 'Dynamic Convolutional Neural Network'],
                             ['Task', 'semantic modelling'], 
                             ['Method', 'Dynamic k-Max Pooling'], 
                             ['Method', 'global pooling operation'], 
                             ['OtherScientificTerm', 'feature graph'], 
                             ['OtherScientificTerm', 'parse tree'], 
                             ['Task', 'multi-class sentiment prediction'], 
                             ['Task', 'six-way question classification'], 
                             ['Task', 'Twitter sentiment prediction'], 
                             ['OtherScientificTerm', 'distant supervision'], 
                             ['Abbreviation', 'DCNN']], 
                'relations': [['HYPONYM-OF', 2, 1], 
                              ['HYPONYM-OF', 2, 1],
                              ['USED-FOR', 4, 2], 
                              ['USED-FOR', 7, 2], 
                              ['USED-FOR', 11, 10], 
                              ['REFER-TO', 12, 2], 
                              ['USED-FOR', 11, 8], 
                              ['USED-FOR', 11, 9]]}
    assert data_out == merge_conjuction_relation(data_in)
    
# for testing special case group have relation with group
def test_merge_conjuction_relation_special():
    data_in = {'entities': [['t','1'],['t','2'],['t','3'],['t','4'],['t','5'],['t','6'],['t','7'],['t','8']],
               'relations': [['CONJUNCTION', 1, 2],['CONJUNCTION', 1, 3],['CONJUNCTION', 2, 3],
                            ['CONJUNCTION', 6, 7],['CONJUNCTION', 6, 8],['CONJUNCTION', 7, 8],
                            ['USED-FOR',1,6]]}
    data_out = {'entities': [['t', '1'], ['t', '2'], ['t', '3'], ['t', '4'], ['t', '5'], ['t', '6'], ['t', '7'], ['t', '8']], 
                'relations': [['USED-FOR', 1, 6], ['USED-FOR', 1, 7], ['USED-FOR', 1, 8], ['USED-FOR', 2, 6], ['USED-FOR', 2, 7], 
                              ['USED-FOR', 2, 8], ['USED-FOR', 3, 6], ['USED-FOR', 3, 7], ['USED-FOR', 3, 8]]}
    assert data_out == merge_conjuction_relation(data_in)