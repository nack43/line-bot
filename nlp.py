import nltk
import MeCab


def strip_stop_words(tokens):
    # english and japanese stop words are requires
    stop_words = ['i', 'you', 'blog', 'article',
                  u'私', u'俺', u'記事', u'ブログ']
    processed = list(filter(lambda x: x.lower() not in stop_words, tokens))
    return processed


def tokenize_english(text):
    # we only want nouns, so we tokenize and strip out everything else
    sent_text = nltk.sent_tokenize(text)
    nouns = []
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokenized_text)
        print(tagged)
        nouns += [w[0] for w in tagged if 'NN' in w[1] or 'JJ' in w[1]]
    return nouns

# return array of nouns
def tokenize_japanese(text):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    nouns = []
    while node:
        if node.feature.split(',')[0] == '名詞':
            nous.append(node.surface)
        node = node.next
    print(nouns)
    return nouns


def natural_response(response, lang, article):
    # turn the response into something more human
    if response == 'nolang':
        return 'sorry, I don\'t speak that language yet\n'
    elif response == 'notfound':
        if lang == 'en':
            return 'I couldn\'t find any articles'
        elif lang == 'ja':
            return '記事を見つけられなかった'
    elif response == 'found':
        if lang == 'en':
            return 'Check this out ' + article
        elif lang == 'ja':
            return 'どうぞ！' + article

