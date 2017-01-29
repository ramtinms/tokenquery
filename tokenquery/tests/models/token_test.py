import unittest
from tokenquery.models.token import Token


class TestTokenClass(unittest.TestCase):

    def test_token(self):
        test_token = Token(1, 'test_string', 12, 16)
        self.assertEqual(test_token.get_token_id(), 1)
        self.assertEqual(test_token.get_span(), (12, 16))
        self.assertEqual(test_token.get_text(), 'test_string')

        test_token.add_a_label('test_label', 'test_label_value')
        self.assertEqual(test_token.get_a_label('test_label'), 'test_label_value')

        test_token.set_token_id('h1')
        self.assertEqual(test_token.get_token_id(), 'h1')

        test_token.set_text('test_string2')
        self.assertEqual(test_token.get_text(), 'test_string2')

        test_token.set_span(13, 17)
        self.assertEqual(test_token.get_span(), (13, 17))


if __name__ == '__main__':
    unittest.main()
