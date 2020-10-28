import json
import copy
from collections import Counter
from SciERC import relation_metrics, coref_metrics
from esra.extractors import ESRAE

def unroll_document(documents):
    """formatting the traditional SciERC to computable format"""
    if isinstance(documents, dict):
        tokens = copy.deepcopy(documents['sentences'])
        entities = copy.deepcopy(documents['ner'])
        relations = copy.deepcopy(documents['relations'])
        corefs = copy.deepcopy(documents['clusters'])
        tokens = [t for l in tokens for t in l]
        entities = [e for l in entities for e in l]
        relations = [r for l in relations for r in l]
        return {'tokens': tokens, 'entities': entities, 'relations': relations, 'coref': corefs}
    
    elif isinstance(documents, list):
        return [unroll_document(doc) for doc in documents]
    
def _print_f1(total_gold, total_predicted, total_matched, message=""):
    precision = 100.0 * total_matched / total_predicted if total_predicted > 0 else 0
    recall = 100.0 * total_matched / total_gold if total_gold > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    print(("{}: Precision: {}, Recall: {}, F1: {}".format(message, precision, recall, f1)))
    return precision, recall, f1

def compute_entity_f1(gold_data, predictions):
    assert len(gold_data) == len(predictions)
    total_gold = 0
    total_predicted = 0
    total_matched = 0
    total_unlabeled_matched = 0
    label_confusions = Counter()  # Counter of (gold, pred) label pairs.
    for i in range(len(gold_data)):
        gold = gold_data[i]
        pred = predictions[i]
        total_gold += len(gold)
        total_predicted += len(pred)
        for a0 in gold:
            for a1 in pred:
                a0_start, a0_end, a0_type = a0
                a1_start, a1_end, a1_type = a1['start'], a1['end'], a1['type']
                if a0_start == a1_start and a0_end + 1 == a1_end:
                    total_unlabeled_matched += 1
                    label_confusions.update([(a0_type, a1_type),])
                    if a0_type == a1_type:
                        total_matched += 1
    prec, recall, f1 = _print_f1(total_gold, total_predicted, total_matched, 'NER')
    ul_prec, ul_recall, ul_f1 = _print_f1(total_gold, total_predicted, total_unlabeled_matched, "Unlabeled NER")
    return prec, recall, f1, ul_prec, ul_recall, ul_f1, label_confusions

def compute_relation_f1(gold_rels, predictions):
    assert len(gold_rels) == len(predictions)
    total_gold = 0
    total_predicted = 0
    total_matched = 0
    total_unlabeled_matched = 0
    label_confusions = Counter()
    # Compute unofficial F1 of entity relations.
    doc_id = 0  # Actually sentence id.
    gold_tuples = []  # For official eval.
    predicted_tuples = []
    for gold, prediction in zip(gold_rels, predictions):
        total_gold += len(gold)
        total_predicted += len(prediction)
        for g in gold:
            gold_tuples.append([["d{}_{}_{}".format(doc_id, g[0], g[1]+1),
                                "d{}_{}_{}".format(doc_id, g[2], g[3]+1)], g[4]])
            for p in prediction:
                if g[0] == p[0] and g[1] + 1 == p[1] and g[2] == p[2] and g[3] + 1 == p[3]:
                    total_unlabeled_matched += 1
                    if g[4] == p[4].upper():
                        total_matched += 1
                    break
        for p in prediction:
            predicted_tuples.append([["d{}_{}_{}".format(doc_id, p[0], p[1]),
                                    "d{}_{}_{}".format(doc_id, p[2], p[3])], p[4]])
        doc_id += 1
    precision, recall, f1 = _print_f1(total_gold, total_predicted, total_matched, "Relations (unofficial)")
    ul_prec, ul_recall, ul_f1 = _print_f1(total_gold, total_predicted, total_unlabeled_matched, "Unlabeled (unofficial)")
    relation_metrics.span_metric(gold_tuples, predicted_tuples)
    return precision, recall, f1

def compute_coref_f1(gold_corefs, predictions):
    assert len(gold_corefs) == len(predictions)
    coref_evaluator = coref_metrics.CorefEvaluator()
    for gold, prediction in zip(gold_corefs, predictions):
        mention_to_predicted = {}
        mention_to_gold = {}
        for pc in prediction:
            for mention in pc:
                mention_to_predicted[mention] = pc
        for gc in gold:
            for mention in gc:
                mention_to_gold[mention] = gc
        coref_evaluator.update(prediction, gold, mention_to_predicted, mention_to_gold)
    precision, recall, f1 = coref_evaluator.get_prf()
    print(("{}: Precision: {}, Recall: {}, F1: {}".format("Coreferences", precision*100, recall*100, f1*100)))
    return precision, recall, f1
 

if __name__ == '__main__':
    
    # test sets of sciie and spert are different
    # sciie contains 100 abstracts
    # spert contains 551 sentences
    
    documents = []
    with open('./SciERC/data/processed_data/json/test.json') as f:
        for i, line in enumerate(f):
            documents.append(json.loads(line))
    
    abstracts = []
    for doc in documents:
        abstract = ' '.join([word for sentence in doc['sentences'] for word in sentence])
        # abstract = abstract.replace('-LRB- ', '(')
        # abstract = abstract.replace(' -RRB-', ')')
        # abstract = abstract.replace('-LSB- ', '[')
        # abstract = abstract.replace(' -RSB-', ']')
        # abstract = abstract.replace(' -- ', '-')
        # abstract = abstract.replace('`', '')
        # abstract = abstract.replace('"', '')
        # abstract = abstract.replace("'", '')
        abstracts += [abstract]

    documents = unroll_document(documents)
    results = ESRAE.extract(abstracts, interpret=False)

    # Compute entity F1
    gold_entities = [d['entities'] for d in documents]
    pred_entities = [d['entities'] for d in results]
    compute_entity_f1(gold_entities, pred_entities)
    
    # Compute relation F1
    sentences = [d['tokens'] for d in documents]
    gold_relations = [d['relations'] for d in documents]
    pred_relations = []
    for i in range(len(results)):
        d = results[i]
        pr = []
        for r in d['relations']:
            head, tail, type_ = r['head'], r['tail'], r['type']
            w1s, w1e = pred_entities[i][head]['start'], pred_entities[i][head]['end']
            w2s, w2e = pred_entities[i][tail]['start'], pred_entities[i][tail]['end']
            pr.append([w1s, w1e, w2s, w2e, type_])
        pred_relations.append(pr)
    compute_relation_f1(gold_relations, pred_relations)
    
    # Compute coreference F1
    gold_coref = [[tuple(tuple(i) for i in c) for c in d['coref']] for d in documents]
    pred_coref = []
    # filter out unmatched entities in coref group
    for i in range(len(results)):
        entities = results[i]['entities']
        corefs = results[i]['coref']
        e_set = {e['start'] for e in entities}
        filtered_cluster = []
        for cluster in corefs:
            filtered_entity = []
            for e in cluster:
                if e[0] in e_set:
                    filtered_entity += [tuple(e)]
            if len(filtered_entity) != 0:
                filtered_cluster.append(tuple(filtered_entity))
        pred_coref.append(filtered_cluster)
    # pred_coref = [[tuple(tuple(i) for i in c) for c in d['coref']] for d in results]
    compute_coref_f1(gold_coref, pred_coref)