import re
import os
import json
import glob
import subprocess

os.chdir('spert')


def _split_punc(abstract):
    """abstract preprocessing"""
    if isinstance(abstract, str):
        return re.sub(r'([\.,:;()])', r' \1 ', abstract)
    elif isinstance(abstract, list):
        return [_split_punc(a) for a in abstract]
    
    
def _dump_json_data(abstracts):
    """export the abstract(s) to data.json format"""
    DATA = [{"tokens": abstract.split(), 
            "entities": [{"type": "Task", "start": 0, "end": 1},
                        {"type": "Task", "start": 1, "end": 2}], 
            "relations": [{"type": "Part-of", "head": 0, "tail": 1}], 
            "orig_id": 1} for abstract in abstracts]
    with open('data.json', 'w') as f:
        json.dump(DATA, f)
        

def _get_latest_filepath():
    return max(glob.glob('data/log/scierc_eval/*/predictions*.json'))


def extract(abstracts):
    abstracts = _split_punc(abstracts)
    _dump_json_data(abstracts)
    subprocess.call(["python3", "./spert.py", "eval", "--config", "configs/eval.conf"])
    
    # read output file
    filepath = _get_latest_filepath()
    with open(filepath) as f:
        preds = f.readlines()
        preds = eval(preds[0])
        return preds
    # relation_all = []
    # for p in preds:
    #     tokens = p['tokens']
    #     entities = [' '.join(tokens[e['start']:e['end']]) for e in p['entities']]
    #     relations = [(entities[r['head']], r['type'], entities[r['tail']]) for r in p['relations']]
    #     relation_all += relations
    # print(relation_all)