import re
import os
import json
import glob
import subprocess

from ..utils import nlp


# TODO: Make it object-oriented
# TODO: Make an extract in SpERT to be directly called and returned

def _split_punc(abstract):
    """abstract preprocessing"""
    if isinstance(abstract, str):
        return ' '.join([word.text for word in nlp(abstract)])
    elif isinstance(abstract, list):
        return [_split_punc(a) for a in abstract]
    
    
def _dump_json_data(abstracts):
    """export the abstract(s) to data.json format"""
    DATA = [{"tokens": abstract, 
            "entities": [{"type": "Task", "start": 0, "end": 1},
                        {"type": "Task", "start": 1, "end": 2}], 
            "relations": [{"type": "Part-of", "head": 0, "tail": 1}], 
            "orig_id": 1} for abstract in abstracts]
    with open('data.json', 'w') as f:
        json.dump(DATA, f)
        

def _get_latest_filepath():
    return max(glob.glob('data/log/scierc_eval/*/predictions*.json'))


def _interpret(result):
    tokens = result['tokens']
    entities = result['entities']
    relations = result['relations']
    
    out_entities = []
    out_relations = []

    for e in entities:
        word = ' '.join(tokens[e['start']:e['end']])
        out_entities += [[e['type'], word]]
 
    for r in relations:
        out_relations += [[r['type'], r['head'], r['tail']]]

    return {'entities': out_entities, 'relations': out_relations}


def extract(abstracts, interpret=True):
    
    os.chdir('./spert')

    abstracts = _split_punc(abstracts)
    _dump_json_data(abstracts)
    subprocess.call(["python3", "./spert.py", "eval", "--config", "configs/eval.conf"])
    
    # read output file
    filepath = _get_latest_filepath()
    with open(filepath) as f:
        preds = f.readlines()
        preds = eval(preds[0])
    
    os.chdir('..')
    
    if interpret:
        return [_interpret(ab) for ab in preds]
    else:
        return preds