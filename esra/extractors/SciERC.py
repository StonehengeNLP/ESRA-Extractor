import re
import os
import json
import glob
import random
import string
import subprocess

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def _split_punc(abstract):
    """abstract preprocessing"""
    if isinstance(abstract, str):
        return re.sub(r'([\.,:;()])', r' \1 ', abstract)
    elif isinstance(abstract, list):
        return [_split_punc(a) for a in abstract]


def _dump_json_data(abstracts):
    """export the abstract(s) to data.json format"""
    
    data = []
    
    for abstract in abstracts:
        sentences = [[]]
        for e in abstract.split():
            sentences[-1] += [e]
            if e == '.':
                sentences += [[]]
        data += [{"clusters": [],
                "sentences": sentences[:-1],
                "ner": [[] for _ in range(len(sentences))],
                "relation": [[] for _ in range(len(sentences))],
                "doc_key": get_random_string(6)}]
        
    with open('./data/processed_data/json/dev.json', 'w') as f:
        for line in data:
            json.dump(line, f)
            f.write('\n')
            

def extract(abstracts):
    
    os.chdir('./SciERC')
    
    abstracts = _split_punc(abstracts)
    _dump_json_data(abstracts)
    
    # bug alert!
    subprocess.call(["python3", "generate_elmo.py", "--input", "./data/processed_data/json/dev.json", "--output", "./data/processed_data/elmo/dev.hdf5"])
    subprocess.call(["python3", "write_single.py", "scientific_best_coref"])
    
    # read output file
    filepath = "output.json"
    out = []
    with open(filepath) as f:
        for line in f:
            out.append(json.loads(line))
    
    os.chdir('..')
    
    return out