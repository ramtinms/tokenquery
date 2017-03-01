import re

# String operations


def str_eq(token_input, operation_input):
    if token_input == operation_input:
        return True
    return False


def str_reg(token_input, operation_input):
    if not token_input:
        return False
    if re.match(operation_input, token_input):
        return True
    else:
        return False


def str_len(token_input, operation_input):
    # parsing operation_input
    cond_type = ''
    comp_part = operation_input.lstrip().strip()[:2]
    if comp_part in ['==', '>=', '<=', '!=', '<>']:
        cond_type = comp_part
        try:
            cond_value = int(operation_input.lstrip().strip()[2:])
        except ValueError:
            # TODO raise tokenregex error
            return False
    elif comp_part[0] in ['=', '>', '<']:
        cond_type = comp_part[0]
        try:
            cond_value = int(operation_input.lstrip().strip()[1:])
        except ValueError:
            # TODO raise tokenregex error
            return False
    else:
        return 'unknown operation'

    try:
        text_len = len(token_input)
        if cond_type == "==" or cond_type == "=":
            return text_len == cond_value
        elif cond_type == "<":
            return text_len < cond_value
        elif cond_type == ">":
            return text_len > cond_value
        elif cond_type == ">=":
            return text_len >= cond_value
        elif cond_type == "<=":
            return text_len <= cond_value
        elif cond_type == "!=" or cond_type == "<>":
            return text_len != cond_value
        else:
            return False
    except ValueError:
        # TODO raise tokenregex error
        return False

# TODO 
# def str_edit_dist(token_input, operation_input):
#     pass
# has acrylic letters
# is punctuation
# is stop word
# is a number  : 2 two II
