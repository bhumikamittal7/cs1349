# ===================================== Shunting Yard Algorithm =====================================
def shunt(regex):
  # Precedence of the operators
  # * - Kleene closure
  # + - Positive closure
  # ? - Optional
  # . - concatenation
  # | - union/or
  symbols = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}

  postfix = ""
  stack = ""

  for character in regex:
    if character == '(':
      stack = stack + character
    elif character == ')':
      while stack[-1] != '(':
        postfix = postfix + stack[-1]
        stack = stack[:-1] 
      stack = stack[:-1]

    elif character in symbols:
      while stack and symbols.get(character, 0) <= symbols.get(stack[-1], 0):
        postfix, stack = postfix + stack[-1], stack[:-1]
      stack = stack + character

    else:
      postfix = postfix + character

  while stack:
    postfix, stack = postfix + stack[-1], stack[:-1]

  return postfix

# ===================================== Thompsons construction Algorithm =====================================
class state:
  label, edge1, edge2 = None, None, None

class nfa:
  initial, accept = None, None

  def __init__(self, initial, accept):
    self.initial, self.accept = initial, accept

def re_to_nfa(postfix):
  nfa_stack = []

  for character in postfix:
    if character == '*':
      nfa_temp = nfa_stack.pop()
      initial, accept = state(), state()
      initial.edge1, initial.edge2 = nfa_temp.initial, accept
      nfa_temp.accept.edge1, nfa_temp.accept.edge2 = nfa_temp.initial, accept
      nfa_stack.append(nfa(initial, accept))

    elif character == '+':
      nfa_temp = nfa_stack.pop()
      accept, initial = state(), state()
      initial.edge1 = nfa_temp.initial
      nfa_temp.accept.edge1, nfa_temp.accept.edge2 = nfa_temp.initial, accept
      nfa_stack.append(nfa(initial, accept))

    elif character == '?':
      nfa_temp = nfa_stack.pop()
      accept, initial = state(), state()
      initial.edge1, initial.edge2 = nfa_temp.initial, accept
      nfa_temp.accept.edge1 = accept
      nfa_stack.append(nfa(initial, accept))

    elif character == '.':
      nfa2, nfa_temp = nfa_stack.pop(), nfa_stack.pop()
      nfa_temp.accept.edge1 = nfa2.initial
      nfa_stack.append(nfa(nfa_temp.initial, nfa2.accept))

    elif character == '|':
      nfa2, nfa_temp = nfa_stack.pop(), nfa_stack.pop()
      initial = state()
      initial.edge1, initial.edge2 = nfa_temp.initial, nfa2.initial
      accept = state()
      nfa_temp.accept.edge1, nfa2.accept.edge1 = accept, accept
      nfa_stack.append(nfa(initial, accept))

    else:
      accept, initial = state(), state()
      initial.label, initial.edge1 = character, accept
      nfa_stack.append(nfa(initial, accept))

  return nfa_stack.pop()

# ===================================== Helper function =====================================
# Returns set of states that can be reached from state following e arrows 
# The main idea is to follow all the e arrows from the current state and add them to the set of states
def epsilon_reach(state):
  states = set()
  states.add(state)

  if state.label is None:
    if state.edge1 is not None:
      states |= epsilon_reach(state.edge1)

    if state.edge2 is not None:
      states |= epsilon_reach(state.edge2)

  return states

# ===================================== Match Function =====================================
def match(regex, string):
  postfix = shunt(regex)    # Convert infix to postfix
  nfa = re_to_nfa(postfix)  # Convert postfix to NFA

  current_states = set()    # Set of states that we are currently in
  next_states = set()       # Set of states we can reach to

  current_states |= epsilon_reach(nfa.initial)  # Add initial state to current states

  for s in string:  
    for character in current_states:
      if character.label == s:
        next_states |= epsilon_reach(character.edge1)   # Add states that can be reached from current states using s

    current_states = next_states    # Update current states
    next_states = set()             # Reset next states

  m = nfa.accept in current_states
  if m:
    msg = "Yayy! The string is in the language generated by the regex!🎉"
  else:
    msg = "Ahh! The string is not in the language generated by the regex!😢"
  return msg

# ===================================== Testcases =====================================
# regex = "(0|1)*.0.0.1.(0|1)*"
# regex = "((0|1))*"
# regex = "((0.1)|(1.0))"
# strings = ["", "11", "0100", "0000", "0001", "0", "1", "101010", "01", "10"]

# print("Given regex:", regex)
# for s in strings:
#   print("Given string:", s)
#   print("Matched:", match(regex, s))
#   print("====================================")

# ===================================== Usability  =====================================
def check_valid_regex_format(regex):
  valid = True
  for character in regex:
    if character not in ['0', '1', '(', ')', '*', '+', '?', '.', '|']:
      valid = False
      print("Invalid regex format. Please use the following characters: 0, 1, (, ), *, +, ?, ., |")
      break
  return valid

def main():
  print("Welcome to the Regex matcher!")
  choice = input("Do you want to enter a regex? (y/n): ")
  choice = choice.lower()
  if choice != 'y' and choice != 'n':
    print("Invalid choice. Bye!")
    return
  while choice == 'y':
    regex = input("Enter the regex: ")
    if check_valid_regex_format(regex):
      string = input("Enter the string: ")
      print(match(regex, string))
      choice2 = input("Do you want to enter another string? (y/n): ")
      choice2 = choice2.lower()
      if choice2 != 'y' and choice2 != 'n':
        print("Invalid choice. Bye!")
        return
      while choice2 == 'y':
        string = input("Enter the string: ")
        print("Is it a match?:", match(regex, string))
        choice2 = input("Do you want to enter another string? (y/n): ")
        choice2 = choice2.lower()
        if choice2 != 'y' and choice2 != 'n':
          print("Invalid choice. Bye!")
          return
    choice = input("Do you want to enter another regex? (y/n): ")
    choice = choice.lower()
    if choice != 'y' and choice != 'n':
      print("Invalid choice. Bye!")
      return
  print("Goodbye!👋")

main()
  


