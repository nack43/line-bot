# -*- coding: utf-8 -*-
import hug
from langdetect import detect_langs
import nltk
import MeCab
from falcon import (
    HTTP_400,
)
import os
from googleapiclient.discovery import build

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

def find_article(text, lang):
    # find the words we want to search with, and then search
    # 興味がある言葉を見つけて、検索する
    if lang == 'en':
        tokens = tokenize_english(text)
    else:
        print('LEYS TOKENIZE JAPANESE!')
        tokens = tokenize_japanese(text)

    # now scrape google
    # これからグーグルで検索しよう
    search_words = ' '.join(tokens)
    service = build('customsearch', 'v1', developerKey=os.environ['GOOGLE_API_KEY'])
    # search via google custom search api
    res = service.cse().list(q = search_words, cx = os.environ['SEARCH_ENGINE_ID'],).execute()
    # extract an article url
    for item in res['items']:
        article_url = item['link']
        break
    print(article_url)
    return article_url

def get_message(body):
    # parse send message out of JSON
    # JSONから送ったことを取る
    if 'events' in body:
        if 'message' in body['events'][0]:
            if 'text' in body['events'][0]['message']:
                return body['events'][0]['message']['text']

def natural_response(response, lang, article):
    # turn the response into something more human
    # 自然（話し言葉）な返事を作る
    if response == 'nolang':
        return 'sorry, I don\'t speak that language yet\n' +\
               'ごめん、送ってくれたメッセージの言語がまだ分からない'
    elif response == 'notfound':
        if lang == 'en':
            return 'I couldn\'t find any articles'
        elif lang == 'ja':
            return '記事を見つけてなかった'
    elif response == 'found':
        if lang == 'en':
            return 'Check this out ' + article
        elif lang == 'ja':
            return 'どうぞ！' + article

@hug.post('/blogsearch/1.0')
def blog_search_post_endpoint_10(body, response = None):
    # handle API call
    # APIレクエストを処理する
    message = get_message(body)
    if message == None:
        response.status = HTTP_400
        # no message / 送ったことがない
        return 'NO MESSAGE'
    # get the language 言語を判定する
    lang = detect_langs(message)[0].lang
    if lang in ['en', 'ja']:
        # find articles 記事を見つけよう！
        article = find_article(message, lang)
    else:
        return natural_response('nolang', lang, '')

    # reply / 返事する
    if article != None:
        return natural_response('found', lang, article)
    else:
        return natural_response('notfound', lang, '')

if __name__ == '__main__':
    main()
