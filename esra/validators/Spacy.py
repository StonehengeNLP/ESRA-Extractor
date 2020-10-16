import spacy

try:
    import en_core_web_lg
except ModuleNotFoundError:
    print("Spacy model not found!")

# Post-processing flow:
#   - separate conjunction first
#   - then lemmatize

class Post_processor:

    def __init__(self):
        # init model and disabling unuse module(s)
        self.model = en_core_web_md.load(disable=["ner", "tagger"])
    
    def _lemmatizer(self, doc):
        """
            Return entire entity name with last token being 
            tokenize
        """
        return doc[:-1] + " " + doc[-1].lemma_

    def _conjunction_spliter(self, doc):
        """
            Split coordinate conjunction into several entity
        """
        generated_entities = []
        texts = []
        heads = []
        deps = []
        cc_idx = []
        conj_idx = []
        for (i,token) in enumerate(doc):
            texts.append(token.text)
            heads.append(token.head)
            deps.append(token.dep_)
            if token.dep_ == "cc" or token.dep_ == "punct": 
                cc_idx.append(i)
            if token.dep_ == "conj":
                conj_idx.append(i)
        individual_words = set(
            [texts[i] for i in conj_idx] + \
            [heads[i] for i in conj_idx]
            )
        backside_start_idx = heads[conj_idx[0]].i
        

        return generated_entities

    def post_precessing(self, entity):
        """
            Post processing function, include conjunction separator
            and name lemmatizer
        """
        doc = self.model(entity)
        processed_entities = self._conjunction_spliter(doc)
        for (i,en) in enumerate(processed_entities):
            tmp = self.model(en)
            processed_entities[i] = self._lemmatizer(tmp)
        return processed_entities
            

    

