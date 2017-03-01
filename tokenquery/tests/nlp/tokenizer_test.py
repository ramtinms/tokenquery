import unittest
from tokenquery.nlp.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def test_ptb_wrapper(self):
        unit = Tokenizer('PTBTokenizer')
        test_text = """
                    this cannot be true; I'm sure it was 2.8$, not $ 4 to buy @this #umbrella. this <sentence>
                     mentioned while shoping! Then he said: "you are responsible for this issue (extra price for fast-food and diet_coke) and \n I am
                    not [happy] about it". Writer: xyz -- nyt
                    """

        expected_tokens = ['this','can','not','be','true',';','I','\'m',
                      'sure','it','was','2.8','$',',','not','$',
                      '4','to','buy','@','this','#','umbrella',
                      '.','this','<','sentence','>','mentioned',
                      'while','shoping','!','Then','he','said',':',
                      '``','you','are','responsible','for','this','issue',
                      '(','extra','price','for','fast-food','and',
                      'diet_coke',')','and','I','am','not','[','happy',
                      ']','about','it',"''",'.','Writer',':','xyz','--','nyt']
        tokens = unit.tokenize(test_text)
        self.assertListEqual(expected_tokens, [token.get_text() for token in tokens])

    def test_ptb_utf8(self):
        unit = Tokenizer('PTBTokenizer')
        test_text = u"""
                    «ταБЬℓσ»: 1<2 & 4+1>3, now 40% off!
                    """
        expected_tokens = [u'«ταБЬℓσ»',u':',u'1',u'<',u'2',u'&',u'4+1',
                           u'>',u'3',u',',u'now',u'40',u'%',u'off',u'!']
        tokens = unit.tokenize(test_text)
        self.assertListEqual(expected_tokens, [token.get_text() for token in tokens])

    def test_space_tokenizer(self):
        unit = Tokenizer('SpaceTokenizer')
        test_text = """
                    this cannot be true; I'm sure it was 2.8$, not $ 4 to buy @this #umbrella. this <sentence>
                     mentioned while shoping! Then he said: "you are responsible for this issue (extra price for fast-food and diet_coke) and \n I am
                    not [happy] about it". Writer: xyz -- nyt
                    """
        expected_tokens = ['this','cannot','be','true',';','I',"'m",
                      'sure','it','was','2','.8$,','not','$','4',
                      'to','buy','@this','#umbrella.','this',
                      '<sentence>','mentioned','while','shoping',
                      '!','Then','he','said',':','"you','are','responsible',
                      'for','this','issue','(extra','price','for',
                       'fast','-food','and','diet_coke',')',
                       'and','I','am','not','[happy]','about',
                       'it','".','Writer',':','xyz','--','nyt']


        tokens = unit.tokenize(test_text)
        self.assertListEqual(expected_tokens, [token.get_text() for token in tokens])

    def test_nltk_white_space_tokenizer(self):
        unit = Tokenizer('NLTKWhiteSpaceTokenizer')
        test_text = """
                    this cannot be true; I'm sure it was 2.8$, not $ 4 to buy @this #umbrella. this <sentence>
                     mentioned while shoping! Then he said: "you are responsible for this issue (extra price for fast-food and diet_coke) and \n I am
                    not [happy] about it". Writer: xyz -- nyt
                    """
        expected_tokens = ['this','cannot','be','true;',"I'm",'sure','it',
                      'was','2.8$,','not','$','4','to','buy','@this',
                      '#umbrella.','this','<sentence>','mentioned',
                      'while','shoping!','Then','he','said:','"you',
                      'are','responsible','for','this','issue',
                      '(extra','price','for','fast-food','and','diet_coke)',
                      'and','I','am','not','[happy]','about','it".',
                      'Writer:','xyz','--','nyt']


        tokens = unit.tokenize(test_text)
        self.assertListEqual(expected_tokens, [token.get_text() for token in tokens])

if __name__ == "__main__":
    unittest.main()
