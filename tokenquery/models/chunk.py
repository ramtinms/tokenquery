import re


class Chunk:
    """ Any sequence of tokens that shares a label,
        this can be used to stote sentences, entities
        and ...
    """

    def __init__(self, chunk_id, tokens):
        self.chunk_id = chunk_id
        self.tokens = tokens
        self.start_span, self.end_span, self.text = change_tokenlist_to_chunk(tokens)

    def change_tokenlist_to_chunk(self, token_list):
        if not token_list:
            return None
        start_span = token_list[0].span_start
        end_span = token_list[0].span_end
        string = token_list[0].get_text()

        if len(token_list) == 1:
            return (start_span, end_span, string)

        else:
            for token in token_list[1:]:
                end_span = token.span_end
                string += ' ' + token.get_text()

        return (start_span, end_span, string)

    def add_a_label(self, label_name, label_value):
        for counter, token in enumerate(self.tokens):
            if counter == 0:
                token.add_a_label(label_name+'~B', label_value)
            else:
                token.add_a_label(label_name+'~I', label_value)

    def get_a_label(self, label_name):
        # ???
        return self.tokens[0].get_a_label(label_name)

    def get_text(self):
        return self.text
