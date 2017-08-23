import unittest
from nlp import strip_stop_words, tokenize_english, tokenize_japanese, natural_response

#class TestStripStopWords(unittest.TestCase):


#class TestTokenizeEnglish(unittest.TestCase):


#class TestTokenizeJapanese(unittest.TestCase):


class TestNaturalResponse(unittest.TestCase):
    def test_nolang(self):
        actual = natural_response('nolang', 'cn', 'http://test.com')
        self.assertEqual(actual, 'sorry, I don\'t speak that language yet\n')

    def test_notfound_english(self):
        actual = natural_response('notfound', 'en', 'http://test.com')
        self.assertEqual(actual, 'I couldn\'t find any articles')

    def test_notfound_japanese(self):
        actual = natural_response('notfound', 'ja', 'http://test.com')
        self.assertEqual(actual, '記事を見つけられなかった')

    def test_found_english(self):
        actual = natural_response('found', 'en', 'http://test.com')
        self.assertEqual(actual, 'Check this out http://test.com')

    def test_found_japanese(self):
        actual = natural_response('found', 'ja', 'http://test.com')
        self.assertEqual(actual, 'どうぞ！http://test.com')
  

