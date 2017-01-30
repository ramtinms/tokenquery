import unittest
from tokenquery.nlp.importer import Importer


class TestImporter(unittest.TestCase):

    def test_load_conllu(self):
        tokens = Importer.load_from_conll_u_file('tokenquery/tests/nlp/data/test.conllu')
        expected_tokens = ['The', 'quick', 'brown', 'fox', 'jumps',
                           'over', 'the', 'lazy', 'dog', '.',
                           'The', 'quick', 'brown', 'fox', 'jumps',
                           'over', 'the', 'lazy', 'dog', '.']
        self.assertListEqual(expected_tokens, [token.get_text() for token in tokens])

if __name__ == "__main__":
    unittest.main()
