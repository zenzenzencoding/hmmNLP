# encoding=utf-8
from algorithm.word_dict import WordDictModel


class DAGSegger(WordDictModel):
    def build_dag(self, sentence):
        dag = {}
        for start in range(len(sentence)):
            unique = [start + 1]
            tmp = [(start + 1, 1)]
            for stop in range(start+1, len(sentence)+1):
                fragment = sentence[start:stop]
                # use tf_idf?
                num = self.word_dict.get(fragment, 0)
                if num > 0 and (stop not in unique):
                    tmp.append((stop, num))
                    unique.append(stop)
            dag[start] = tmp
        return dag

    def predict(self, sentence):
        Len = len(sentence)
        route = [0] * Len
        dag = self.build_dag(sentence)  # {i: (stop, num)}

        for i in range(0, Len):
            route[i] = max(dag[i], key=lambda x: x[1])[0]
        return route

    def cut(self, sentence):
        route = self.predict(sentence)
        next = 0
        word_list = []
        i = 0
        while i < len(sentence):
            next = route[i]
            word_list.append(sentence[i:next])
            i = next
        return word_list

    def test(self):
        cases = [
            "我来到北京清华大学",
            "长春市长春节讲话",
            "我们去野生动物园玩",
            "我只是做了一些微小的工作",
            "国庆节我在研究中文分词"
        ]
        for case in cases:
            result = self.cut(case)
            for word in result:
                print(word)
            print('')


