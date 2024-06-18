class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

def is_deterministic(transitions):
    for state in transitions:
        for symbol in transitions[state]:
            if len(transitions[state][symbol]) > 1:
                return False
    return True

def accepts_string(fa, string):
    current_state = fa.start_state
    for symbol in string:
        if symbol in fa.transitions[current_state]:
            current_state = fa.transitions[current_state][symbol][0]
        else:
            return False
    return current_state in fa.accept_states

def nfa_to_dfa(nfa):
    def union(*sets):
        result = set()
        for s in sets:
            result |= s
        return result

    dfa_transitions = {}
    dfa_start_state = frozenset([nfa.start_state])
    dfa_states = {dfa_start_state}
    dfa_accept_states = set()

    unmarked_states = [dfa_start_state]

    while unmarked_states:
        current_states = unmarked_states.pop()
        for symbol in nfa.alphabet:
            new_state = frozenset(union(*[set(nfa.transitions[state].get(symbol, [])) for state in current_states]))
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
                if len(next_group) > 1:
                    partition.remove(group)
                    partition.append({state for state in group if dfa.transitions[state].get(symbol) == next(next(iter(next_group)))})
                    partition.append({state for state in group if dfa.transitions[state].get(symbol) != next(next(iter(next_group)))})
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
            next_state = min(dfa.transitions[state].get(symbol) for state in group if symbol in dfa.transitions[state])
            min_dfa_transitions[min_state] = {symbol: next_state}

    return FiniteAutomaton(
        states=min_dfa_states,
        alphabet=dfa.alphabet,
        transitions=min_dfa_transitions,
        start_state=min(dfa.start_state),
        accept_states=min_dfa_accept_states
    )

def test_is_deterministic():
    dfa_transitions = {
        'q0': {'a': ['q1'], 'b': ['q0']},
        'q1': {'a': ['q1'], 'b': ['q2']},
        'q2': {'a': ['q2'], 'b': ['q2']}
    }
    nfa_transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q2']},
        'q2': {'a': ['q2']}
    }

    dfa = FiniteAutomaton(states={'q0', 'q1', 'q2'}, alphabet={'a', 'b'}, transitions=dfa_transitions, start_state='q0', accept_states={'q2'})
    nfa = FiniteAutomaton(states={'q0', 'q1', 'q2'}, alphabet={'a', 'b'}, transitions=nfa_transitions, start_state='q0', accept_states={'q2'})

    assert is_deterministic(dfa.transitions) == True
    assert is_deterministic(nfa.transitions) == False
    print("is_deterministic tests passed")

def test_accepts_string():
    dfa_transitions = {
        'q0': {'a': ['q1'], 'b': ['q0']},
        'q1': {'a': ['q1'], 'b': ['q2']},
        'q2': {'a': ['q2'], 'b': ['q2']}
    }

    dfa = FiniteAutomaton(states={'q0', 'q1', 'q2'}, alphabet={'a', 'b'}, transitions=dfa_transitions, start_state='q0', accept_states={'q2'})

    assert accepts_string(dfa, "aab") == True
    assert accepts_string(dfa, "aaa") == False
    print("accepts_string tests passed")

def test_nfa_to_dfa():
    nfa_transitions = {
        'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
        'q1': {'b': ['q2']},
        'q2': {'a': ['q2']}
    }

    nfa = FiniteAutomaton(states={'q0', 'q1', 'q2'}, alphabet={'a', 'b'}, transitions=nfa_transitions, start_state='q0', accept_states={'q2'})

    dfa = nfa_to_dfa(nfa)

    assert is_deterministic(dfa.transitions) == True
    assert accepts_string(dfa, "aab") == True
    assert accepts_string(dfa, "aaa") == False
    print("nfa_to_dfa tests passed")

def test_minimize_dfa():
    dfa_transitions = {
        'q0': {'a': 'q1', 'b': 'q2'},
        'q1': {'a': 'q0', 'b': 'q3'},
        'q2': {'a': 'q3', 'b': 'q0'},
        'q3': {'a': 'q2', 'b': 'q1'}
    }

    dfa = FiniteAutomaton(states={'q0', 'q1', 'q2', 'q3'}, alphabet={'a', 'b'}, transitions=dfa_transitions, start_state='q0', accept_states={'q0'})

    min_dfa = minimize_dfa(dfa)

    assert is_deterministic(min_dfa.transitions) == True
    print("minimize_dfa tests passed")

if __name__ == "__main__":
    test_is_deterministic()
    test_accepts_string()
    test_nfa_to_dfa()
    test_minimize_dfa()
