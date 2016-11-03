import re
from models.fsa import State
from models.fsa import StateMachine


class TokenRegex:

    def __init__(self, token_regex_string):

        parsed_token_regex_string = self.parse(token_regex_string)
        self.machine = self.compile(parsed_token_regex_string)

    def match_tokens(self, input_tokens):
        final_results = []
        for start_point in range(len(input_tokens)):
            sub_input_tokens = input_tokens[start_point:]
            result_set = self.machine.runAll(sub_input_tokens)
            if result_set:
                for result in result_set:
                    for group in result:
                        for item in group:
                            print item.get_text()
                final_results += result_set
        return final_results

    def parse_a_segment_info(self, segment_string):
        r"""
            - "abc"  text match
            - /abc/ regex match
            - pos:"NNP"     (token_label:)  POS
            - pos:/NN.*/  regex over label   POS
            - word>30  text is number and greater than 30 ( >=, <. <=, ==, !=) supported
        """

        cond_type = None
        value = None
        label = None
        comp_type = None

        if segment_string[0] == '"' and segment_string[-1] == '"':
            cond_type = "match_text"
            value = segment_string[1:-1]
            label = ""
        elif segment_string[0] == '/' and segment_string[-1] == '/':
            cond_type = "match_regex"
            value = segment_string[1:-1]
            label = ""
        elif ':' in segment_string:
            label, remaining = segment_string.split(':', 1)
            if remaining[0] == '"' and remaining[-1] == '"':
                cond_type = "match_text"
                value = remaining[1:-1]
            elif remaining[0] == '/' and remaining[-1] == '/':
                cond_type = "match_regex"
                value = remaining[1:-1]
        elif 'word' == segment_string[:4]:
            part = segment_string[4:]
            # removing spaces
            comp_part = part.lstrip().strip()[:2]
            if comp_part in ['==', '>=', '<=', '!=']:
                comp_type = comp_part
                cond_type = "number_comp"
                # TODO add try
                value = int(part.lstrip().strip()[2:])
                label = "number_value"
            elif comp_part[0] in ['>', '<']:
                comp_type = comp_part[0]
                # TODO add try
                value = int(part.lstrip().strip()[1:])
                cond_type = "number_comp"
                label = "number_value"

        if cond_type is None or value is None or label is None:
            raise ValueError('Parser is not able to parse this segment {} .'.format(segment_string))
            return None
            # TODO exception

        rule = {'cond_type': cond_type,
                'label': label,
                'value': value
                }
        if comp_type:
            rule['comp_type'] = comp_type

        return rule


    def parse(self, token_regex_string):

        segment_capture_mode = False
        segment = ""

        repetition_capture_mode = False
        repetition = 0

        scape_mode = False

        parsed = []

        for char in token_regex_string:

            # scapce_chars
            if segment_capture_mode:
                # for \] and \\
                if char == "]" and not scape_mode:
                    parsed_segment = self.parse_a_segment_info(segment)
                    parsed.append({'type': 'segment', 'value': parsed_segment})
                    segment = ""
                    segment_capture_mode = False

                elif char == "\\" and not scape_mode:
                    scape_mode = True

                else:
                    segment += char
                    scape_mode = False

                continue

            if repetition_capture_mode:
                if char == "}":
                    parsed.append({'type': 'repetition', 'value': repetition})
                    repetition = 0
                    repetition_capture_mode = False

                elif char.is_digit():
                    repetition = repetition * 10 + int(char)

                else:
                    raise ValueError('Parser is not able to parse {} beacuse of invalid repetition char {} .'.format(token_regex_string, char))
                continue

            # command chars
            if char == "[":
                # start of a segment
                segment_capture_mode = True
                segment = ""

            elif char == "*":
                #  zero or more times
                parsed.append({'type': 'repetition', 'value': '*'})
            elif char == "?":
                # once or not at all
                parsed.append({'type': 'repetition', 'value': '?'})
            elif char == "+":
                # one or more time
                parsed.append({'type': 'repetition', 'value': '+'})

            elif char == "{":
                # fixed number
                repetition_capture_mode = True

            elif char == "(":
                parsed.append({'type': 'capture', 'value': 'On'})

            elif char == ")":
                parsed.append({'type': 'capture', 'value': 'Off'})

        return parsed


    def compile(self, parsed_token_regex):
        #stateMachine =

        # add start node
        capture_mode = False
        no_capture_at_all = True
        previous_connection = False

        start_state = State('start', capture_mode)
        states = [start_state]
        current_state = start_state
        prev_state = None
        prev_segment = None


        state_counter = 1
        for item in parsed_token_regex:

            if item['type'] == 'segment':
                next_state = State('state ' + str(state_counter), capture_mode)
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
                    capture_mode = True
                    no_capture_at_all = False
                else:
                    capture_mode = False

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
                    # todo check if it is a number
                    for i in range(item['value']):
                        next_state = State('state ' + str(state_counter), capture_mode)
                        states.append(next_state)
                        state_counter += 1
                        current_state.add_a_next(prev_segment, next_state)
                        # machine.add_a_transition(Transition(prev_segment, current_state, next_state))
                        prev_state = current_state
                        current_state = next_state

        last_state = State('end', capture_mode, True)
        any_rule = {'cond_type': 'match_regex',
                    'label': '',
                    'value': '.*'}
        current_state.add_a_next(any_rule, last_state)

        states.append(last_state)

        # if no capture, capture all
        if no_capture_at_all:
            for state in states:
                state.capture_mode = True

        return StateMachine(start_state, states)


if __name__ == "__main__":

    from nlp.tokenizer import Tokenizer
    t = Tokenizer()
    input_tokens = t.tokenize('David is a painter and ')
    input_tokens[0].add_a_label('ner', 'PERSON')
    input_tokens[1].add_a_label('pos', 'VBZ')

    test_case_0 = '[ner:"PERSON"]+ [pos:"VBZ"] [/an?/] ["painter"]'
    unit = TokenRegex(test_case_0)
    unit.match_tokens(input_tokens)

    print "<>"*25

    test_case_1 = '([ner:"PERSON"]+) [pos:"VBZ"] [/an?/] ["painter"]'
    unit = TokenRegex(test_case_1)
    unit.match_tokens(input_tokens)
