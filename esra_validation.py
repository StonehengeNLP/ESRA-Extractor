import re
import tqdm
import glob
import pickle

from esra.transformers.entity_merging import coreference_handler
from esra.transformers.post_processing import Post_processor
from esra.transformers.generic_remover import remove_generic
from esra.transformers.conjunction_relations_merger import merge_conjuction_relation
from esra.transformers.entity_merging import duplicate_entity_handler
from esra.transformers.abbreviation_splitter import abbreviation_split
from esra.transformers.cycle_counter import CycleCounter

list_data = []
for filename in glob.glob('./data/pickle/data_5000*')[:-1]:
    print(filename)
    with open(filename, 'rb') as f:
        list_data += pickle.load(f)
print(len(list_data))

list_valid_data = []
list_invalid_data = []
pp = Post_processor()
cc = CycleCounter(threshold=3)

for data in tqdm.tqdm(list_data):
    
    # NOTE: Pass data id for identification purpose
    meta = {'id': data['id']}
    
    data = coreference_handler(data)
    data = abbreviation_split(data)
    data = pp.post_processing(data)
    data = remove_generic(data)
    data = merge_conjuction_relation(data)
    
    # NOTE: Hot fix name of entities
    for en in data['entities']:
        en[1] = en[1].lower()
        en[1] = re.sub(r'( \- |\- | \-)', '-', en[1]) # connect hyphens
        en[1] = re.sub(r'[\(\)]', '', en[1]) # remove single sided parenthesis
        en[1] = re.sub(r' +', ' ', en[1]) # remove double spaces
        en[1] = en[1].strip()
            
    data = duplicate_entity_handler(data)
    data = cc.drop_self_loops(data)
    
    # NOTE: Add data id here
    data.update(meta)

    if cc.cyclic_validate(data):        
        list_invalid_data.append(data)
    else:
        list_valid_data.append(data)
    
with open('./data/pickle/data_5000_cleaned.pickle','wb') as f:
    pickle.dump(list_valid_data,f)
    print("Done!")