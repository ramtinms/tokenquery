
import re
from nltk.tokenize import word_tokenize

class State:

    def __init__(self, state_name, capture_mode, is_final=False):
        self.transitions = []
        self.state_name = state_name
        self.capture_mode = capture_mode
        self.is_final = is_final

    def __str__(self):
        return self.state_name

    def next(self, input_token):
        nexts = []
        for transition, next_state in self.transitions:
            if transition['cond_type'] == "match_text":
                if not transition['label']:
                    if input_token.text_is_equal(transition['value']):
                        nexts.append(next_state)
                else:
                    if input_token.label_is_equal(transition['label'], transition['value']):
                        nexts.append(next_state)

            elif transition['cond_type'] == "match_regex":
                if not transition['label']:
                    if input_token.text_match_a_regex(transition['value']):
                        nexts.append(next_state)
                else:
                    if input_token.label_match_a_regex(transition['label'],transition['value']):
                        nexts.append(next_state)

            elif transition['cond_type'] == "number_comp":
                if input_token.is_a_number(transition['comp_type'],transition['value']):
                    nexts.append(next_state)

        return nexts

    def add_a_next(self, segment_condition, next_state):
        self.transitions.append((segment_condition, next_state))


class StateMachine:
    def __init__(self, initialState, states):
        self.currentState = initialState
        self.states = states

    def print_state_machine(self):
        print "<>"*20
        for state in self.states:
            print 'state name: ', state.state_name
            print 'capture mode :', state.capture_mode
            print 'is final :', state.is_final
            for cond, next in state.transitions:
                print cond, ' ---> ', next.state_name

    # I need an stack (active context)
    def runAll(self, inputs):
        captured_info_list = []
        captured_info_item = []
        curser = 0
        # Stack
        stack = [(self.currentState, curser, captured_info_list, captured_info_item)]

        groups = []

        # push down automata
        max_stack_size = 100

        while stack and len(stack) < max_stack_size :
            currentState, curser, captured_info_list, captured_info_item = stack.pop()
            # print(currentState.state_name, curser, captured_info_list, captured_info_item)
            # print inputs[curser].get_text()

            if curser < len(inputs):
                token = inputs[curser]

                # capturing

                nexts = currentState.next(token)
                if nexts:
                    for next in nexts:
                        if next.is_final:
                            if captured_info_item:
                                captured_info_list.append(captured_info_item)
                            groups.append(captured_info_list)
                        else:
                            if next.capture_mode:
                                captured_info_item.append(token)
                            elif captured_info_item:
                                captured_info_list.append(captured_info_item)
                                captured_info_item = []

                            stack.append((next, curser+1, captured_info_list, captured_info_item))
            else:
                if currentState.is_final:
                    if captured_info_item:
                        captured_info_list.append(captured_info_item)
                    if captured_info_list:
                        groups.append(captured_info_list)


        return groups
