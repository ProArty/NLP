from lib.PerceptronTagger import PerceptronTagger
from lib.Linear import Linear
from constants.globals import PAD
import re

class GoldTagger(PerceptronTagger):

    def __init__(self, vocab_words, vocab_tags, encoded = True):
        self.vocab_words = vocab_words
        self.vocab_tags = vocab_tags
        self.most_frequent = {}
        self.pre_sufix = {}
        self.fallback = None
        if encoded:
            self.model = Linear(len(vocab_tags))
        else:
            self.model = Linear(len(vocab_tags), vocab_tags)


    def featurize(self, words, i, pred_tags, next_tag):
        ENC_PAD = self.vocab_words[PAD]
        features = []

        features.append((0,words[i]))
        features.append((1,words[i-1]) if i != 0 else ENC_PAD )
        features.append((2 ,words[i+1] if i + 1 < len(words) else ENC_PAD))
        features.append((3 ,pred_tags[i-1] if i != 0 else ENC_PAD))
        features.append((4 ,(pred_tags[i-2] if i > 1 else ENC_PAD, pred_tags[i-1] if i != 0 else ENC_PAD)))
        features.append((5, self.pre_sufix[words[i][:1] ] if words[i][:1] in self.pre_sufix else ENC_PAD))
        features.append((6, self.pre_sufix[words[i][:2] ] if words[i][:2] in self.pre_sufix else ENC_PAD))
        features.append((7, self.pre_sufix[words[i][:3] ] if words[i][:3] in self.pre_sufix else ENC_PAD))
        features.append((8, self.pre_sufix[words[i][:4] ] if words[i][:4] in self.pre_sufix else ENC_PAD))
        features.append((9, self.pre_sufix[words[i][-1:]] if words[i][-1:] in self.pre_sufix else ENC_PAD))
        features.append((10, self.pre_sufix[words[i][-2:]] if words[i][-2:] in self.pre_sufix else ENC_PAD))
        features.append((11, self.pre_sufix[words[i][-3:]] if words[i][-3:] in self.pre_sufix else ENC_PAD))
        features.append((12, self.pre_sufix[words[i][-4:]] if words[i][-4:] in self.pre_sufix else ENC_PAD))
        #Most frequent tag for next word        
        features.append((13, next_tag))
        features.append((14, 1 if  bool(re.search(r'\w*-\w*', words[i])) else ENC_PAD))
        features.append((15, 1 if bool(re.search(r'\d', words[i])) else ENC_PAD))
        return features

    def predict(self, words, tags):
        pred_tags = []
        for i in range(len(words)):
            features = self.featurize(words, i, pred_tags, tags[i+1] if i + 1 < len(tags) else PAD)
            output_vector = self.model.forward(features)
            tag = max(output_vector, key=output_vector.get)
            pred_tags.append(tag)
        return pred_tags
