import pygraphviz as pgv
from collections import defaultdict

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

# Function to check if an FA is deterministic
def is_deterministic(transitions):
    for state in transitions:
        for symbol in transitions[state]:
            if len(transitions[state][symbol]) > 1:
                return False
    return True

# Function to check if a string is accepted by a FA
def accepts_string(fa, string):
    current_state = fa.start_state
    for symbol in string:
        if symbol in fa.transitions[current_state]:
            current_state = fa.transitions[current_state][symbol][0]
        else:
            return False
    return current_state in fa.accept_states

# Function to convert an NFA to a DFA
def nfa_to_dfa(nfa):
    dfa_transitions = {}
    dfa_start_state = frozenset([nfa.start_state])
    dfa_states = {dfa_start_state}
    dfa_accept_states = set()

    unmarked_states = [dfa_start_state]

    while unmarked_states:
        current_states = unmarked_states.pop()
        for symbol in nfa.alphabet:
            new_state = frozenset(union(*[nfa.transitions[state].get(symbol, []) for state in current_states]))
            if new_state:
                if new_state not in dfa_states:
                    dfa_states.add(new_state)
                    unmarked_states.append(new_state)
                dfa_transitions.setdefault(current_states, {})[symbol] = new_state
                if any(state in nfa.accept_states for state in new_state):
                    dfa_accept_states.add(new_state)

    return FiniteAutomaton(
        states=dfa_states,
        alphabet=nfa.alphabet,
        transitions=dfa_transitions,
        start_state=dfa_start_state,
        accept_states=dfa_accept_states
    )

# Function to minimize a DFA
def minimize_dfa(dfa):
    partition = [{state for state in dfa.states if state in dfa.accept_states}, {state for state in dfa.states if state not in dfa.accept_states}]
    new_partition = None

    while new_partition != partition:
        new_partition = partition.copy()
        for group in partition:
            for symbol in dfa.alphabet:
                next_group = set()
                for state in group:
                    next_group.add(dfa.transitions[state].get(symbol, None))
                if len(next_group) == 1:
                    next_group = next_group.pop()
                    partition.remove(group)
                    partition.append({state for state in dfa.states if dfa.transitions[state].get(symbol) == next_group})
                    break

    min_dfa_states = set()
    min_dfa_accept_states = set()
    min_dfa_transitions = {}

    for group in partition:
        min_state = min(group)
        min_dfa_states.add(min_state)
        if any(state in dfa.accept_states for state in group):
            min_dfa_accept_states.add(min_state)
        for symbol in dfa.alphabet:
            next_state = min(dfa.transitions[state].get(symbol) for state in group)
            min_dfa_transitions[min_state] = {symbol: next_state}

    return FiniteAutomaton(
        states=min_dfa_states,
        alphabet=dfa.alphabet,
        transitions=min_dfa_transitions,
        start_state=min_dfa_states.intersection(dfa.start_state).pop(),
        accept_states=min_dfa_accept_states
    )

# Function to visualize the FA using Graphviz
def visualize_fa(fa, filename='fa'):
    graph = pgv.AGraph(directed=True)

    for state in fa.states:
        if state in fa.accept_states:
            graph.add_node(state, shape='doublecircle')
        else:
            graph.add_node(state, shape='circle')
    
    for state in fa.transitions:
        for symbol in fa.transitions[state]:
            for next_state in fa.transitions[state][symbol]:
                graph.add_edge(state, next_state, label=symbol)
    
    graph.add_node('', shape='none')
    graph.add_edge('', fa.start_state)

    graph.layout(prog='dot')
    graph.draw(f'{filename}.png')

# Example usage
if __name__ == "__main__":
    nfa = FiniteAutomaton(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
            'q1': {'b': ['q2']},
            'q2': {}
        },
        start_state='q0',
        accept_states={'q2'}
    )

    # Check if NFA is deterministic
    print("Is the NFA deterministic?", is_deterministic(nfa.transitions))

    # Convert NFA to DFA
    dfa = nfa_to_dfa(nfa)
    print("Converted DFA transitions:", dfa.transitions)

    # Minimize DFA
    min_dfa = minimize_dfa(dfa)
    print("Minimized DFA transitions:", min_dfa.transitions)

    # Check if DFA accepts a string
    test_string = 'aab'
    print(f"Does the DFA accept '{test_string}'?", accepts_string(dfa, test_string))

    # Visualize the NFA and DFA
    visualize_fa(nfa, filename='nfa')
    visualize_fa(dfa, filename='dfa')
    visualize_fa(min_dfa, filename='min_dfa')
