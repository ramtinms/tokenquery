def int_value(token_input, operation_input):
    # parsing operation_input

    cond_type = ""
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

    try:
        text_value = int(token_input)
        if cond_type == "=" or cond_type == "==":
            return text_value == cond_value
        elif cond_type == "<":
            return text_value < cond_value
        elif cond_type == ">":
            return text_value > cond_value
        elif cond_type == ">=":
            return text_value >= cond_value
        elif cond_type == "<=":
            return text_value <= cond_value
        elif cond_type == "!=" or cond_type == "<>":
            return text_value != cond_value
        else:
            return False
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_e(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value == op_value
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_g(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value > op_value
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_l(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value < op_value
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_ne(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value != op_value
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_le(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value <= op_value
    except ValueError:
        # TODO raise tokenregex error
        return False


def int_ge(token_input, operation_input):
    try:
        text_value = int(token_input)
        op_value = int(operation_input)
        return text_value >= op_value
    except ValueError:
        # TODO raise tokenregex error
        return False

# TODO
# add M , K , ...
# add float
