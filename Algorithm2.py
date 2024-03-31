from Algorithm1 import H

           



# Example:

Sigma_uo={'a'}
Sigma_o={'b', 'c', 'd', 'e', 'f', 'g'}
Sigma_vs={'c', 'd', 'e'}
Sigma_va={'d'}

theta=[('a', 'na', 'a'), ('b', 'na', 'b'), ('c', 'sr', 'e'), ('d', 'as', 'varepsilon')]

""" lambda_theta=[item[0] for item in theta]
nu_theta=[item[2] for item in theta]

Po_lambda_theta=[sigma for sigma in lambda_theta if sigma in Sigma_o]
Po_nu_theta=[sigma for sigma in nu_theta if sigma in Sigma_o]

print("", lambda_theta, nu_theta)

print("", Po_lambda_theta, Po_nu_theta) """
#lambda_theta: project theta to a string of events
def lambda_theta(theta):
    return [item[0] for item in theta]

#nu_theta: project theta to a string of replaced readings
def nu_theta(theta):
    return [item[2] for item in theta]

#projection P_o
def projection(string, Sigma):
    return [sigma for sigma in string if sigma in Sigma]

#print("lambda nu:", projection(lambda_theta(theta), Sigma_o), projection(nu_theta(theta), Sigma_o))

#control command S(s)
def control_command(string, dfa):
    current_state=dfa.initial_state
    for event in string:
        if event!='varepsilon':
            current_state=dfa.current_state(current_state, event)
        if event=='varepsilon':
            current_state=current_state
    #print("current state in S", current_state)
    return dfa.active_events(current_state)

#print("lambda_theta", control_command(nu_theta, H))

#----------------------------------------------------------------------------
#Algorithm 2: Synthesis of attacks
#----------------------------------------------------------------------------
#Input:  A feasible attack string \theta and a supervisor S
#Output: A_sr and A_ae, synthesized SR-attacks and AEattacks
A_sr=[]
A_ae=[]
i=0
while i < len(theta):
    if theta[i][0] in Sigma_va and theta[i][1]=='ae' and theta[i][2] not in control_command(theta[:i], H):
        A_ae.append("A_ae("+''.join(projection(nu_theta(theta[:i]), Sigma_o))+")=S("+''.join(projection(nu_theta(theta[:i]), Sigma_o))+")∪{"+''.join(theta[i][0])+"}")
        #print("A_ae(", projection(nu_theta(theta[:i]), Sigma_o),")=S(", projection(nu_theta(theta[:i]), Sigma_o),")\cup{", theta[i][0],"}")
    if theta[i][0] in Sigma_vs and theta[i][1]=='sr' and theta[i][2] in Sigma_vs|{'varepsilon'}-{theta[i][0]}:
        A_sr.append("A_sr("+''.join(projection(lambda_theta(theta[:i]), Sigma_o))+","+''.join(theta[i][0])+")={"+''.join(theta[i][2])+"}")
        #print("A_sr(", projection(lambda_theta(theta[:i]), Sigma_o),",", theta[i][0],")={", theta[i][2],"}")
    if theta[i][0] in Sigma_va and theta[i][1]=='as' and theta[i][2] not in control_command(theta[:i], H) and theta[i][2] in Sigma_vs|{'varepsilon'}-{theta[i][0]}:
        A_ae.append("A_ae("+''.join(projection(nu_theta(theta[:i]), Sigma_o))+")=S("+''.join(projection(nu_theta(theta[:i]), Sigma_o))+")∪{"+''.join(theta[i][0])+"}")
        A_sr.append("A_sr("+''.join(projection(lambda_theta(theta[:i]), Sigma_o))+","+''.join(theta[i][0])+")={"+''.join(theta[i][2])+"}")
        #print("A_ae(", projection(nu_theta(theta[:i]), Sigma_o),")=S(", projection(nu_theta(theta[:i]), Sigma_o),")\cup{", theta[i][0],"}")
        #print("A_sr(", projection(lambda_theta(theta[:i]), Sigma_o),",", theta[i][0],")={", theta[i][2],"}")
    i=i+1
print("Asr:", A_sr)
print("Aae:", A_ae)
