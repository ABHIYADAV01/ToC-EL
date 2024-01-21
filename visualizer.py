import graphviz as gv


def visualize_dfa(dfa):
    """Visualizes a DFA using Graphviz.

    Args:
        dfa: A dictionary representing the DFA, with the following structure:
            - 'states': A list of states.
            - 'alphabet': A list of input symbols.
            - 'transitions': A dictionary of transitions, where keys are tuples
              of (state, input symbol), and values are the next states.
            - 'start_state': The start state.
            - 'accept_states': A list of accepting states.

    Returns:
        A Graphviz object representing the DFA.
    """

    graph = gv.Digraph(format='png')  # Choose a suitable output format

    # Add nodes for states, highlighting accepting states
    for state in dfa['states']:
        shape = 'doublecircle' if state in dfa['accept_states'] else 'circle'
        graph.node(state, shape=shape)

    # Add edges for transitions
    for (state, symbol), next_state in dfa['transitions'].items():
        # Special handling for empty string
        label = f"{symbol}" if symbol != 'λ' else 'ε'
        graph.edge(state, next_state, label=label)

    # Highlight the start state
    graph.node(dfa['start_state'], shape='circle',
               style='filled', fillcolor='lightblue')

    return graph


def visualize_dfa_path(dfa, s):
    """Visualizes a DFA path for a given string using Graphviz.

    Args:
        dfa: A dictionary representing the DFA, with the following structure:
            - 'states': A list of states.
            - 'alphabet': A list of input symbols.
            - 'transitions': A dictionary of transitions, where keys are tuples
              of (state, input symbol), and values are the next states.
            - 'start_state': The start state.
            - 'accept_states': A list of accepting states.
        s: The input string to check.

    Returns:
        A Graphviz object representing the DFA path. 
    """

    accepted = True

    # Create a DFA path for the string
    current_state = dfa['start_state']
    path = [current_state]
    for symbol in s:
        next_state = dfa['transitions'].get((current_state, symbol), None)
        if next_state is None:
            accepted = False
            break
        current_state = next_state
        path.append(current_state)

    accepted = accepted and current_state in dfa['accept_states']
    accepted_color = 'green' if accepted else 'red'

    # Create a DFA path graph
    graph = gv.Digraph(format='png')

    # Add the string 's' at the top of the image
    graph.node('s', label=s, shape='none', fontsize='20', fontweight='bold')

    # Highlight the start state
    graph.node(dfa['start_state'], shape='circle',
               style='filled', fillcolor='lightblue')

    # Add nodes for states, highlighting accepting states
    for state in dfa['states']:
        shape = 'doublecircle' if state in dfa['accept_states'] else 'circle'
        if state == path[-1]:  # last state in the path
            graph.node(state, shape=shape, style='filled',
                       fillcolor=accepted_color)
        else:
            graph.node(state, shape=shape)

    # Add edges for transitions
    for (state, symbol), next_state in dfa['transitions'].items():
        # Special handling for empty string
        label = f"{symbol}" if symbol != 'λ' else 'ε'
        graph.edge(state, next_state, label=label, color=accepted_color if (
            state, symbol) in zip(path, s) else 'black')  # Highlight the path

    return graph, accepted, path


def visualize_nfa(nfa):
    """Visualizes an NFA using Graphviz.

    Args:
        nfa: A dictionary representing the NFA, with the following structure:
            - 'states': A list of states.
            - 'alphabet': A list of input symbols.
            - 'transitions': A dictionary of transitions, where keys are tuples
              of (state, input symbol), and values are lists of next states.
            - 'start_state': The start state.
            - 'accept_states': A list of accepting states.

    Returns:
        A Graphviz object representing the NFA.
    """

    graph = gv.Digraph(format='png')  # Choose a suitable output format

    # Add nodes for states, highlighting accepting states
    for state in nfa['states']:
        shape = 'doublecircle' if state in nfa['accept_states'] else 'circle'
        graph.node(state, shape=shape)

    # Add edges for transitions, handling multiple next states
    for (state, symbol), next_states in nfa['transitions'].items():
        # Special handling for empty string
        label = f"{symbol}" if symbol != 'λ' else 'ε'
        for next_state in next_states:
            # Create edges for all next states
            graph.edge(state, next_state, label=label)

    # Highlight the start state
    graph.node(nfa['start_state'], shape='circle',
               style='filled', fillcolor='lightblue')

    return graph


def calculate_epsilon_closures(nfa):

    epsilon_closures = {}
    for state in nfa['states']:
        epsilon_closures[state] = set()
        visited = set()
        stack = [state]
        while stack:
            current_state = stack.pop()
            if current_state in visited:
                continue
            visited.add(current_state)
            epsilon_closures[state].add(current_state)
            for next_state in nfa['transitions'].get((current_state, 'λ'), []):
                stack.append(next_state)

    return epsilon_closures


def visualize_e_nfa(nfa):
    """Visualizes an Epsilon Closure NFA using Graphviz.

    Args:
        nfa: A dictionary representing the NFA, with the following structure:
            - 'states': A list of states.
            - 'alphabet': A list of input symbols.
            - 'transitions': A dictionary of transitions, where keys are tuples
              of (state, input symbol), and values are lists of next states.
            - 'start_state': The start state.
            - 'accept_states': A list of accepting states.
            - 'epsilon_closures': A dictionary mapping each state to its epsilon closure
              (a set of states reachable through epsilon transitions).

    Returns:
        A Graphviz object representing the NFA.
    """

    graph = gv.Digraph(format='png')  # Choose a suitable output format

    # Add nodes for states, highlighting accepting states
    for state in nfa['states']:
        shape = 'doublecircle' if state in nfa['accept_states'] else 'circle'
        graph.node(state, shape=shape)

    # Add edges for transitions, handling multiple next states
    for (state, symbol), next_states in nfa['transitions'].items():
        # Special handling for empty string
        label = f"{symbol}" if symbol != 'λ' else 'ε'
        for next_state in next_states:
            # Create edges for all next states
            graph.edge(state, next_state, label=label)

    # Highlight the start state
    graph.node(nfa['start_state'], shape='circle',
               style='filled', fillcolor='lightblue')

    return graph


if __name__ == '__main__':

    dfa = {
        'states': ['q0', 'q1', 'q2'],
        'alphabet': ['0', '1'],
        'transitions': {
            ('q0', '0'): 'q0',
            ('q0', '1'): 'q1',
            ('q1', '0'): 'q2',
            ('q1', '1'): 'q0',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        },
        'start_state': 'q0',
        'accept_states': ['q2']
    }

    graph = visualize_dfa(dfa)
    # Render and save the diagram
    graph.render('images/dfa_visualization', cleanup=True)

    nfa = {
        'states': ['q0', 'q1', 'q2'],
        'alphabet': ['0', '1'],
        'transitions': {
            ('q0', '0'): ['q0', 'q1'],  # Multiple next states for '0'
            ('q0', '1'): ['q1'],
            ('q1', '0'): ['q2'],
            ('q1', '1'): ['q0'],
            ('q2', '0'): [],  # No transitions for '0' from q2
            ('q2', '1'): ['q2']
        },
        'start_state': 'q0',
        'accept_states': ['q2']
    }

    graph = visualize_nfa(nfa)
    # Render and save the diagram
    graph.render('images/nfa_visualization', cleanup=True)

    e_nfa = {
        'states': ['q0', 'q1', 'q2', 'q3'],
        'alphabet': ['a', 'b'],
        'transitions': {
            ('q0', 'λ'): ['q1', 'q3'],
            ('q1', 'a'): ['q2'],
            ('q2', 'b'): ['q0'],
            ('q3', 'b'): ['q2']
        },
        'start_state': 'q0',
        'accept_states': ['q2']
    }

    # Calculate epsilon closures (optional, if not already provided in e_nfa)
    e_nfa['epsilon_closures'] = calculate_epsilon_closures(e_nfa)
    print(f"Epsilon closures: {e_nfa['epsilon_closures']}")

    graph = visualize_e_nfa(e_nfa)
    graph.render('images/epsilon_e_nfa_visualization', cleanup=True)

    s = "1000101"
    graph, accepted, path = visualize_dfa_path(dfa, s)
    print(f"String: {s}, Accepted: {accepted}, Path: {path}")
    graph.render('images/dfa_path_visualization1', cleanup=True)

    s = "0010111"
    graph, accepted, path = visualize_dfa_path(dfa, s)
    print(f"String: {s}, Accepted: {accepted}, Path: {path}")
    graph.render('images/dfa_path_visualization2', cleanup=True)
