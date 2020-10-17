import spacy

try:
    import en_core_web_lg
except ModuleNotFoundError:
    print("Spacy model not found!, importing small model")
    import en_core_web_sm

# Post-processing flow:
#   - separate conjunction first
#   - then lemmatize

class Post_processor:

    def __init__(self):
        # init model and disabling unuse module(s)
        try:
            self.model = en_core_web_lg.load(disable=["ner", "tagger"])
            print("Set SpaCy model to large model")
        except:
            self.model = en_core_web_sm.load(disable=["ner", "tagger"])         
            print("Set SpaCy model to small model")

    
    def _find_root(self, idx, compound_indexes):
        """
            find start index of the compound phase

            params: 

                - idx(int): input index

                - compound_indexes(dict[int]): dict contains head of 
                  each compound word
            
            return:

                - root_index(int): index of root, if not found then 
                  return -1
        """
        if idx not in compound_indexes:
            return idx # root 
        else:
            root = min(compound_indexes[idx])
            while root in compound_indexes:
                root = min(compound_indexes[root])
            return root
        return -1

    def _retrieve_indexes(self, doc):
        """
            Retrieve relate compoment for spltting conjunction

            params:

                - doc(Doc): spacy Doc object
            
            return:

                - heads(list[Token]): list of token's head object

                - conj_indexes(list[int]): list of indexes of 
                  conjunction head

                - compound_indexes(dict[list[int]]): dict of compound
                  and dep related index, used for find starting point of 
                  each word
        """
        heads = []
        conj_indexes = set()
        compound_indexes = {}
        for (i,tok) in enumerate(doc):
            heads.append(tok.head)
            dep = tok.dep_
            head_idx = tok.head.i
            if dep == "conj":
                conj_indexes.add(i)
                conj_indexes.add(head_idx)
            if dep == "compound" or dep == "dep":
                compound_indexes[head_idx] = \
                    compound_indexes.get(head_idx, []) + [i] 
        return (
            heads,
            conj_indexes,
            compound_indexes
        )
    
    # def _find_compound(self, doc, conj_indexes, compound_indexes):
    

    def _conjunction_spliter(self, doc):
        """
            Split coordinate conjunction into several entity.
            
            Because each sentence structure is:

                Front + Compound + (cc) + Compound + Back
            
            this function will split sentence into:

                Front + Compound + Back
            
            params:

                - doc(spacy Doc): input Doc class object 
            
            return:

                - generate_entities(list[str]): output generated 
                  entity
        """
        # retrieve indexes
        heads, conj_indexes, compound_indexes = \
            self._retrieve_indexes(doc)

        # init used_indexes to store used index
        used_indexes = set()
    
        # Back component index
        back_index = heads[doc[min(conj_indexes)].head.i].i
        back_index = self._find_root(back_index, compound_indexes)
        back = doc[back_index:].text
        used_indexes.add(back_index)

        # Compound component
        compounds = []
        for con in conj_indexes:
            if con in compound_indexes:    
                start_idx = self._find_root(con,compound_indexes)
                compounds.append(doc[start_idx:con+1].text)
                used_indexes.add(start_idx)
            else:
                compounds.append(doc[con].text)
                used_indexes.add(con)
        
        # Front component
        front = doc[:min(used_indexes)].text
        
        # generate entities 
        generated_entities = []
        for compound in compounds:
            generated_entities.append(
                " ".join([front,compound,back])
            )
        return generated_entities

    def _lemmatizer(self, doc):
        """
            Return entire entity name with last token being 
            tokenize
        """
        return doc[:-1].text + " " + doc[-1].lemma_

    def post_precessing(self, entity):
        """
            Post processing function, include conjunction separator
            and name lemmatizer.

            params: 

                - entity(str), input entity name 

            return:

                - generate entity names(list[str])
        """
        doc = self.model(entity)
        processed_entities = self._conjunction_spliter(doc)
        for (i,en) in enumerate(processed_entities):
            tmp = self.model(en)
            processed_entities[i] = self._lemmatizer(tmp)
        return processed_entities