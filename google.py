from googleapiclient.discovery import build
import nlp
import os

def find_article(text, lang):
    # find the words we want to search with, and then search
    if lang == 'en':
        tokens = nlp.tokenize_english(text)
    else:
        tokens = nlp.tokenize_japanese(text)

    # google search
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

