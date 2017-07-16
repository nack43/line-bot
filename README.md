# line-bot


to start up server:

```
hug -f get_article.py -p 1234
```


send data packet

```
curl -H "Content-Type: application/json" -X POST -d '{"events": [{"replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA","type": "message","timestamp": 1462629479859,"source": {"type": "user","userId": "U206d25c2ea6bd87c17655609a1c37cb8"},"message": {"id": "325708","type": "text","text": "Hello, world"}}]}' http://localhost:1234/blogsearch/1.0
```
