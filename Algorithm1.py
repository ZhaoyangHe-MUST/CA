import DFA
class HA:
    def __init__(self, states_Xh, attack_events, transition_function_ha, initial_state_ha):
        self.states_Xh = states_Xh
        self.attack_events = attack_events
        self.transition_function_ha = transition_function_ha
        self.initial_state_ha = initial_state_ha
    
           



# Example:
states = {'0', '1', '2', '3', '4'}#set of states of a supervisor realization
events = {'a01', 'a12', 'a23', 'a30', 'b24', 'b45', 'b56', 'b62', 'c37', 'c47'}#set of events of a supervisor realization
transition_function = {
    ('0', 'a01', '0'),
    ('0', 'b56', '0'),
    ('0', 'a12', '1'),
    ('1', 'a01', '1'),
    ('1', 'b56', '1'),
    ('1', 'a23', '2'),
    ('1', 'b24', '3'),
    ('2', 'a01', '2'),
    ('2', 'b56', '2'),
    ('2', 'a30', '0'),
    ('3', 'a01', '3'),
    ('3', 'b56', '3'),
    ('3', 'b45', '4'),
    ('4', 'a01', '4'),
    ('4', 'b56', '4'),
    ('4', 'b62', '1')
}#transitions of a supervisor realization
initial_state = '0'#initial state of a supervisor realization

H = DFA.DFA(states, events, transition_function, initial_state)#construct a supervisor realization H

# Test
""" print("This is a supervisor realization H:")
print("The set of states:", H.states)
print("The set of events:", H.events)
print("Transition function f:", H.transition_function)
print("initial state:", H.initial_state) """
Sigma_uo={'a01', 'b56'}#set of unobservable events
Sigma_vs={'a23', 'b24', 'c37', 'c47'}#set of vulnerable sensor events
Sigma_va={'c37', 'c47'}#set of vulnerable actuator events
#----------------------------------------------------------------------------
#Algorithm 1: Construction of a corrupted supervisor under acceptable attacks
#----------------------------------------------------------------------------
#Input:  a supervisor realization H, 
#        active event set Gamma_H(x_h) at each x_h\in X_h, 
#        vulnerable sensor event set Sigma_vs, 
#        and vulnerable actuator event set Sigma_va
#Output: H_a=(X_h, \Sigma\times\AT\times(\Sigma\cup{\varepsilon}), f_{h_{a}}, x_{0,h}), 
#        a corrupted supervisor under acceptable attacks

#X_h:
states_Xh=H.states

#x_{0,h}:
initial_state_ha=H.initial_state

#\Sigma\times\AT\times(\Sigma\cup{\varepsilon}):
attack_events=set()
for event in H.events:
    attack_events.add((event, 'na', 'varepsilon'))
    attack_events.add((event, 'ae', 'varepsilon'))
    attack_events.add((event, 'sr', 'varepsilon'))
    attack_events.add((event, 'as', 'varepsilon'))
    for reading in H.events:
        attack_events.add((event, 'na', reading))
        attack_events.add((event, 'ae', reading))
        attack_events.add((event, 'sr', reading))
        attack_events.add((event, 'as', reading))
        
# print("attack_events:", attack_events)


#f_{h_{a}}:
transition_function_ha=set()
#Lines 1--4:
for xh in states_Xh:
    for event in H.events:
        if event in H.active_events(xh):
            transition_function_ha.add((xh, (event, 'na', event), H.current_state(xh, event)))

def pre_active_events_Ha(x, tfs):#obtain \Gamma_{H_{a}}(x) 
    pre_ae_set=set()
    for tf in tfs:
        if tf[0]==x:
           pre_ae_set.add(tf[1]) 
    return pre_ae_set

def current_state_Ha(x, ae, tfs):#obtain the current state in H_{a} after an attack event occurs ae at x
    cstate = ''
    for tf in tfs:
        if tf[0]==x and tf[1]==ae:
            cstate = tf[2]
    return cstate

#Lines 5--18:
for event in Sigma_vs:
    for xh in states_Xh:
        if (event, 'na', event) in pre_active_events_Ha(xh, transition_function_ha):
            if (event, 'sr', 'varepsilon') not in pre_active_events_Ha(xh, transition_function_ha):
                transition_function_ha.add((xh, (event, 'sr', 'varepsilon'), xh))
            for reading in Sigma_vs-{event}:
                """ print("sigma:", event)
                print("r(sigma):", reading)
                print("xh:", xh)
                print("pre:", pre_active_events_Ha(xh, transition_function_ha)) """
                if (reading, 'na', reading) in pre_active_events_Ha(xh, transition_function_ha) and (event, 'sr', reading) not in pre_active_events_Ha(xh, transition_function_ha):
                    #print("addsr:", (xh, (event, 'sr', reading), current_state_Ha(xh, (reading, 'na', reading), transition_function_ha)))
                    transition_function_ha.add((xh, (event, 'sr', reading), current_state_Ha(xh, (reading, 'na', reading), transition_function_ha)))
                    
        
        if event in Sigma_va and (event, 'na', event) not in pre_active_events_Ha(xh, transition_function_ha):
            if (event, 'as', 'varepsilon') not in pre_active_events_Ha(xh, transition_function_ha):
                transition_function_ha.add((xh, (event, 'as', 'varepsilon'), xh))
            for reading in Sigma_vs-{event}:
                if (reading, 'na', reading) in pre_active_events_Ha(xh, transition_function_ha) and (event, 'as', reading) not in pre_active_events_Ha(xh, transition_function_ha):
                    transition_function_ha.add((xh, (event, 'as', reading), current_state_Ha(xh, (reading, 'na', reading), transition_function_ha)))    

Ha = HA(states_Xh, attack_events, transition_function_ha, initial_state_ha)#construct a corrupted supervisor H_{a}

#print H_{a} for test
def print_Ha():
    print("This is a corrupted supervisor H_a:")
    print("     The set of states:", Ha.states_Xh)
    #print("The set of attack events:", Ha.attack_events)
    print("     Transition function f_{h_{a}}:")
    for xh in states_Xh:
        print("     state", xh, ":")
        for tf in transition_function_ha:
            if tf[0]==xh:
                print("     ", tf)
    print("     initial state:", initial_state_ha)

if __name__=='__main__':
    # Test
    print_Ha()
