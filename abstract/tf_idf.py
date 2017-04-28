from algorithm.word_dict import WordDictModel
import math
from .extra import abstract_stop_words as stop_words


class TF_IDF(WordDictModel):
    def __init__(self):
        super(TF_IDF, self).__init__()
        self.word_count = 0

    def build_word_count(self):
        self.word_count = sum(map(lambda x: self.word_dict[x], self.word_dict))

    def build_local_dict(self, words):
        local_dict = {}
        for word in words:
            if word in self.stop_words:
                continue
            if local_dict.get(word):
                local_dict[word] += 1
            else:
                local_dict[word] = 1
        return local_dict

    def get_tf_idf(self, words):
        local_dict = self.build_local_dict(words)
        term_dict = {}
        for word in words:
            if (word in term_dict) or (word in stop_words):
                continue
            tf = local_dict.get(word, 0)
            idf = math.log(self.word_count / self.word_dict.get(word, 1))
            term_dict[word] = tf * idf
        return term_dict

    def get_key_words(self, words):
        term_dict = self.get_tf_idf(words)
        return sorted(term_dict, key=lambda x: term_dict[x], reverse=True)[:6]

