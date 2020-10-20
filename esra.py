import sys
import pandas as pd

from esra.extractors import ESRAE
from esra.loaders import csv_file
from esra.transformers.cycle_counter import CycleCounter
from esra.transformers.post_processing import Post_processor
from esra.transformers.entity_merging import merge_entity
from esra.transformers.abbreviation_splitter import abbreviation_split
 

if __name__ == '__main__':
    
    abstracts = [
        "The ability to accurately represent sentences is central to language understanding. We describe a convolutional architecture dubbed the Dynamic Convolutional Neural Network (DCNN) that we adopt for the semantic modelling of sentences. The network uses Dynamic k-Max Pooling, a global pooling operation over linear sequences. The network handles input sentences of varying length and induces a feature graph over the sentence that is capable of explicitly capturing short and long-range relations. The network does not rely on a parse tree and is easily applicable to any language. We test the DCNN in four experiments: small scale binary and multi-class sentiment prediction, six-way question classification and Twitter sentiment prediction by distant supervision. The network achieves excellent performance in the first three tasks and a greater than 25% error reduction in the last task with respect to the strongest baseline.",
        ]
    
    r = ESRAE.extract(abstracts)
    print(r)
    # CycleCounter = CycleCounter(2)
    # PostProcessor = Post_processor()
    
    # for data in results:
    #     data = merge_entity(data)
    #     data = abbreviation_split(data)
    #     data = PostProcessor.post_processing(data)
    #     print(data)
    #     if CycleCounter.cyclic_validate(data)):
    #         # TODO: merge
    #         # pass
