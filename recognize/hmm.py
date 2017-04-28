# encoding=utf-8
from config import data_path

from algorithm.hmm import HMModel
from segment import cut

import pickle
import json

STATES = {
    'A': 'adj',   # adjective
    'B': 'modifier',   # other noun-modifier
    'C': 'conj',   # conjunction
    'D': 'adv',   # adverb
    'E': 'exclam',   # exclamation
    'G': 'morpheme',   # morpheme
    'H': 'prefix',   # prefix
    'I': 'idiom',   # idiom
    'J': 'abbr',   # abbreviation
    'K': 'suffix',   # suffix
    'M': 'num',   # number
    'N': 'noun',   # general noun
    'ND': 'direction',  # direction noun
    'NH': 'person',  # person name
    'NI': 'org',  # organization name
    'NL': 'position',  # location noun
    'NS': 'location',  # geographical name
    'NT': 'time',  # temporal noun
    'NZ': 'noun',  # other proper noun
    'O': 'onoma',   # onomatopoeia
    'P': 'prep',   # preposition
    'Q': 'quantity',   # quantity
    'R': 'pronoun',   # pronoun
    'U': 'auxiliary',   # auxiliary
    'V': 'verb',   # verb
    'W': 'punctuation',   # punctuation
    'WS': 'foreign',  # foreign words
    'X': 'other',   # non-lexeme
}


class HMMTagger(HMModel):
    def __init__(self, *args, **kwargs):
        super(HMMTagger, self).__init__(*args, **kwargs)
        self.states = STATES.keys()
        self.data = None

    def load_data(self, filename):
        self.data = open(data_path(filename), 'r', encoding="utf-8")

    def train(self):
        if not self.inited:
            self.setup()

        # train
        for line in self.data:
            # pre processing
            line = line.strip()
            if not line:
                continue

            # get observes and states
            observes = []
            states = []
            items = line.split(' ')
            for item in items:
                tmp = item.split('/')
                if len(tmp) > 1:
                    state = tmp[1].upper()
                    if state not in self.states:
                        continue
                    observes.append(tmp[0])
                    states.append(state)

            # special method for this dataset
            observes[0], observes[-1] = observes[-1], observes[0]
            states[0], states[-1] = states[-1], states[0]

            # resume train
            self.do_train(observes, states)

        # special method for this dataset
        avg = float(sum(self.init_vec.values())) / len(self.init_vec)
        for key in self.init_vec:
            if self.init_vec[key] == 0:
                self.init_vec[key] = avg

    def tag(self, words):
        try:
            tags = self.do_predict(words)
            return list(map(lambda key: STATES[key], tags))
        except:
            return list(map(lambda key: STATES['X'], tags))


