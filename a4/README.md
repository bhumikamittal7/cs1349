We will be implementing the membership checkig of an arbitrary string with respect to an input language defined by its regular expression.

- _Input_: A regular expression R over $\{0, 1\}$, and a string $w \in \{0, 1\}^*$
- _Output_: Accept if $w \in \mathcal{L}(R)$, and reject otherwise.

### Assumptions
- The input regular expression is syntactically correct.
- The input regular expression is in infix notation.
- The input regular expression is over $\{0, 1\}$.
- The input string is over $\{0, 1\}$.

### Main Steps
1. Build an NFA $\mathcal{N}$ such that $\mathcal{L}(N) = \mathcal{L}(R)$
2. Run $\mathcal{N}$ on $w$ to decide its membership

# Implementation
We will be using the two well known algorithms to convert a regular expression to an NFA, namely:
1. Shunting Yard Algorithm
2. Thompson's Construction

The main idea is to first convert the regular expression to postfix notation using the shunting yard algorithm, and then use Thompson's construction to convert the postfix expression to an NFA.

## Shunting Yard Algorithm
The shunting yard algorithm is a method for parsing mathematical expressions specified in infix notation. It can be used to produce output in Reverse Polish notation (RPN) or as an abstract syntax tree (AST). 

Fun fact: The algorithm was invented by Edsger Dijkstra and named the "shunting yard" algorithm because its operation resembles that of a railroad shunting yard.

- _Input_: A regular expression R over {0, 1}
- _Output_: An equivalent regular expression R' in postfix notation
- Steps:
    1. Create an empty stack for operators. Create an empty list for the output.
    2. For each token in the input:
        - If the token is a number, then add it to the output list.
        - If the token is an operator, then:
            - While there is an operator at the top of the stack with greater precedence than the token, pop the operator from the stack and add it to the output list.
            - Push the token onto the stack.
        - If the token is a left parenthesis, then push it onto the stack.
        - If the token is a right parenthesis, then:
            - While the top of the stack is not a left parenthesis, pop the operator from the stack and add it to the output list.
            - Pop the left parenthesis from the stack and discard it.
    3. When there are no more tokens to read, pop all operators from the stack and add them to the output list.

## Thompson's Construction
Thompson's construction is an algorithm for converting a regular expression into an equivalent nondeterministic finite automaton (NFA). The algorithm was introduced by Ken Thompson in 1960.

- _Input_: A regular expression R over {0, 1}
- _Output_: An NFA N such that L(N) = L(R)
- Steps:
    1. Create an empty stack for NFAs.
    2. For each token in the input:
        - If the token is a number, then create an NFA with two states, and add a transition between them labeled with the number. Push the NFA onto the stack.
        - If the token is an operator, then:
            - If the operator is `*`, then pop the NFA from the stack, create a new start state and a new final state, add transitions from the new start state to the old start state and from the old final state to the new final state, and push the new NFA onto the stack.
            - If the operator is `|`, then pop two NFAs from the stack, create a new start state and a new final state, add transitions from the new start state to the old start states and from the old final states to the new final state, and push the new NFA onto the stack.
            - If the operator is `.` (concatenation), then pop two NFAs from the stack, add a transition from the old final state of the first NFA to the old start state of the second NFA, and push the new NFA onto the stack.
    3. The NFA is the only NFA left on the stack.

## Other Functions - Epsilon Reach
This function calculates the set of states reachable from a given state via epsilon transitions. It utilizes recursive traversal to handle epsilon transitions.

# References
  - https://en.wikipedia.org/wiki/Shunting_yard_algorithm
  - https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF
  - https://en.wikipedia.org/wiki/Thompson%27s_construction
  - https://swtch.com/~rsc/regexp/regexp1.html