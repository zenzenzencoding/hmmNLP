from recognize.hmm import HMMTagger
from recognize.rules import main_filter
from segment import cut

import os


def data_path(filename):
    return os.path.join(os.path.dirname(__file__), "%s" % filename)


hmm_tagger = HMMTagger()

hmm_tagger.load(filename=data_path("tagger.hmm.json"))


def build_result(words, tags):
    result = []
    for i in range(len(words)):
        result.append([words[i], tags[i]])
    return result


def tag(sentence):
    words = cut(sentence)
    tags = hmm_tagger.tag(words)
    tags = main_filter(words, tags)
    return build_result(words, tags)



