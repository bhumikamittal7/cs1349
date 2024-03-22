# NFA to simulate a language that accepts strings that is accepted by the following language:
# L = { w = w_1w_2 ... w_n \in {a,b,c,$,*,#,1,2,3} | n>= 6, w_i \in {1,2,3}, w_j \in {a,b,c}, w_k \in {$,*,#} for some 1 <= i,j,k <= n and the string doesn't contain 123 as a substring }


# ==================================== Checking the file format ====================================
#check if the file is in the correct format
def check_file_format(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        if len(lines) < 5:
            return False
        #we need to check if there are lines starting with # States, # Alphabet, # Start, # Accept, # Transitions
        states, alphabet, start, accept, transitions = False, False, False, False, False
        for line in lines:
            line = line.strip()
            if line == '# States':
                states = True
            elif line == '# Alphabet':
                alphabet = True
            elif line == '# Start':
                start = True
            elif line == '# Accept':
                accept = True
            elif line == '# Transitions':
                transitions = True
        return states and alphabet and start and accept and transitions
    
#==================================== Reading the DFA ====================================
# The file has the "# States" line, followed by the states, then the "# Alphabet" line, followed by the alphabet, then the "# Start" line, 
# followed by the start state, then the "# Accept" line, followed by the accept states, then the "# Transitions" line, followed by the transitions

def read_dfa_description(file_name):    
    states = []
    alphabet = []
    start_state = ''
    accept_states = []
    transitions = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, False, False
        for line in lines:
            line = line.strip()
            if line == '# States':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = True, False, False, False, False
            elif line == '# Alphabet':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, True, False, False, False
            elif line == '# Start':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, True, False, False
            elif line == '# Accept':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, True, False
            elif line == '# Transitions':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, False, True

            elif reading_states:
                states.append(line)
            elif reading_alphabet:
                alphabet.append(line)
            elif reading_start:
                start_state = line
            elif reading_accept:
                accept_states.append(line)
            elif reading_transitions:
                transition = line.split()
                transitions.append((transition[0], transition[1], transition[2])) # (from, symbol, to)

    return states, alphabet, start_state, accept_states, transitions

def is_dfa(states, alphabet, start_state, accept_states, transitions):
    # a dfa is a valid dfa if:
    # 1. the start state is in the set of states
    # 2. the accept states are a subset of the states
    # 3. for each state and symbol, there is exactly one transition
    # 4. the alphabet is not empty
    if start_state not in states:
        return False
    if not set(accept_states).issubset(set(states)):
        return False
    if len(alphabet) == 0:
        return False
    for state in states:
        for symbol in alphabet:
            transitions_from_state = [t for t in transitions if t[0] == state and t[1] == symbol]
            if len(transitions_from_state) != 1:
                return False
    return True

# ==================================== Simulating the DFA ====================================
def simulate_dfa(states, alphabet, start_state, accept_states, transitions, string):
    current_state = start_state
    for symbol in string:
        if symbol not in alphabet:
            return False
        transition = [t for t in transitions if t[0] == current_state and t[1] == symbol][0]
        current_state = transition[2]
    
    res = current_state in accept_states
    if res:
       return True
    else:
        return False

def mainDFA(file_name, word):
    if not check_file_format(file_name):
        return False
    
    states, alphabet, start_state, accept_states, transitions = read_dfa_description(file_name)

    if is_dfa(states, alphabet, start_state, accept_states, transitions) == False:
        return False
    
    if (simulate_dfa(states, alphabet, start_state, accept_states, transitions, word)):
        return True
    else:
        return False
    
#==================================== NFA ====================================
#==================================== Reading the NFA ====================================
def read_nfa_description(file_name):    
    states = []
    alphabet = []
    start_state = ''
    accept_states = []
    transitions = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, False, False
        for line in lines:
            line = line.strip()
            if line == '# States':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = True, False, False, False, False
            elif line == '# Alphabet':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, True, False, False, False
            elif line == '# Start':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, True, False, False
            elif line == '# Accept':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, True, False
            elif line == '# Transitions':
                reading_states, reading_alphabet, reading_start, reading_accept, reading_transitions = False, False, False, False, True

            elif reading_states:
                states.append(line)
            elif reading_alphabet:
                alphabet.append(line)
            elif reading_start:
                start_state = line
            elif reading_accept:
                accept_states.append(line)
            elif reading_transitions:
                transition = line.split()
                transitions.append((transition[0], transition[1], transition[2])) # (from, symbol, to)

    return states, alphabet, start_state, accept_states, transitions

#==================================== Designing NFA ====================================
class NFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.validate_transition_function()

    # Validation function
    def validate_transition_function(self):
        transition_states = set()
        for transition in self.transitions:
            if transition[0] not in self.states or transition[2] not in self.states:
                raise Exception('Invalid transition states.')
            transition_states.add((transition[0], transition[1]))
        if len(transition_states) != len(self.transitions):
            raise Exception('Duplicate transitions detected.')

    def transition(self, state, symbol):
        possible_transitions = []
        for transition in self.transitions:
            if transition[0] == state and transition[1] == symbol:
                possible_transitions.append(transition[2])
        return possible_transitions

    def simulate(self, string):
        return self.accept(self.start_state, string)

    def accept(self, state, string):
        if len(string) == 0:
            return state in self.accept_states
        for next_state in self.transition(state, string[0]):
            if self.accept(next_state, string[1:]):
                return True
        for next_state in self.transition(state, 'eps'):
            if self.accept(next_state, string):
                return True
        return False

def mainNFA(file_name, word):
    if not check_file_format(file_name):
        return False
    
    states, alphabet, start_state, accept_states, transitions = read_nfa_description(file_name)

    nfa = NFA(states, alphabet, start_state, accept_states, transitions)
    result = nfa.simulate(word)
    if result:
        return True
    else:
        return False

#==================================== Combining NFAs and DFAs ====================================
def lenSix(word):
    if mainDFA('lenSix.txt', word):
        # print ("Accepted by lenSix")
        return True
    else:
        return False

def wi(word):
    if mainDFA('wi.txt', word):
        # print ("Accepted by wi")
        return True
    else:
        return False

def wj(word):
    if mainDFA('wj.txt', word):
        # print ("Accepted by wj")
        return True
    else:
        return False
    
def wk(word):
    if mainDFA('wk.txt', word):
        # print ("Accepted by wk")
        return True
    else:
        return False
    
def substring123(word):
    if mainDFA('substring123.txt', word):
        # print ("Accepted by substring123")
        return True
    else:
        return False
    
def main():
    word = input("Enter a string: ")
    res = lenSix(word) and wi(word) and wj(word) and wk(word) and substring123(word)
    if res:
        print("The string {} is accepted by the language".format(word))
        print("#=======================================================")
    else:
        print("The string {} is not accepted by the language".format(word))
        print("#=======================================================")

#==================================== Testing ====================================
# word = ["abc12$", "abc#3*", "123abc", "123abc$", "12abc#3$*", "1#3abc12"]

# for words in word:
#     main(words)

#==================================== Running the program ====================================
main()
