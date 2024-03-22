'''
NFA Simulation:
• Input: A description of a NFA N over an arbitrary alphabet Σ; and a string x ∈ Σ∗
• Output: Accept if x ∈ L(N), otherwise reject
'''
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
    
#==================================== Reading the NFA ====================================
# The file has the "# States" line, followed by the states, then the "# Alphabet" line, followed by the alphabet, then the "# Start" line, followed by the start state, then the "# Accept" line, followed by the accept states, then the "# Transitions" line, followed by the transitions

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

# ==================================== Main Function ====================================
def main():
    print('Welcome to the NFA simulator')
    file_name = 'nfa.txt'

    if not check_file_format(file_name):
        print('The file is not in the correct format. Please check the file format and try again.')
        print('The file should have the "# States" line, followed by the states, then the "# Alphabet" line, followed by the alphabet, then the "# Start" line, followed by the start state, then the "# Accept" line, followed by the accept states, then the "# Transitions" line, followed by the transitions')
        return
    
    states, alphabet, start_state, accept_states, transitions = read_nfa_description(file_name)
    choice = input('Do you want to check if a string is in the language? (y/n) ')

    while choice == 'y':
        string = input('Enter a string to check if it is in the language: ')
        nfa = NFA(states, alphabet, start_state, accept_states, transitions)
        result = nfa.simulate(string)
        if result:
            print('Yayy! The string is in the language generated by the NFA!🎉')
        else:
            print('Ahh! The string is not in the language generated by the NFA!😢')
        choice = input('Do you want to check if another string is in the language? (y/n) ')

    print('Thank you for using the NFA simulator')
    print('Bye bye!')        

# ==================================== Run ====================================
main()