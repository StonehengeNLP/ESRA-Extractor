import json
from esra.extractors import ESRAE

if __name__ == '__main__':
    
    # test sets of sciie and spert are different
    # sciie contains 100 abstracts
    # spert contains 551 sentences
    
    test = []
    with open('./SciERC/data/processed_data/json/test.json') as f:
        for i, line in enumerate(f):
            test.append(json.loads(line))    
    
    abstracts = []
    for document in test[:5]:
        abstract = ' '.join([word for sentence in document['sentences'] for word in sentence])
        # abstract = abstract.replace('-LRB- ', '(')
        # abstract = abstract.replace(' -RRB-', ')')
        # abstract = abstract.replace('-LSB- ', '[')
        # abstract = abstract.replace(' -RSB-', ']')
        # abstract = abstract.replace(' -- ', '-')
        # abstract = abstract.replace('`', '')
        # abstract = abstract.replace('"', '')
        # abstract = abstract.replace("'", '')
        abstracts += [abstract]

    results = ESRAE.extract(abstracts, interpret=False)
    
    # TODO: remove corefs that refer to no entity
    # TODO: calculate F1 for NER, Relation extraction, Coreference resolution
    
    print(document)
    print(results)