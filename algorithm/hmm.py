# encoding=utf-8
import pickle
import json

EPS = 0.0001


class HMModel:
    def __init__(self):
        self.trans_mat = {}  # trans_mat[status][status] = int
        self.emit_mat = {}  # emit_mat[status][observe] = int
        self.init_vec = {}  # init_vec[status] = int
        self.state_count = {}  # state_count[status] = int
        self.states = {}
        self.inited = False

    def setup(self):
        for state in self.states:
            # build trans_mat
            self.trans_mat[state] = {}
            for target in self.states:
                self.trans_mat[state][target] = 0.0
            # build emit_mat
            self.emit_mat[state] = {}
            # build init_vec
            self.init_vec[state] = 0
            # build state_count
            self.state_count[state] = 0
        self.inited = True

    def save(self, filename="hmm.json", code='json'):
        fw = open(filename, 'w', encoding='utf-8')
        data = {
            "trans_mat": self.trans_mat,
            "emit_mat": self.emit_mat,
            "init_vec": self.init_vec,
            "state_count": self.state_count
        }
        if code == "json":
            txt = json.dumps(data)
            txt = txt.encode('utf-8').decode('unicode-escape')
            fw.write(txt)
        elif code == "pickle":
            pickle.dump(data, fw)
        fw.close()

    def load(self, filename="hmm.json", code="json"):
        fr = open(filename, 'r', encoding='utf-8')
        if code == "json":
            txt = fr.read()
            model = json.loads(txt)
        elif code == "pickle":
            model = pickle.load(fr)
        self.trans_mat = model["trans_mat"]
        self.emit_mat = model["emit_mat"]
        self.init_vec = model["init_vec"]
        self.state_count = model["state_count"]
        self.inited = True
        fr.close()

    def do_train(self, observes, states):
        if not self.inited:
            self.setup()

        for i in range(len(states)):
            if i == 0:
                self.init_vec[states[0]] += 1
                self.state_count[states[0]] += 1
            else:
                self.trans_mat[states[i - 1]][states[i]] += 1
                self.state_count[states[i]] += 1
                if observes[i] not in self.emit_mat[states[i]]:
                    self.emit_mat[states[i]][observes[i]] = 1
                else:
                    self.emit_mat[states[i]][observes[i]] += 1

    def get_prob(self):
        init_vec = {}
        trans_mat = {}
        emit_mat = {}
        default = max(self.state_count.values())  # avoid ZeroDivisionError
        # convert init_vec to prob
        for key in self.init_vec:
            if self.state_count[key] != 0:
                init_vec[key] = float(self.init_vec[key]) / self.state_count[key]
            else:
                init_vec[key] = float(self.init_vec[key]) / default
        # convert trans_mat to prob
        for key1 in self.trans_mat:
            trans_mat[key1] = {}
            for key2 in self.trans_mat[key1]:
                if self.state_count[key1] != 0:
                    trans_mat[key1][key2] = float(self.trans_mat[key1][key2]) / self.state_count[key1]
                else:
                    trans_mat[key1][key2] = float(self.trans_mat[key1][key2]) / default
        # convert emit_mat to prob
        for key1 in self.emit_mat:
            emit_mat[key1] = {}
            for key2 in self.emit_mat[key1]:
                if self.state_count[key1] != 0:
                    emit_mat[key1][key2] = float(self.emit_mat[key1][key2]) / self.state_count[key1]
                else:
                    emit_mat[key1][key2] = float(self.emit_mat[key1][key2]) / default
        return init_vec, trans_mat, emit_mat

    def do_predict(self, sequence):
        tab = [{}]
        path = {}
        init_vec, trans_mat, emit_mat = self.get_prob()

        # init
        for state in self.states:
            tab[0][state] = init_vec[state] * emit_mat[state].get(sequence[0], EPS)
            path[state] = [state]

        # build dynamic search table
        for t in range(1, len(sequence)):
            tab.append({})
            new_path = {}
            for state1 in self.states:
                items = []
                for state2 in self.states:
                    if tab[t - 1][state2] == 0:
                        continue
                    prob = tab[t - 1][state2] * trans_mat[state2].get(state1, EPS) * emit_mat[state1].get(sequence[t], EPS)
                    items.append((prob, state2))
                best = max(items)  # best: (prob, state)
                tab[t][state1] = best[0]
                new_path[state1] = path[best[1]] + [state1]
            path = new_path

        # search best path
        prob, state = max([(tab[len(sequence) - 1][state], state) for state in self.states])
        return path[state]
