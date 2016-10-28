import re 

class Token:
    def __init__(self, token_text, span_start, span_end):
        self.token_text = token_text
        self.span_start = span_start
        self.span_end = span_end
        self.labels = {}

    def add_a_label(self, label_name, label_value):
        self.labels[label_name] = label_value

    def get_a_label(self, label_name):
        return self.labels.get(label_name, None)

    def get_text(self):
        return self.token_text

    def text_match_a_regex(self, regex):
        return re.match(regex, self.token_text)

    def text_is_equal(self, value):
        if self.token_text == value:
            return True
        return False

    def label_match_a_regex(self, label_key, regex):
        label_value = self.get_a_label(label_key)
        if not label_value:
            return False
        return re.match(regex, label_value)

    def label_is_equal(self, label_key, label_value):
        if self.get_a_label(label_key) == label_value:
            return True
        return False

    def is_a_number(self, cond_type, cond_value):
        # check if it is a number and condition is valid
        try:
            text_value = float(self.token_text)
            if cond_type == "==":
                return text_value == cond_value
            elif cond_type == "!=":
                return text_value != cond_value
            elif cond_type == ">=":
                return text_value >= cond_value
            elif cond_type == "<=":
                return text_value <= cond_value
            elif cond_type == "<":
                return text_value < cond_value
            elif cond_type == ">":
                return text_value > cond_value
            else:
                return False
        except ValueError:
            return False