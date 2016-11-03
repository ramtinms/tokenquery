import unittest
from nlp.tokenizer import Tokenizer
from nlp.pos_tagger import POSTagger


class TestPOSTagger(unittest.TestCase):

    def test_pos_tags(self):
        tokenizer = Tokenizer('PTBTokenizer')
        test_text = """
                    this cannot be true; I'm sure it was 2.8$, not $ 4 to buy @this #umbrella. this <sentence>
                     mentioned while shoping! Then he said: "you are responsible for this issue (extra price for fast-food and diet_coke) and \n I am
                    not [happy] about it". Writer: xyz -- nyt
                    """
        tokens = tokenizer.tokenize(test_text)
        unit = POSTagger()
        updated_tokens = unit.tag(tokens)
        expected_tags = ['DT','MD','RB','VB','JJ',':','PRP',
                           'VBP','JJ','PRP','VBD','CD','$',',',
                           'RB','$','CD','TO','VB','NNP','DT',
                           '#','NN','.','DT','JJ','NN','NN',
                           'VBD','IN','VBG','.','RB','PRP','VBD',
                           ':','``','PRP','VBP','JJ','IN','DT',
                           'NN','(','JJ','NN','IN','NN','CC','NN',
                           ')','CC','PRP','VBP','RB','NNP','JJ',
                           'NN','IN','PRP',"''",'.','NN',':','NN',
                           ':','NN']

        self.assertListEqual(expected_tags, [token.get_a_label('pos') for token in tokens])

if __name__ == "__main__":
    unittest.main()
