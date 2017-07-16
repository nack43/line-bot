# -*- coding: utf-8 -*-
import hug
from langdetect import detect_langs
import nltk
import MeCab


def strip_stop_words(tokens):
    # english and japanese stop words are requires
    # 英語でも日本語でもいらない言葉を消す
    stop_words = ['i', 'you', 'blog',
                  'article',
                  u'私', u'俺', u'記事',
                  u'ブロク']

    return filter(lambda x: x.lower() not in stop_words, tokens)

def tokenize_english(text):
    # we only want nouns, so we tokenize and strip out everything else
    # 名詞だけが必要だから他の言葉を消そう
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
            nouns.append(node.surface)
        node = node.next
    print(nouns)
    return nouns

def find_articles(text, lang):
    # find the words we want to search with, and then search
    # 興味がある言葉を見つけて、検索する
    if lang == 'en':
        tokens = tokenize_english(text)
    else:
        print('LEYS TOKENIZE JAPANESE!')
        tokens = tokenize_japanese(text)

    # now scrape google
    # これからグーグルで検索しろう


# sample data from line
# ラインから送信されるデータフォーマットの例
"""
{
  "events": [
      {
        "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
        "type": "message",
        "timestamp": 1462629479859,
        "source": {
             "type": "user",
             "userId": "U206d25c2ea6bd87c17655609a1c37cb8"
         },
         "message": {
             "id": "325708",
             "type": "text",
             "text": "Hello, world"
          }
      }
  ]
}
"""

@hug.post('/blogsearch/1.0')
def blog_search_post_endpoint_10(data, response=None):
    print data

def main():
    # get user input ユーザーの入力を受け付ける
    user_input = str(input(">>>"))
    print("lets find a blog!")

    # get the language 言語を判定する
    lang = detect_langs(user_input)[0].lang
    print(user_input)
    if lang in ['en', 'ja']:
        # find articles 記事を見つけよう！
        find_articles(user_input, lang)
    else:
        print('not supported :(')

if __name__ == '__main__':
    main()
