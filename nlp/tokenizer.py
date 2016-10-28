
from nltk.tokenize import word_tokenize
from models.token import Token

class Tokenizer:
    """
        TODOs : start and end span problem
    """

    def tokenize(self, string):
        tokens = []

        for token_text in word_tokenize(string):
            new_token = Token(token_text, 0, 0)
            tokens.append(new_token)

        return tokens
