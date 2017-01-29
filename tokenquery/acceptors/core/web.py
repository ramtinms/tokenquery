# -*- coding: utf-8 -*-
from tokenquery.acceptors.core.string import str_reg


def web_is_url(token_input):
    url_regex = r'^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$'
    return str_reg(token_input, url_regex)


def web_is_email(token_input):
    email_regex = r"(^[mailto:]?[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return str_reg(token_input, email_regex)


def web_is_hex_code(token_input):
    hex_regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return str_reg(token_input, hex_regex)


def web_is_hashtag(token_input):
    if token_input[0] == "#" and ' ' not in token_input:
        return True
    else:
        return False


def web_is_emoji(token_input, operation_input):
    unicode_regex = r"(<U\\+\\w+?>)"
    if str_reg(token_input, unicode_regex):
        return True
    else:
        emojicons = r'(^|\s)(:D|:\/)(?=\s|[^[:alnum:]+-]|$)'
        return str_reg(token_input, emojicons)
    return False
