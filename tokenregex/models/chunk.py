import re


class Chunk:
    """ Any sequence of tokens that shares a label,
        this can be used to stote sentences, entities
        and ...
    """

    def __init__(self, chunk_id, tokens):
        self.chunk_id = chunk_id
        self.tokens = tokens

    def add_a_label(self, label_name, label_value):
        for counter, token in enumerate(self.tokens):
            if counter == 0:
                token.add_a_label(label_name+'~B', label_value)
            else:
                token.add_a_label(label_name+'~I', label_value)

    def get_a_label(self, label_name):
        return self.tokens[0].get_a_label(label_name)

    def get_text(self):
        if not self.tokens:
            return None
        return " ".join([token.get_text() for token in self.tokens])