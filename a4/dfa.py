'''
DFA Simulation:
• Input: A description of a DFA M over an arbitrary alphabet Σ; and a string x ∈ Σ∗
• Output: Accept if x ∈ L(M), otherwise reject

PS - no library used
'''
#read the DFA description from the file

def read_dfa_description(file_name):
    with open(file_name, 'r') as file:
        states = file.readline().split()
        alphabet = file.readline().split()
        start_state = file.readline().strip()
        accept_states = file.readline().split()
        transitions = [line.split() for line in file]
    return states, alphabet, start_state, accept_states, transitions

#check if it is a valid DFA
def is_dfa(states, alphabet, start_state, accept_states, transitions):
    if start_state not in states:
        return False
    
    # Check for duplicate transitions
    transitions_set = set()
    for transition in transitions:
        transition_tuple = (transition[0], transition[1])
        if transition_tuple in transitions_set:
            return False
        transitions_set.add(transition_tuple)
    
    # Check for unreachable states
    reachable_states = set()
    queue = [start_state]
    while queue:
        current_state = queue.pop(0)
        reachable_states.add(current_state)
        for transition in transitions:
            if transition[0] == current_state:
                next_state = transition[2]
                if next_state not in reachable_states:
                    queue.append(next_state)
    
    if not all(state in reachable_states for state in states):
        return False

#simulate the DFA
def simulate_dfa(states, alphabet, start_state, accept_states, transitions, input_string):
    if not is_dfa(states, alphabet, start_state, accept_states, transitions):
        raise ValueError('Invalid DFA description')
    current_state = start_state
    for symbol in input_string:
        for transition in transitions:
            if transition[0] == current_state and transition[1] == symbol:
                current_state = transition[2]
                break
    return current_state in accept_states

#main function
def main():
    file_name = 'dfa.txt'
    input_string = 'abb'
    states, alphabet, start_state, accept_states, transitions = read_dfa_description(file_name)
    if simulate_dfa(states, alphabet, start_state, accept_states, transitions, input_string):
        print('Accepted')
    else:
        print('Rejected')

main()