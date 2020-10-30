from ..esra.transformers.cycle_counter import CycleCounter

def test_cyclic_validate_pass():

    cc = CycleCounter(threshold=2)

    data_in = {'entities': [['OtherScientificTerm', 'black-box nature'],
                            ['Method', 'deep learning models'], 
                            ['Generic', 'methods'],
                            ['Generic', 'models'],
                            ['Method', 'model-agnostic and model-specific explanation methods'],
                            ['Method', 'CNNs'],
                            ['Task', 'text classification'],
                            ['Task', 'human-grounded evaluations'],
                            ['OtherScientificTerm', 'model behavior'],
                            ['Method', 'model predictions'],
                            ['Method', 'explanation methods'],
                            ['Generic', 'methods']],
                'relations':[['USED-FOR', 1, 2],
                            ['USED-FOR', 2, 3],
                            ['USED-FOR', 7, 7]]
                }
    
    data_out = False

    assert data_out == cc.cyclic_validate(data_in)
    
def test_cyclic_validate_fail():

    cc = CycleCounter(threshold=1)

    data_in = {'entities': [['OtherScientificTerm', 'black-box nature'],
                            ['Method', 'deep learning models'], 
                            ['Generic', 'methods'],
                            ['Generic', 'models'],
                            ['Method', 'model-agnostic and model-specific explanation methods'],
                            ['Method', 'CNNs'],
                            ['Task', 'text classification'],
                            ['Task', 'human-grounded evaluations'],
                            ['OtherScientificTerm', 'model behavior'],
                            ['Method', 'model predictions'],
                            ['Method', 'explanation methods'],
                            ['Generic', 'methods']],
                'relations':[['USED-FOR', 1, 2],
                            ['USED-FOR', 2, 3],
                            ['USED-FOR', 7, 7],
                            ['USED-FOR', 8, 8]]
                }
    
    data_out = True

    assert data_out == cc.cyclic_validate(data_in)