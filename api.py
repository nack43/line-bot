import hug
from langdetect import detect_langs
from falcon import ( HTTP_400, )
import line
import google
import nlp

@hug.post('/blogsearch/1.0')
def blog_search_post_endpoint_10(body, response = None):
    # handle API call
    message = line.get_message(body)
    reply_token = line.get_reply_token(body)
    if message == None:
        response.__status = HTTP_400
        # no message
        return 'NO MESSAGE'
    # get the language
    lang = detect_langs(message)[0].lang
    if lang in ['en', 'ja']:
        # find articles
        print(lang)
        article = google.find_article(message, lang)
    else:
        if reply_token != None:
            line.send_response(reply_token, nlp.natural_response('nolang', lang, ''))
        return 

    # reply
    if article != None:
        if reply_token != None:
            line.send_response(reply_token, nlp.natural_response('found', lang, article))
    else:
        if reply_token != None:
            line.send_response(reply_token, nlp.natural_response('notfound', lang, ''))

