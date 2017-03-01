from tokenquery.models.fsa import StateMachine
from tokenquery.models.fsa import State
from tokenquery.models.stack import Stack
from tokenquery.acceptors.core.string_opr import str_eq
from tokenquery.acceptors.core.string_opr import str_reg
from tokenquery.acceptors.core.string_opr import str_len
from tokenquery.acceptors.core.int_opr import *
from tokenquery.acceptors.core.web_opr import *


class TokenQuery:

    def __init__(self, token_query_string, verbose=False):
        self.acceptors = {}
        self.acceptors['str_eq'] = str_eq
        self.acceptors['str_reg'] = str_reg
        self.acceptors['str_len'] = str_len
        self.verbose = verbose
        parsed_token_query_string = self.parse(token_query_string)
        if self.verbose:
            print (parsed_token_query_string)
        self.machine = self.compile(parsed_token_query_string)
        if self.verbose:
            self.machine.print_state_machine()

    def match_tokens(self, input_tokens):
        final_results = []
        # ranges = {}
        last_matched = -1
        for start_point in range(len(input_tokens)):
            # skip from the matched ones
            if start_point > last_matched:
                sub_input_tokens = input_tokens[start_point:]
                result_set = self.machine.runAll(sub_input_tokens)
                if result_set:
                    final_results += result_set
                    for result_item in result_set:
                        for group_key in result_item:
                            group = result_item[group_key]
                            if len(group) > 0:
                                last_matched_token = group[-1].get_token_id()
                                if last_matched_token > last_matched:
                                    last_matched = last_matched_token

        # change into max match

        # for result in result_set:
        #     ranges.append(range(result[0],result[0])
        return final_results

    def parse(self, token_query_string):
        """
           Parsing token query string
        """

        parser_stack = Stack()

        parsed = []
        capturing_inside_a_token_mode = False
        capturing_expr_for_token_mode = False
        capture_chunk_id = 1
        capture_mode_name = None

        not_mode = False
        repetition_capture_mode = False
        repetition = 0

        # shorthand modes
        expr_regex_shorthand_mode = False
        expr_string_shorthand_mode = False

        for next_char in token_query_string:
            if self.verbose:
                print ('next char : ', next_char)
                print ('current stack : ', parser_stack.items)
                # print ('capturing_inside_a_token_mode : ', capturing_inside_a_token_mode)
                # print ('expr_regex_shorthand_mode : ', expr_regex_shorthand_mode)
                # print ('expr_string_shorthand_mode : ', expr_string_shorthand_mode)
            # ignore white spaces
            if next_char.isspace():
                continue

            # inside a token
            if capturing_inside_a_token_mode:

                # inside an expression
                if capturing_expr_for_token_mode:

                    # String shorthand mode
                    if expr_string_shorthand_mode:
                        if next_char == '"':
                            active_operation['type'] = 'str_eq'
                            active_operation['opr_input'] = capturer
                            expr_string_shorthand_mode = False
                            capturer = ""
                            parser_stack.push(active_operation)
                            capturing_expr_for_token_mode = False
                            continue
                        else:
                            capturer += next_char

                    # Regex shorthand mode
                    elif expr_regex_shorthand_mode:
                        if next_char == '/':
                            active_operation['type'] = 'str_reg'
                            active_operation['opr_input'] = capturer
                            expr_regex_shorthand_mode = False
                            capturer = ""
                            parser_stack.push(active_operation)
                            capturing_expr_for_token_mode = False
                            continue
                        else:
                            capturer += next_char

                    # Normal mode
                    else:
                        # go to string shorthand mode
                        if capturer == '"':
                            capturer = next_char
                            expr_string_shorthand_mode = True
                            continue

                        # go to regex shorthand mode
                        if capturer == '/':
                            capturer = next_char
                            expr_regex_shorthand_mode = True
                            continue

                        # end of label
                        if next_char == ':':
                            # previous captured thing is a label
                            active_operation['label'] = capturer
                            capturer = ""

                        # start of operation
                        elif next_char == '(':
                            # previous captured thing is a label
                            active_operation['type'] = capturer
                            capturer = ""

                        # end of operation
                        elif next_char == ')':
                            # push a new operation
                            if capturer:
                                active_operation['opr_input'] = capturer

                            # if not mode
                            if not_mode:
                                negated_operation = {'opr1': active_operation,
                                                     'type': 'comp_not'}
                                not_mode = False
                                parser_stack.push(negated_operation)

                            # adding new operation
                            else:
                                parser_stack.push(active_operation)
                            capturing_expr_for_token_mode = False

                        # add char to the capturer
                        else:
                            capturer += next_char

                        # deal with this later
                        # if char == '"':
                        #     capturing_expr_for_token_mode = True

                    # if next_char == "\\" and not scape_mode:
                    #     scape_mode = True

                # outside an expression  (compounding stuff)
                else:
                    if next_char == "(":
                        parser_stack.push('(')
                    elif next_char == "&":
                        parser_stack.push('&')
                    elif next_char == "|":
                        parser_stack.push('|')
                    elif next_char == "!":
                        not_mode = True

                    elif next_char == ")":
                        while(parser_stack.size() > 2):
                            item2 = parser_stack.pop()
                            op = parser_stack.pop()
                            item1 = parser_stack.pop()
                            if op == '&':
                                new_acceptor = {'opr1': item1,
                                                'opr2': item2,
                                                'type': 'comp_and'}
                            if op == "|":
                                new_acceptor = {'opr1': item1,
                                                'opr2': item2,
                                                'type': 'comp_or'}

                            if parser_stack.size() == 0:
                                parser_stack.push(new_acceptor)
                                break

                            if parser_stack.peek() == '(':
                                parser_stack.pop()
                                parser_stack.push(new_acceptor)
                                break

                            parser_stack.push(new_acceptor)

                        if parser_stack.size() != 1:
                            raise ValueError('Parssing error! parser stack: {} .'.format(parser_stack))

                        # start of a token
                        if next_char == "]":
                            parsed.append({'type': 'segment', 'value': active_operation})
                            capturing_inside_a_token_mode = False
                            # reset capturer
                            capturer = ""
                            continue

                    elif next_char == "]":
                        while(parser_stack.size() > 2):
                            item2 = parser_stack.pop()
                            op = parser_stack.pop()
                            item1 = parser_stack.pop()
                            if op == '&':
                                new_acceptor = {'opr1': item1,
                                                'opr2': item2,
                                                'type': 'comp_and'}
                            if op == "|":
                                new_acceptor = {'opr1': item1,
                                                'opr2': item2,
                                                'type': 'comp_or'}

                            if parser_stack.size() == 0:
                                parser_stack.push(new_acceptor)
                                break

                            if parser_stack.peek() == '(':
                                parser_stack.pop()
                                parser_stack.push(new_acceptor)
                                break

                            parser_stack.push(new_acceptor)

                        if parser_stack.size() != 1:
                            raise ValueError('Parssing error! parser stack: {} .'.format(parser_stack))

                        active_operation = parser_stack.pop()
                        parsed.append({'type': 'segment', 'value': active_operation})
                        capturing_inside_a_token_mode = False
                        capturer = ""
                        continue

                    # start of an expression
                    else:
                        capturer = next_char
                        active_operation = {'type': '', 'label': 'text'}
                        capturing_expr_for_token_mode = True

            # outside a token
            else:
                if repetition_capture_mode:
                    if next_char == "}":
                        if start_repetition:
                            parsed.append({'type': 'repetition_range', 'start': start_repetition, 'end': repetition})
                        else:
                            parsed.append({'type': 'repetition', 'value': repetition})
                        repetition = 0
                        start_repetition = None
                        repetition_capture_mode = False

                    elif next_char.isdigit():
                        repetition = repetition * 10 + int(next_char)

                    elif next_char == ",":
                        start_repetition = repetition
                        repetition = 0

                    else:
                        raise ValueError('Parser is not able to parse {} beacuse of invalid repetition char {} .'.format(token_query_string, char))
                    continue

                if capture_mode_name != None:
                    if next_char in ["(", " ", "["]:
                        if capture_mode_name:
                            name = capture_mode_name
                        else:
                            name = "chunk " + str(capture_chunk_id)
                        capture_chunk_id += 1
                        parsed.append({'type': 'capture', 'value': 'On', 'name': name})
                        capture_mode_name = None
                    else:
                        capture_mode_name += next_char
                        continue

                if next_char == "*":
                    #  zero or more times
                    parsed.append({'type': 'repetition', 'value': '*'})
                if next_char == "?":
                    # once or not at all
                    parsed.append({'type': 'repetition', 'value': '?'})
                if next_char == "+":
                    # one or more time
                    parsed.append({'type': 'repetition', 'value': '+'})

                if next_char == "{":
                    # fixed number
                    repetition = 0
                    start_repetition = None
                    repetition_capture_mode = True

                if next_char == "(":
                    capture_mode_name = ""

                if next_char == ")":
                    parsed.append({'type': 'capture', 'value': 'Off'})
                    capture_mode_name = None

                if next_char == "[":
                    parser_stack = Stack()
                    capturing_inside_a_token_mode = True
                    continue

        return parsed

    def compile(self, parsed_token_regex):
        # add start node
        # capture_mode = False
        capture_name = None
        no_capture_at_all = True
        previous_connection = False

        start_state = State('start', capture_name, self.acceptors)
        states = [start_state]
        current_state = start_state
        prev_state = None
        prev_segment = None

        state_counter = 1
        for item in parsed_token_regex:

            if item['type'] == 'segment':
                next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                states.append(next_state)
                state_counter += 1
                # machine.add_a_transition(Transition(item['value'], current_state, next_state))
                current_state.add_a_next(item['value'], next_state)

                if previous_connection:
                    # machine.add_a_transition(Transition(item['value'], prev_state, next_state))
                    prev_state.add_a_next(item['value'], next_state)

                    previous_connection = False
                prev_state = current_state
                current_state = next_state
                prev_segment = item['value']

            elif item['type'] == 'capture':
                if item['value'] == "On":
                    # capture_mode = True
                    capture_name = item['name']
                    # fix start state capture mode
                    if len(states) == 1:
                        states[0].capture_name = capture_name
                    no_capture_at_all = False
                else:
                    capture_name = None
                    # capture_mode = False

            elif item['type'] == 'repetition':
                if item['value'] == "*":
                    current_state.add_a_next(prev_segment, current_state)
                    # machine.add_a_transition(Transition(prev_segment, current_state, current_state))
                    previous_connection = True
                elif item['value'] == "?":
                    previous_connection = True

                elif item['value'] == "+":
                    current_state.add_a_next(prev_segment, current_state)
                    # machine.add_a_transition(Transition(prev_segment, current_state, current_state ))

                elif item['value']:
                    if item['value'] > 1:
                        for i in range(item['value']-1):
                            next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                            states.append(next_state)
                            state_counter += 1
                            current_state.add_a_next(prev_segment, next_state)
                            # machine.add_a_transition(Transition(prev_segment, current_state, next_state))
                            prev_state = current_state
                            current_state = next_state

            elif item['type'] == 'repetition_range':
                # repetition starts from 1
                source_state = prev_state  # current_state
                if item['end'] - item['start'] > 0:
                    for i in range(item['end']-item['start']):
                            next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                            states.append(next_state)
                            state_counter += 1
                            current_state.add_a_next(prev_segment, next_state)
                            #if i > 0:
                            source_state.add_a_next(prev_segment, next_state)

                            # machine.add_a_transition(Transition(prev_segment, current_state, next_state))
                            prev_state = current_state
                            current_state = next_state

                if item['start'] > 1:
                    for i in range(item['start']-1):
                        next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                        states.append(next_state)
                        state_counter += 1
                        current_state.add_a_next(prev_segment, next_state)
                        # machine.add_a_transition(Transition(prev_segment, current_state, next_state))
                        prev_state = current_state
                        current_state = next_state
                #     previous_connection = True
                # elif item['start'] == 1:
                #     previous_connection = True

        last_state = State('end', capture_name, self.acceptors, True)
        any_rule = {'type': 'str_reg',
                    'label': 'text',
                    'opr_input': '.*|[\r\n]+'}
        current_state.add_a_next(any_rule, last_state)

        states.append(last_state)

        # if no capture, capture all
        if no_capture_at_all:
            for state in states:
                state.capture_name = 'chunk 1'

        return StateMachine(start_state, states)
