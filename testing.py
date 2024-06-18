import pygraphviz as pgv
import main
import example

def draw_fa(states, alphabet, transitions, start_state, accept_states, filename='fa.png'):
    graph = pgv.AGraph(directed=True)
    for state in states:
        shape = 'doublecircle' if state in accept_states else 'circle'
        graph.add_node(state, shape=shape)
    
    for from_state, symbol_dict in transitions.items():
        for symbol, to_states in symbol_dict.items():
            for to_state in to_states:
                graph.add_edge(from_state, to_state, label=symbol)

    graph.add_node(start_state, shape='circle', color='red')  # Highlight start state
    graph.layout(prog='dot')
    graph.draw(filename)
