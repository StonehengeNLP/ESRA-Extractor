from esra.extractors import SciERC, SpERT


def _interpret(result):
    tokens = result['tokens']
    entities = result['entities']
    relations = result['relations']
    coref = result['coref']
    
    words = {}
    out_entities = []
    out_relations = []
    out_corefs = []

    for e in entities:
        word = ' '.join(tokens[e['start']:e['end']])
        words[e['start']] = len(words)
        out_entities += [[e['type'], word]]
 
    for r in relations:
        out_relations += [[r['type'], r['head'], r['tail']]]

    # the corefs from SciERC which refer to none entity in SpERT will be ejected
    for c in coref:
        for start, end in c:
            if start in words:
                out_corefs += [[words[start]]]

    return {'entities': out_entities, 'relations': out_relations, 'coreferences': out_corefs}

    
def extract(abstracts, interpret=True):
    
    # NER and Relations are from SpERT, but Corefs are from SciERC
    result_spert = SpERT.extract(abstracts, interpret=False)
    result_scierc = SciERC.extract(abstracts, interpret=False)
    out = [dict(sp, **{'coref': sc['coref']}) for sp, sc in zip(result_spert, result_scierc)]
    
    if interpret:
        return [_interpret(ab) for ab in out]
    else:
        return out