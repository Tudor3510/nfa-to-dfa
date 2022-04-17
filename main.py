
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


reader = open("input.txt", "r")

nfa.stateMachine = {}                                 
nfa.noStates = int(reader.readline())
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
              
    
newStates = []
dfa.stateMachine = {}
dfa.stateSet = list(nfa.startState)


dfa.stateMachine[dfa.stateSet[0]] = {}
for y in range(len(nfa.pathSet)):

    aux = nfa.stateMachine[dfa.stateSet[0]][nfa.pathSet[y]]
    aux = list(dict.fromkeys(aux))          #stergem duplicatele
    aux.sort()                              #sortam pentru a nu avea probleme de genul ab != ba
    s = "".join(aux)                        #facem un singur string cu elementele din lista

    s = "".join(aux)                        #facem un singur string cu elementele din lista continuta in nfa.stateMachine-ul startState si pathSet-ul respectiv
    dfa.stateMachine[dfa.stateSet[0]][nfa.pathSet[y]] = s
    if s not in dfa.stateSet and s != '':
        newStates.append(s)
        dfa.stateSet.append(s)
        

while len(newStates) != 0:
    dfa.stateMachine[newStates[0]] = {}

    for o in range(len(newStates[0])):
        for i in range(len(nfa.pathSet)):
            aux = []
            for j in range(len(newStates[0])):
                aux += nfa.stateMachine[newStates[0][j]][nfa.pathSet[i]]

            aux = list(dict.fromkeys(aux))          #stergem duplicatele
            aux.sort()                              #sortam pentru a nu avea probleme de genul ab != ba
            s = "".join(aux)                        #facem un singur string cu elementele din lista


            if s not in dfa.stateSet and s!= '':
                newStates.append(s)
                dfa.stateSet.append(s)
            dfa.stateMachine[newStates[0]][nfa.pathSet[i]] = s
        
    newStates.remove(newStates[0])

print("\nDFA:")
print(dfa.stateMachine)


dfa.stateSet = list(dfa.stateMachine.keys())
dfa.endingStates = []

for x in dfa.stateSet:
    for i in x:
        if i in nfa.endingStates:
            dfa.endingStates.append(x)
            break
        
dfa.startState = nfa.startState

print("\nStarile finale ale DFA-ului : ",dfa.endingStates)      