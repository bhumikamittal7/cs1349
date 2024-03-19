'''
DFA Simulation:
• Input: A description of a DFA M over an arbitrary alphabet Σ; and a string x ∈ Σ∗
• Output: Accept if x ∈ L(M), otherwise reject

To simulate a DFA
1. We start at the start state
2. For each character in the string, we follow the transition for that character
3. If we reach the end of the string and we are in an accepting state, then the string is in the language
4. If we reach the end of the string and we are not in an accepting state, then the string is not in the language
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

# ==================================== Validity of the DFA ====================================
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
            print(f'The string "{string}" is not in the language')
            return
        transition = [t for t in transitions if t[0] == current_state and t[1] == symbol][0]
        current_state = transition[2]
    
    res = current_state in accept_states
    if res:
        print(f'The string "{string}" is in the language')
    else:
        print(f'The string "{string}" is not in the language')

# ==================================== Main Function ====================================
def main():
    print('Welcome to the DFA simulator')
    file_name = 'dfa.txt'

    if not check_file_format(file_name):
        print('The file is not in the correct format. Please check the file format and try again.')
        print('The file should have the "# States" line, followed by the states, then the "# Alphabet" line, followed by the alphabet, then the "# Start" line, followed by the start state, then the "# Accept" line, followed by the accept states, then the "# Transitions" line, followed by the transitions')
        return
    
    states, alphabet, start_state, accept_states, transitions = read_dfa_description(file_name)

    if is_dfa(states, alphabet, start_state, accept_states, transitions) == False:
        print('The DFA is not valid')
        return
    
    choice = input('Do you want to check if a string is in the language? (y/n) ')

    while choice == 'y':
        string = input('Enter a string to check if it is in the language: ')
        simulate_dfa(states, alphabet, start_state, accept_states, transitions, string)
        choice = input('Do you want to check if another string is in the language? (y/n) ')

    print('Thank you for using the DFA simulator')
    print('Bye bye!')        

# ==================================== Run ====================================
main()