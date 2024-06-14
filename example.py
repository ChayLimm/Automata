# b. Test if a FA is Deterministic or Non-deterministic:

def is_deterministic(transitions):
    for state in transitions:
        for symbol in transitions[state]:
            if len(transitions[state][symbol]) > 1:
                return False
    return True
# c. Test if a String is Accepted by a FA:

def accepts_string(fa, string):
    current_state = fa.start_state
    for symbol in string:
        if symbol in fa.transitions[current_state]:
            current_state = fa.transitions[current_state][symbol][0]
        else:
            return False
    return current_state in fa.accept_states
# d. Construct an Equivalent DFA from an NFA:

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
# e. Minimize a DFA:

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