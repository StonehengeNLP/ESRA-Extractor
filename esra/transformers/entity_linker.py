# Candidate entities generator

import torch
import numpy as np

try:
    from transformers import *
except:
    raise ImportError("Unable to load transformers")

class Entity_Embedder:
    """
        A class for embedding entity name to embedding vector
    """

    # use SciBERT
    tokenizer = BertTokenizer.from_pretrained(
        'allenai/scibert_scivocab_uncased'
    )
    model = BertModel.from_pretrained(
        'allenai/scibert_scivocab_uncased',
        output_hidden_states=True
    )
    model.eval()

    def __init__(self):
        pass

    def generate_emb_vector(self, entity_name):
        """
            Return entity name embedding numpy array
        """
        tokens = self.tokenizer.encode(entity_name, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(tokens)
        hidden_states = model_output[2]
        # create sentence embedding frim hidden states 
        out = hidden_states[-2][0].mean(dim=0)
        return out.detach().numpy()