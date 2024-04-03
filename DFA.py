class DFA:
    def __init__(self, states, events, transition_function, initial_state):
        self.states = states
        self.events = events
        self.transition_function = transition_function
        self.initial_state = initial_state
    def active_events(self, state):
        active_event_set=set()
        for tf in self.transition_function:
            if tf[0]==state:
                active_event_set.add(tf[1]) 
        #print("", active_event_set) 
        return active_event_set
    def current_state(self, state, event):
        cstate = ''
        for tf in self.transition_function:
            if tf[0]==state and tf[1]==event:
                cstate = tf[2]
        return cstate




# Example:

states = {'0', '1', '2', '3', '4', '5', '6', '7'}#set of states
events = {'a01', 'a12', 'a23', 'a30', 'b24', 'b45', 'b56', 'b62', 'c37', 'c47'}#set of events
transition_function = {
    ('0', 'a01', '1'),
    ('1', 'a12', '2'),
    ('2', 'a23', '3'),
    ('3', 'a30', '0'),
    ('3', 'c37', '7'),
    ('2', 'b24', '4'),
    ('4', 'b45', '5'),
    ('4', 'c47', '7'),
    ('5', 'b56', '6'),
    ('6', 'b62', '2')
}#transitions
initial_state = '0'#initial state

#build a DFA
G = DFA(states, events, transition_function, initial_state)

#print DFA G for test
def print_G():
    print("This is a plant G:")
    print("The set of states:", G.states)
    print("The set of events:", G.events)
    print("Transition function f:",G.transition_function)
    print("initial state:", G.initial_state)


if __name__=='__main__':
    # Test
    print_G()
