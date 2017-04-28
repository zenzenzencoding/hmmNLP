from .extra import abstract_stop_words
from .tf_idf import TF_IDF

from segment import data_path as seg_data_path
from segment import cut

idf_abstracter = TF_IDF()
idf_abstracter.stop_words = abstract_stop_words
idf_abstracter.load(filename=seg_data_path("words.txt"))
idf_abstracter.build_word_count()


def get_abstract(txt):
    tmp = ""
    for c in txt:
        if c in abstract_stop_words:
            continue
        tmp += c
    words = cut(tmp)
    return idf_abstracter.get_key_words(words)

