# Candidate entities generator

import torch
import numpy as np

try:
    from transformers import *
except:
    raise ImportError("Unable to load transformers")

class Entity_Embedder:
    """
        A class for embedding entity name to embedding vector using SciBERT
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

    def last_layer_embedding(self, entity_name):
        """
            Return entity name embedding generate from last hidden layer
        """
        tokens = self.tokenizer.encode(entity_name, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(tokens)
        last_layer = model_output[0]
        return last_layer[:,0,:].cpu().detach().numpy().flatten() # CLS 

    def sum_4_layers_embedding(self, entity_name):
        """
            Return entity name embedding generate from sum of last 4 layers
        """
        tokens = self.tokenizer.encode(entity_name, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(tokens)
        embedding = torch.stack(
            [hidden_layer for hidden_layer in model_output[2][-4:]]
        ).sum(dim=0)[:,0,:]
        return embedding.cpu().detach().numpy().flatten()

    def second_last_layer_embedding(self, entity_name):
        """
            Return entity name embedding generate from second-to-last hidden
            layer
        """
        tokens = self.tokenizer.encode(entity_name, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(tokens)
        hidden_states = model_output[2]
        # select CLS token embedding 
        out = hidden_states[-2][:,0,:].mean(dim=0)
        return out.cpu().detach().numpy().flatten()