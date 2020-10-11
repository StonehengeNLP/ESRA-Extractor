import re
import json


def split_punc(abstract):
    if isinstance(abstract, str):
        return re.sub(r'([\.,:;()])', r' \1 ', abstract)
    elif isinstance(abstract, list):
        return [re.sub(r'([\.,:;()])', r' \1 ', a) for a in abstract]
    
def dump_data(abstracts):
    DATA = [{"tokens": abstract.split(), 
            "entities": [{"type": "Task", "start": 0, "end": 1},
                        {"type": "Task", "start": 1, "end": 2}], 
            "relations": [{"type": "Part-of", "head": 0, "tail": 1}], 
            "orig_id": 1} for abstract in abstracts]
    with open('data.json', 'w') as f:
        json.dump(DATA, f)