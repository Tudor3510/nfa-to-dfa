import pandas as pd

class Automat:
    noStates = 0
    stateMachine = {}
    stateSet = []
    pathSet = []
    startState = ''
    endingStatesNo = 0
    endingStates = []

class DFA(Automat):
    pass

class NFA(Automat):
    pass

nfa = NFA()
dfa = DFA()


# Taking NFA input from User 

reader = open("input.txt", "r")

nfa.stateMachine = {}                                 
nfa.noStates = int(reader.readline())                   #Enter total no. of states
nfa.stateSet = []
for i in reader.readline().strip().split():
    nfa.stateMachine[i] = {}
    if i not in nfa.stateSet:
        nfa.stateSet.append(i)

inputtedTransitionsNo = int(reader.readline().strip())
inputtedTransitions = []
nfa.pathSet = []
for i in range(inputtedTransitionsNo):
    inputtedTransitions.append(i)
    inputtedTransitions[i] = [x for x in reader.readline().strip().split()]

    if inputtedTransitions[i][-1] not in nfa.pathSet:
        nfa.pathSet.append(inputtedTransitions[i][-1])

for i in nfa.stateSet:
    for j in nfa.pathSet:
        nfa.stateMachine[i][j] = []

for i, j, k in inputtedTransitions:
    nfa.stateMachine[i][k].append(j)

nfa.startState = reader.readline().strip()
nfa.endingStatesNo = int(reader.readline().strip())
nfa.endingStates = reader.readline().strip().split()


print("\nnfa.stateMachine :- \n")
print(nfa.stateMachine)                                    #Printing nfa.stateMachine
print("\nPrinting nfa.stateMachine table :- ")
nfa.stateMachine_table = pd.DataFrame(nfa.stateMachine)
print(nfa.stateMachine_table.transpose())


###################################################                 
    
newStates = []                          #holds all the new states created in dfa
dfa.stateMachine = {}                                      #dfa dictionary/table or the output structure we needed
dfa.stateSet = list(nfa.startState)                  #conatins all the states in nfa.stateMachine plus the states created in dfa are also appended further

###################################################

# Computing first row of DFA transition table

dfa.stateMachine[dfa.stateSet[0]] = {}                        #creating a nested dictionary in dfa 
for y in range(len(nfa.pathSet)):

    temp = nfa.stateMachine[dfa.stateSet[0]][nfa.pathSet[y]]
    temp = list(dict.fromkeys(temp))        #stergem duplicatele
    temp.sort()                             #sortam pentru a nu avea probleme de genul ab != ba
    s = "".join(temp)                       #facem un singur string cu elementele din lista

    var = "".join(temp)   #facem un singur string cu elementele din lista continuta in nfa.stateMachine-ul startState si pathSet-ul respectiv
    dfa.stateMachine[dfa.stateSet[0]][nfa.pathSet[y]] = var            #assigning the state in DFA table
    if var not in dfa.stateSet and var != '':                         #if the state is newly created 
        newStates.append(var)                  #then append it to the new_states_list
        dfa.stateSet.append(var)                        #as well as to the keys_list which contains all the states
        
###################################################
 
# Computing the other rows of DFA transition table

while len(newStates) != 0:                     #consition is true only if the new_states_list is not empty
    dfa.stateMachine[newStates[0]] = {}                     #taking the first element of the new_states_list and examining it

    for _ in range(len(newStates[0])):
        for i in range(len(nfa.pathSet)):
            temp = []                                #creating a temporay list
            for j in range(len(newStates[0])):
                temp += nfa.stateMachine[newStates[0][j]][nfa.pathSet[i]]  #taking the union of the states

            temp = list(dict.fromkeys(temp))        #stergem duplicatele
            temp.sort()                             #sortam pentru a nu avea probleme de genul ab != ba
            s = "".join(temp)                       #facem un singur string cu elementele din lista


            if s not in dfa.stateSet and s!= '':                   #if the state is newly created
                newStates.append(s)            #then append it to the new_states_list
                dfa.stateSet.append(s)                  #as well as to the keys_list which contains all the states
            dfa.stateMachine[newStates[0]][nfa.pathSet[i]] = s   #assigning the new state in the DFA table
        
    newStates.remove(newStates[0])       #Removing the first element in the new_states_list

print("\nDFA :- \n")    
print(dfa.stateMachine)                                           #Printing the DFA created


dfa.stateSet = list(dfa.stateMachine.keys())
dfa.endingStates = []

for x in dfa.stateSet:
    for i in x:
        if i in nfa.endingStates:
            dfa.endingStates.append(x)
            break
        
dfa.startState = nfa.startState

print("\nFinal states of the DFA are : ",dfa.endingStates)       #Printing Final states of DFA

 

"""
# Code Ouput Example
No. of states : 4
No. of transitions : 2
state name : A
path : a
Enter end state from state A travelling through path a : 
A B
path : b
Enter end state from state A travelling through path b : 
A
state name : B
path : a
Enter end state from state B travelling through path a : 
C
path : b
Enter end state from state B travelling through path b : 
C
state name : C
path : a
Enter end state from state C travelling through path a : 
D
path : b
Enter end state from state C travelling through path b : 
D
state name : D
path : a
Enter end state from state D travelling through path a : 
path : b
Enter end state from state D travelling through path b : 
nfa.stateMachine :- 
{'A': {'a': ['A', 'B'], 'b': ['A']}, 'B': {'a': ['C'], 'b': ['C']}, 'C': {'a': ['D'], 'b': ['D']}, 'D': {'a': [], 'b': []}}
Printing nfa.stateMachine table :- 
        a    b
A  [A, B]  [A]
B     [C]  [C]
C     [D]  [D]
D      []   []
Enter final state of nfa.stateMachine : 
D
DFA :- 
{'A': {'a': 'AB', 'b': 'A'}, 'AB': {'a': 'ABC', 'b': 'AC'}, 'ABC': {'a': 'ABCD', 'b': 'ACD'}, 'AC': {'a': 'ABD', 'b': 'AD'}, 'ABCD': {'a': 'ABCD', 'b': 'ACD'}, 'ACD': {'a': 'ABD', 'b': 'AD'}, 'ABD': {'a': 'ABC', 'b': 'AC'}, 'AD': {'a': 'AB', 'b': 'A'}}
Printing DFA table :- 
         a    b
A       AB    A
AB     ABC   AC
ABC   ABCD  ACD
AC     ABD   AD
ABCD  ABCD  ACD
ACD    ABD   AD
ABD    ABC   AC
AD      AB    A
Final states of the DFA are :  ['ABCD', 'ACD', 'ABD', 'AD']
"""
#code to convert nfa.stateMachine to dfa 