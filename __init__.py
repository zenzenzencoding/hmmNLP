import sys
import os

sys.path.append(os.path.dirname(__file__))
del(sys)
del(os)

from segment import cut, dict_cut, hmm_cut
from.recognize import tag
