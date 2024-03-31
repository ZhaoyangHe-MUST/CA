from DFA import G
from Algorithm1 import Ha, pre_active_events_Ha, current_state_Ha
#import sys
#sys.setrecursionlimit(100000)

class Estimator:
    def __init__(self, states_e, attack_events, transition_function_e, initial_state_e):
        self.states_e = states_e
        self.attack_events = attack_events
        self.transition_function_e = transition_function_e
        self.initial_state_e = initial_state_e

def C_sr(sigma, Cost):
    return Cost[sigma]
def C_ae(sigma, Cost):
    return Cost[sigma]


#Example
Sigma = {'a01', 'a12', 'a23', 'a30', 'b24', 'b45', 'b56', 'b62', 'c47'}#set of events
Sigma_uo={'a01', 'b56'}#set of unobservable events
Sigma_vs={'a23', 'b24', 'c47'}#set of vulnerable sensor events
Sigma_va={'c47'}#set of vulnerable actuator events
X_us={'7'}#unsafe state set
#Resource assumption assignment
c_ir=30
Costvs={'a23': 10, 'b24': 5, 'c47': 10}#resource consumption of SR-attack on event
Costva={'c47' : 15}#resource consumption of AE-attack on event


#Resource consumption of attacks in an attack string
def C(attack_event):
    consumption=0
    if attack_event[0] in Sigma and attack_event[1]=='na':
        consumption+=0
    if attack_event[0] in Sigma_va and attack_event[1]=='ae':
        consumption+=C_ae(attack_event[0], Costva)
    if attack_event[0] in Sigma_vs and attack_event[1]=='sr':
        consumption+=C_sr(attack_event[0], Costvs)
    if attack_event[0] in Sigma_va and attack_event[1]=='as':
        consumption+=C_sr(attack_event[0], Costvs)+C_ae(attack_event[0], Costva)
    return consumption
""" def C(theta):
    consumption=0
    for attack_event in theta:
        if attack_event[0] in Sigma and attack_event[1]=='na':
            consumption+=0
        if attack_event[0] in Sigma_va and attack_event[1]=='ae':
            consumption+=C_ae(attack_event[0], Costva)
        if attack_event[0] in Sigma_vs and attack_event[1]=='sr':
            consumption+=C_sr(attack_event[0], Costvs)
        if attack_event[0] in Sigma_va and attack_event[1]=='as':
            consumption+=C_sr(attack_event[0], Costvs)+C_ae(attack_event[0], Costva)
    return consumption """


#initial
initial_state_e=(G.initial_state, Ha.initial_state_ha, c_ir)
states_e={initial_state_e}
attack_events=Ha.attack_events
transition_function_e=set()
def Get_states_e(state_e):
    for attack_event in attack_events:
        if attack_event[0] in G.active_events(state_e[0]) and attack_event in pre_active_events_Ha(state_e[1], Ha.transition_function_ha) and state_e[2]>= C(attack_event) and attack_event[1] in {'sr', 'as'}:
           current_state_e=(G.current_state(state_e[0], attack_event[0]), current_state_Ha(state_e[1], attack_event, Ha.transition_function_ha), state_e[2]-C(attack_event))
           print("ce1= ", current_state_e)
           if current_state_e in states_e and (state_e, attack_event, current_state_e) not in transition_function_e:
               transition_function_e.add((state_e, attack_event, current_state_e))
           if current_state_e not in states_e:
               states_e.add(current_state_e)
               if (state_e, attack_event, current_state_e) not in transition_function_e:
                   transition_function_e.add((state_e, attack_event, current_state_e))
               Get_states_e(current_state_e)
        if attack_event[0] in G.active_events(state_e[0]) and attack_event in pre_active_events_Ha(state_e[1], Ha.transition_function_ha) and attack_event[1] =='na':
           current_state_e=(G.current_state(state_e[0], attack_event[0]), current_state_Ha(state_e[1], attack_event, Ha.transition_function_ha), state_e[2])
           print("ce2= ", current_state_e)
           if current_state_e in states_e and (state_e, attack_event, current_state_e) not in transition_function_e:
               transition_function_e.add((state_e, attack_event, current_state_e))
           if current_state_e not in states_e:
               states_e.add(current_state_e)
               if (state_e, attack_event, current_state_e) not in transition_function_e:
                    transition_function_e.add((state_e, attack_event, current_state_e))
               Get_states_e(current_state_e)
Get_states_e(initial_state_e)


#Construction of an estimator
E = Estimator(states_e, attack_events, transition_function_e, initial_state_e)

print("This is an estimator with respect to S/G and c_ir:")
print("     The set of states:", E.states_e)
#print("The set of attack events:", Ha.attack_events)
print("     Transition function f_{e}:")
for xe in E.states_e:
    print("     state", xe, ":")
    for tf in transition_function_e:
        if tf[0]==xe:
            print("     ", tf)
print("     initial state:", E.initial_state_e)

#Verification of combined-attackability by an estimator (Theorem 2)
states_e_xus=set()
for xe in E.states_e:
    if xe[0] in X_us:
        states_e_xus.add(xe)
if states_e_xus is None:
    print("The closed-loop system S/G is not combined-attackable!")
else:
    print("The closed-loop system S/G is combined-attackable since there exist states:", states_e_xus)
