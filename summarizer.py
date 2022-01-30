# General I
import torch
import pickle
from transformers import T5ForConditionalGeneration,T5Tokenizer

summary_model = T5ForConditionalGeneration.from_pretrained('t5-large')
summary_tokenizer = T5Tokenizer.from_pretrained('t5-large')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
summary_model = summary_model.to(device)

pickle.dump(summary_model, open('abstraction-model.pkl','wb'))

# General II
import random
import numpy as np

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_seed(7)

#General III

import nltk
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize

#General IV

def postprocesstext (content):
  final=""
  for sent in sent_tokenize(content):
    sent = sent.capitalize()
    final = final +" "+sent
  return final
