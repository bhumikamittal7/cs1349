import sys
import json

class NondeterministicFiniteAutomata(object):

	def __init__(self, definition):
		self.definition = definition
		self.validate_transition_function()

	def compute(self, string):
		self.validate_string(string)
		return self.accept(self.start_state(), string)

	def accept(self, state, string, forbidden_transitions=[]):
		if(len(string) == 0):
			if self.is_final_state(state):
					return True

			if (state, 'epsilon') not in forbidden_transitions:
				for next_state in self.transition(state, 'epsilon'):
					forbidden_transitions.append((state, 'epsilon'))
					if self.accept(next_state, string, forbidden_transitions):
						return True
			return False

		char = string[0]
		remaining_string = string[1:]

		# First try without epsilon transitions
		for next_state in self.transition(state, char):
			if self.accept(next_state, remaining_string, []):
				return True

		# Didn't worked, now try with epsilon transitions
		if (state, 'epsilon') not in forbidden_transitions:
			for next_state in self.transition(state, 'epsilon'):
				forbidden_transitions.append((state, 'epsilon'))
				if self.accept(next_state, string, forbidden_transitions):
					return True

		return False

	# Validation function

	def validate_transition_function(self):
		transition_function_states_set = set(self.transition_function_states())
		states_set = set(self.states())

		if not transition_function_states_set.issubset(states_set):
			raise Exception('The transition function contains states that are not on the states definition.')

	def validate_string(self, string):
		if not self.valid_string(string):
			raise Exception('String not valid according with automata definition.')

	def valid_string(self, string):
		string_set = set(string)
		alphabet_set = set(self.alphabet())

		return string_set.issubset(alphabet_set)

	# Auxiliar methods

	def transition_function_states(self):
		return self.definition['delta'].keys()

	def states(self):
		return self.definition['Q']

	def alphabet(self):
		return self.definition['sigma']

	def start_state(self):
		return self.definition['q0']

	def is_final_state(self, state):
		return state in self.definition['f']

	def transition(self, state, char):
		return self.definition['delta'].get(state, dict()).get(char, [])

if __name__ == '__main__':
	definition = json.loads(open(sys.argv[1], 'r').read())
	string = sys.argv[2]

	nfa = NondeterministicFiniteAutomata(definition)
	print(nfa.compute(string))