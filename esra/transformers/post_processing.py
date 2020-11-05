import spacy
import inflection
try:
    import en_core_web_md
except ModuleNotFoundError:
    print("Spacy model not found!, importing small model")
    import en_core_web_sm

# Post-processing flow:
#   - separate conjunction first
#   - then lemmatize

class Post_processor:
    """
        Post_processor class for ESRA validator module
        
        Init Post_processor class and you are good to go. 
        
        Process entitiy name by call .post_processing(entity). The 
        post-processing function will return list of newly generated 
        entities
    """
    def __init__(self):
        # init model and disabling unuse module(s)
        try:
            self.model = en_core_web_md.load()
            print("Set SpaCy model to medium model")
        except:
            self.model = en_core_web_sm.load()         
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
            if dep == "compound" or dep == "dep" or dep == "npadvmod":
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
        if len(conj_indexes) == 0:
            return [doc.text]
        elif max(conj_indexes) == len(doc) - 1:
            back_index = len(doc)
        else:
            back_index = doc[min(conj_indexes)].head.i
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
        return doc[:-1].text + " " + inflection.singularize(doc[-1].text)

    def _post_processing(self, entity):
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
            processed_entities[i] = self._lemmatizer(tmp).strip()
        return processed_entities
        
    def post_processing(self, data):
        entities = data['entities']
        relations = data['relations']
        len_entities = len(entities)
        _changes = {}
        
        # split the conjuncted entities
        for i, (_type, _name, _confidence) in enumerate(entities):
            processed_entities = self._post_processing(_name)
            if len(processed_entities) == 1:
                entities[i][1] = processed_entities[0]
            else:
                _changes[i] = processed_entities
        
        # append the entities
        for i in list(_changes.keys())[::-1]:
            _type, _name, _confidence = entities.pop(i)
            for _n in _changes[i]:
                entities.insert(i, [_type, _n, _confidence])
        
        # create index mapping
        _index_map = []
        _c = 0
        for i in range(len_entities):
            _index_map += [_c]
            if i in _changes:
                _c += len(_changes[i])
            else:
                _c += 1
        
        # map its relations
        _i = 0
        while _i < len(relations):
            relation = relations[_i] 
            if relation[1] in _changes and relation[2] in _changes:
                relations.pop(_i)
                for j in range(len(_changes[relation[1]])):
                    for k in range(len(_changes[relation[2]])):
                        relations.insert(_i + j + k, [relation[0], relation[1] + j, relation[2] + k, relation[3]])
                _i += len(_changes[relation[1]]) + len(_changes[relation[2]])
            elif relation[1] in _changes:
                for j in range(1, len(_changes[relation[1]])):
                    relations.insert(_i + j, [relation[0], relation[1] + j, relation[2], relation[3]])
                _i += len(_changes[relation[1]])
            elif relation[2] in _changes:
                for j in range(1, len(_changes[relation[2]])):
                    relations.insert(_i + j, [relation[0], relation[1], relation[2] + j, relation[3]])
                _i += len(_changes[relation[2]])
            else:
                relation[1] = _index_map[relation[1]]
                relation[2] = _index_map[relation[2]]
                _i += 1
        return data