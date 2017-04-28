from recognize.extra import DEFAULT, PUNCT, PHRASE, LOCATION


def filter_punct(word, tag):
    if word in PUNCT:
        return 'punctuation'
    elif tag == 'punctuation':
        if word in DEFAULT:
            return DEFAULT[word]
        else:
            return 'noun'
    return tag


def filter_location(word, tag):
    if word in LOCATION:
        return 'location'
    return tag


def filter_phrase(word, tag):
    if word in PHRASE:
        return 'phrase'
    return tag


def filter_default(word, tag):
    if tag in {'other', 'exclam'}:
        if word in DEFAULT:
            return DEFAULT[word]
    return tag


FILTERS = [filter_punct, filter_location, filter_phrase, filter_default]


def main_filter(words, tags, filters=FILTERS):
    if len(words) != len(tags):
        return tags
    for i in range(len(words)):
        word = words[i]
        tag = tags[i]
        for the_filter in filters:
            tag = the_filter(word, tag)
        tags[i] = tag
    return tags

