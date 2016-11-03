from nlp.tokenizer import Tokenizer
from nlp.pos_tagger import POSTagger
from tokenregex import TokenRegex
import unittest

class TestTokenRegex(unittest.TestCase):

    def test_regex_match(self):
        test_case_2 = '[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] [/artist|painter/]'
        test_case_3 = '([ner:"NUMBER"]+) [/km|kilometers?/]'
        test_case_4 = '[ner:"PERSON"]? [pos:/V.*/]'
        test_case_5 = '[ner:"PERSON"]{2} [pos:/V.*/]'

    def test_capturing(self):

        test_case_0 = '[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] ["painter"]'

        test_case_1 = '([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] ["painter"]'

        test_case_2 = '([ner:"PERSON"]+ [pos:"VBZ"]) [/an?/] ["painter"]'

        test_case_3 = '([ner:"PERSON"]+ [pos:"VBZ"] )[/an?/] ["painter"]'

        test_case_4 = '[ner:"PERSON"]+ ([pos:"VBZ"] [/an?/] ["painter"])'

    def test_by_pos_tag(self):
        tokenizer = Tokenizer('PTBTokenizer')
        pos_tagger = POSTagger()
        test_text = """
                    I am a painter, you're also a painter!
                    """

        tokens = tokenizer.tokenize(test_text)
        tokens = pos_tagger.tag(tokens)

        test_tokenregex_1 = '[/.*/] [pos:"VBP"] [/an?/] ["painter"]'
        unit = TokenRegex(test_tokenregex_1)
        unit.machine.print_state_machine()

        print unit.match_tokens(tokens)

        test_tokenregex_2 = '([/.*/]) [pos:"VBP"] [/an?/] ["painter"]'
        unit = TokenRegex(test_tokenregex_1)
        unit.machine.print_state_machine()

        print unit.match_tokens(tokens)


        # self.assertListEqual(expected_tags, [token.get_a_label('POS') for token in tokens])


if __name__ == "__main__":
    unittest.main()

