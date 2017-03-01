import nltk
from nltk import pos_tag


class POSTagger:
    """
        NLTK pos tagger
    """

    def __init__(self):
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

    def tag(self, tokens):
        """
            add pos tags to token objects

            :param tokens: list of token objects
            :type tokens: list(Token)
            :return: label augmented list of Token objects
            :rtype: list(Token)
        """
        tags = pos_tag([token.get_text() for token in tokens])
        for token, tag in zip(tokens, tags):
            token.add_a_label('pos', tag[1])
        return tokens
