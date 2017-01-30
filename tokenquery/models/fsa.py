class State:

    def __init__(self, state_name, capture_name, acceptors, is_final=False):
        self.transitions = []
        self.state_name = state_name
        self.capture_name = capture_name
        self.acceptors = acceptors
        self.is_final = is_final

    def __str__(self):
        return self.state_name

    def get_state_name(self):
        return self.state_name

    def capture_name(self):
        return self.capture_name

    def accept(self, acceptor, token):
        # print (acceptor)
        if acceptor['type'] == 'comp_not':
            return not self.accept(acceptor['opr1'], token)

        elif acceptor['type'] == 'comp_and':
            res1 = self.accept(acceptor['opr1'], token)
            res2 = self.accept(acceptor['opr2'], token)
            return res1 and res2

        elif acceptor['type'] == 'comp_or':
            res1 = self.accept(acceptor['opr1'], token)
            res2 = self.accept(acceptor['opr2'], token)
            return res1 or res2

        elif acceptor['type'] in self.acceptors:
            opr_input = acceptor.get('opr_input', None)

            if acceptor['label'] == 'text':
                token_input = token.get_text()
            else:
                token_input = token.get_a_label(acceptor['label'])

            # if not token_input:
            #     print ("something went wrong, token input is empty")

            if opr_input:
                return self.acceptors[acceptor['type']](token_input, opr_input)
            else:
                return self.acceptors[acceptor['type']](token_input)
        else:
            print ("something went wrong! unknown operation {}".format(acceptor['type']))

    def next(self, input_token):
        nexts = []
        for transition, next_state in self.transitions:
            if self.accept(transition, input_token):
                nexts.append(next_state)
        return nexts

    def add_a_next(self, segment_condition, next_state):
        self.transitions.append((segment_condition, next_state))


class StateMachine:

    def __init__(self, initialState, states, max_stack_size=200, verbose=False):
        self.currentState = initialState
        self.states = states
        self.max_stack_size = max_stack_size
        self.verbose = verbose

    def print_state_machine(self):
        print ("<>"*20)
        for state in self.states:
            print ('state name: ', state.state_name)
            print ('capture name :', state.capture_name)
            print ('is final :', state.is_final)
            for cond, next in state.transitions:
                print (cond, ' ---> ', next.state_name)

    # exuastive search
    def runAll(self, inputs):
        captured_dictionary = {}
        captured_info_item = []
        capture_name = self.currentState.capture_name
        curser = 0
        # Stack
        stack = [(self.currentState, curser, captured_dictionary, captured_info_item, capture_name)]
        groups = []

        # push down automata
        while stack and len(stack) < self.max_stack_size:
            currentState, curser, captured_dictionary, captured_info_item, capture_name = stack.pop()
            # print (currentState, curser, captured_dictionary, captured_info_item)
            # if captured_info_item:
            #     print ('capturer : ', ' '.join([token.get_text() for token in captured_info_item]))

            if curser < len(inputs):
                token = inputs[curser]
                # print ('token : ', token.get_text())
                # capturing
                nexts = currentState.next(token)
                if nexts:
                    for next in nexts:
                        if next.is_final:
                            if captured_info_item:
                                captured_dictionary[capture_name] = captured_info_item
                            if captured_dictionary not in groups:
                                groups.append(captured_dictionary)
                        else:
                            # print (token.get_text(), capture_name, next.capture_name, captured_info_item)
                            if next.capture_name and not capture_name:
                                # starting mode
                                if token not in captured_info_item:
                                    captured_info_item.append(token)

                            elif next.capture_name and next.capture_name == capture_name:
                                if token not in captured_info_item:
                                    captured_info_item.append(token)

                            elif next.capture_name != capture_name:
                                if captured_info_item:
                                    captured_dictionary[capture_name] = captured_info_item
                                    captured_info_item = []
                                if next.capture_name:
                                    captured_info_item.append(token)

                            capture_name = next.capture_name
                            stack.append((next, curser+1, captured_dictionary, captured_info_item, capture_name))
            else:
                if currentState.is_final:
                    if captured_info_item:
                        captured_dictionary[capture_name] = captured_info_item
                    if captured_dictionary:
                        if captured_dictionary not in groups:
                            groups.append(captured_dictionary)

        return groups
