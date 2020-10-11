import sys
import subprocess

import re
import json


def split_punc(abstract):
    if isinstance(abstract, str):
        return re.sub(r'([\.,:;()])', r' \1 ', abstract)
    elif isinstance(abstract, list):
        return [split_punc(a) for a in abstract]
    
def dump_data(abstracts):
    DATA = [{"tokens": abstract.split(), 
            "entities": [{"type": "Task", "start": 0, "end": 1},
                        {"type": "Task", "start": 1, "end": 2}], 
            "relations": [{"type": "Part-of", "head": 0, "tail": 1}], 
            "orig_id": 1} for abstract in abstracts]
    with open('data.json', 'w') as f:
        json.dump(DATA, f)
        
def what():
    import glob
    def get_latest_filepath():
        return max(glob.glob('data/log/custom/*/predictions*.json'))
    file_path = get_latest_filepath()
    with open(file_path) as f:
        preds = f.readlines()
        preds = eval(preds[0])

    relation_all = []
    for p in preds:
        tokens = p['tokens']
        entities = [' '.join(tokens[e['start']:e['end']]) for e in p['entities']]
        relations = [(entities[r['head']], r['type'], entities[r['tail']]) for r in p['relations']]
        relation_all += relations
    print(relation_all)

def _extract():
    abstracts = ["Due to the black-box nature of deep learning models, methods for explaining the models’ results are crucial to gain trust from humans and support collaboration between AIs and humans. In this paper, we consider several model-agnostic and model-specific explanation methods for CNNs for text classification and conduct three human-grounded evaluations, focusing on different purposes of explanations: (1) revealing model behavior, (2) justifying model predictions, and (3) helping humans investigate uncertain predictions. The results highlight dissimilar qualities of the various explanation methods we consider and show the degree to which these methods could serve for each purpose."]
    abstracts = split_punc(abstracts)
    dump_data(abstracts)
    subprocess.call(["python3", "./spert/spert.py", "eval", "--config", "spert/configs/eval.conf"])
    what()

if __name__ == '__main__':
    _extract()