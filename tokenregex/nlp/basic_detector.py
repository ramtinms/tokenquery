#!/usr/bin/env python
# -*- coding: utf-8 -*-


# def is_number(s):
#     try:
#         float(s) if '.' in s else int(s)
#         return True
#     except ValueError:
#         return False



# # basic operations like
# URL detection 
# Hashtag detection 
# Emoji dete


import re

class EmailDetector():

    def __init__(self):
        self.email_regex = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})'

    def detect(self, text):

        # email address vs email
        'label' 'schema:email'

        # TODO
        # span, content

class URLDetector():

    def __init__(self):
        self.url_regex = r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

    def detect(self, text):
        # TODO



class DateDetector():

    def __init__(self):
        self.email_regex = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})'

    def detect(self, text):

        # span, content


class GenderDetector():

    def __init__(self):
        self.email_regex = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})'

    def detect(self, text):

        # span, content

        # if a person gender of that person


class ColorDetector():

    def __init__(self):
        # codes
        self.color_code_regex = r'([0-9a-f]{6}|[0-9a-f]{3})'

    def detect(self, text):

        # schema:color

        # span, content

        # if a person gender of that person


    # query kg
    # 



if __name__ == '__main__':
    main()
    #test()
