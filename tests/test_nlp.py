import unittest
from nlp import (
    strip_stop_words,
    tokenize_english,
    tokenize_japanese,
    natural_response
)

class TestStripStopWords(unittest.TestCase):

    def test_remove_english_stopwords(self):
        query = ['I',  'Blog', 'Article', 'You']

        result = strip_stop_words(query)

        self.assertNotEqual(None, result)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, []) # should also strip whitespace

    def test_strip_sample_english_sentence(self):
        query = ['I', 'blog', 'dogs']

        result = strip_stop_words(query)

        self.assertNotEqual(None, result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'dogs') # should also strip whitespace

    def test_strip_japanese_stopwords(self):
        query = [u'私', u'ブログ', u'記事', u'俺']

        result = strip_stop_words(query)

        self.assertNotEqual(None, result)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, []) # should also strip whitespace

    def test_strip_japanese_sentence(self):
        query = [u'私', u'犬', u'記事']

        result = strip_stop_words(query)

        self.assertNotEqual(None, result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, [u'犬']) # should also strip whitespace
        

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
  

