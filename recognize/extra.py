import os


def data_path(filename):
    return os.path.join(os.path.dirname(__file__), "%s" % filename)


def build(filename):
    fr = open(filename, 'r', encoding='utf-8')

    word_set = set()

    for line in fr:
        line = line.strip()
        word_set.add(line)
    return word_set

DEFAULT = {
    '我': 'pronoun',
    '我们': 'pronoun',
    '你': 'pronoun',
    '你们': 'pronoun',
    '给': 'verb',
    '春节': 'noun',
    '玩': 'verb',
    '玩耍': 'verb',
    '只是': 'adv',
    '忠诚': 'noun',
    '可能': 'adv',
    '国庆节': 'noun',
    '比起': 'conj'
}

PUNCT = {
    "，",
    "。",
    "“",
    "”",
    "？",
    "！",
    "：",
    "《",
    "》",
    "、",
    "；",
    "·",
    "‘ ",
    "’",
    "──",
    ",",
    ".",
    "?",
    "!",
    "`",
    "~",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "+",
    "=",
    "[",
    "]",
    "{",
    "}",
    '"',
    "'",
    "<",
    ">",
    "\\",
    "|"
}

PHRASE = build(data_path("phrase.txt"))

LOCATION = build(data_path("location.txt"))