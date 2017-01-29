
from nltk.tokenize import word_tokenize
from tokenquery.models.token import Token
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.tokenize import WhitespaceTokenizer


class Tokenizer:
    """
        Tokenizer will break text into a list of Token objects.
        Currently it supports SpaceTokenizer, NLTKWhiteSpaceTokenizer,
        and PTBTokenizer (default) using NLTK lib. Since NLTK PTBTokenizer
        does not provide spans for tokens, we have a wrapper
        over PTB tokenizer to capture start and end of the tokens
        but is currently in beta mode. please report any potential
        problems.

        :param tokenizer_type: type of tokenizer one of 'SpaceTokenizer',
                               'NLTKWhiteSpaceTokenizer', 'PTBTokenizer'
        :type tokenizer_type: str
    """
    def __init__(self, tokenizer_type="PTBTokenizer"):

        # Sanity checks
        if tokenizer_type in ['SpaceTokenizer', 'NLTKWhiteSpaceTokenizer', 'PTBTokenizer']:
            self.tokenizer_type = tokenizer_type
        else:
            print ("Unrecognized tokenizer type : setting back to default (PTBTokenizer)")
            self.tokenizer_type = "PTBTokenizer"

    def tokenize(self, text):
        """
           tokenize text into a list of Token objects

            :param text: text to be tokenized (might contains several sentences)
            :type text: str
            :return: List of Token objects
            :rtype: list(Token)
        """
        tokens = []

        if self.tokenizer_type == "SpaceTokenizer":
            operator = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
            for counter, span in enumerate(operator.span_tokenize(text)):
                new_token = Token(counter, text[span[0]:span[1]], span[0], span[1])
                tokens.append(new_token)

        elif self.tokenizer_type == "NLTKWhiteSpaceTokenizer":
            operator = WhitespaceTokenizer()
            for counter, span in enumerate(operator.span_tokenize(text)):
                new_token = Token(counter, text[span[0]:span[1]], span[0], span[1])
                tokens.append(new_token)

        elif self.tokenizer_type == "PTBTokenizer":
            ptb_tokens = word_tokenize(text)
            counter = 0
            for token, span in self._penn_treebank_tokens_with_spans(text, ptb_tokens):
                new_token = Token(counter, token, span[0], span[1])
                counter += 1
                tokens.append(new_token)

        return tokens

    def _penn_treebank_tokens_with_spans(self, text, tokens):
        text_from_tokens = ""

        for token in tokens:
            norm_token = token.replace('``', '"') \
                              .replace("''", '"') \
                              .replace('-LRB-', '(') \
                              .replace('-RRB-', ')') \
                              .replace('-LSB-', '[') \
                              .replace('-RSB-', ']') \
                              .replace('-LCB-', '{') \
                              .replace('-RCB-', '}')

            text_from_tokens += " " + norm_token
        text_from_tokens = text_from_tokens.strip().lstrip()
        spans = []
        start_of_span = 0
        t_index = 0
        for t_f_t_index, t_char in enumerate(text_from_tokens):
            # assumption we dont have two space in a row for normalized text
            if t_char == " ":
                spans.append((start_of_span, t_index))
                start_of_span = t_index
                continue
            if text[t_index].isspace():
                while (text[t_index].isspace() and t_index < len(text)):
                    t_index += 1
                    start_of_span = t_index
            if text[t_index] != t_char:
                raise Exception("something went wrong while finding spans for PTB tokens {} does not match {}".format(text[t_index], t_char))
            else:
                t_index += 1

        spans.append((start_of_span, t_index))

        assert len(spans) == len(tokens)

        return zip(tokens, spans)
