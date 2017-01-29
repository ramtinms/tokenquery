#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import textwrap
import json

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

from tokenquery.models.token import Token

################################
#### Google API functions   ####
################################

def call_google_nlp(text):
    """Use the NL API to analyze the given text string, and returns the
    response from the API.  Requests an encodingType that matches
    the encoding used natively by Python.  Raises an
    errors.HTTPError if there is a connection problem.
    """

    # TODO check cred exists ....

    # check GOOGLE_APPLICATION_CREDENTIALS
    credentials = GoogleCredentials.get_application_default()
    scoped_credentials = credentials.create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    scoped_credentials.authorize(http)
    service = discovery.build(
        'language', 'v1beta1', http=http)
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text
        },
        'features': {
            # 'extract_syntax': True,
            'extractEntities': True
        },
        'encodingType': get_native_encoding_type(),
    }
    request = service.documents().annotateText(body=body)
    return request.execute()

def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def get_tokens(text):
    final_tokens = []
    tokens = call_google_nlp(text).get()
    for token in tokens:
        # begin = tokens[head_index]['text']['beginOffset']
        # end = begin + len(tokens[head_index]['text']['content'])

        print (token)
        # Token()

    return final_tokens

################################
#### Dep-parsing Helpers    ####
################################

def dependents(tokens, head_index):
    """Returns an ordered list of the token indices of the dependents for
    the given head."""
    # Create head->dependency index.
    head_to_deps = {}
    for i, token in enumerate(tokens):
        head = token['dependencyEdge']['headTokenIndex']
        if i != head:
            head_to_deps.setdefault(head, []).append(i)
    return head_to_deps.get(head_index, ())

def phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    begin, end = phrase_extent_for_head(tokens, head_index)
    return text[begin:end]


def all_phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    results = []
    for (begin, end) in all_phrases_for_head(tokens, head_index):
        results.append(text[begin:end])
    return results


def phrase_extent_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    begin = tokens[head_index]['text']['beginOffset']
    end = begin + len(tokens[head_index]['text']['content'])
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        begin = min(begin, child_begin)
        end = max(end, child_end)
    return (begin, end)


def all_phrases_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    results = []
    begin = tokens[head_index]['text']['beginOffset']
    end = begin + len(tokens[head_index]['text']['content'])
    head_begin = begin
    head_end = end

    results.append((begin, end))
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        results.append((min(head_begin, child_begin), max(head_end, child_end)))
        begin = min(begin, child_begin)
        end = max(end, child_end)
        # TODO two combination
    # return (begin, end)
    return results


if __name__ == "__main__":
    get_tokens("I love to travel.")
