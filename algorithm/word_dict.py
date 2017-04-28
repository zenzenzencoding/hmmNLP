import json
import pickle


class WordDictModel:
    def __init__(self):
        self.word_dict = {}
        self.data = None
        self.stop_words = {}

    def load_data(self, filename):
        self.data = open(filename, "r", encoding="utf-8")

    def update(self):
        # build word_dict
        for line in self.data:
            words = line.split(" ")
            for word in words:
                if word in self.stop_words:
                    continue
                if self.word_dict.get(word):
                    self.word_dict[word] += 1
                else:
                    self.word_dict[word] = 1

    def save(self, filename="words.txt", code="txt"):
        fw = open(filename, 'w', encoding="utf-8")
        data = {
            "word_dict": self.word_dict
        }

        # encode and write
        if code == "json":
            txt = json.dumps(data)
            fw.write(txt)
        elif code == "pickle":
            pickle.dump(data, fw)
        if code == 'txt':
            for key in self.word_dict:
                tmp = "%s %d\n" % (key, self.word_dict[key])
                fw.write(tmp)
        fw.close()

    def load(self, filename="words.txt", code="txt"):
        fr = open(filename, 'r', encoding='utf-8')

        # load model
        model = {}
        if code == "json":
            model = json.loads(fr.read())
        elif code == "pickle":
            model = pickle.load(fr)
        elif code == 'txt':
            word_dict = {}
            for line in fr:
                tmp = line.split(" ")
                if len(tmp) < 2:
                    continue
                word_dict[tmp[0]] = int(tmp[1])
            model = {"word_dict": word_dict}
        fr.close()

        # update word dict
        word_dict = model["word_dict"]
        for key in word_dict:
            if self.word_dict.get(key):
                self.word_dict[key] += word_dict[key]
            else:
                self.word_dict[key] = word_dict[key]
