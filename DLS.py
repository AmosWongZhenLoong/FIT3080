import time

def DLS(puzzle):
    next

def mergesort(container):
    '''
    sorts a list using mergesort because mergesort has an okay complexity
    and not too complicated
    arg container: the list to be sorted
    complexity: O(n log n)
    '''
    if len(container)>1:
        mid = len(container)//2
        leftside = container[:mid]
        rightside = container[mid:]

        mergesort(leftside)
        mergesort(rightside)

        i=0
        j=0
        k=0
        while i < len(leftside) and j < len(rightside):
            if leftside[i][1] <= rightside[j][1]:
                container[k]=leftside[i]
                i=i+1
            else:
                container[k]=rightside[j]
                j=j+1
            k=k+1

        while i < len(leftside):
            container[k]=leftside[i]
            i=i+1
            k=k+1

        while j < len(rightside):
            container[k]=rightside[j]
            j=j+1
            k=k+1

def getPossibleMoves(currentNode):
    possibleMoves = []
    for i in range(len(currentNode)):
        if currentNode[i] == 'E':
            ePos = i
            break
    if i - 3 >= 0:
        possibleMoves.append('3L')
    if i - 2 >= 0:
        possibleMoves.append('2L')
    if i - 1 >= 0:
        possibleMoves.append('1L')
    if i + 1 < len(currentNode):
        possibleMoves.append('1R')
    if i + 2 < len(currentNode):
        possibleMoves.append('2R')
    if i + 3 < len(currentNode):
        possibleMoves.append('3R')
    return possibleMoves

def getPossibleStates(possibleMoves,currentNode):
    possibleStates = []
    for i in range(len(possibleMoves)):
        if possibleMoves[i] == '3L':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j - 3
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '3L'
        elif possibleMoves[i] == '2L':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j - 2
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '2L'
        elif possibleMoves[i] == '1L':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j - 1
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '1L'
        elif possibleMoves[i] == '1R':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j + 1
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '1R'
        elif possibleMoves[i] == '2R':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j + 2
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '2R'
        elif possibleMoves[i] == '3R':
            for j in range(len(currentNode)):
                if currentNode[j] == 'E':
                    ePos = j
                    swapPos = j + 3
                    break
            itemToSwap = currentNode[swapPos]
            tempString = currentNode[:swapPos] + 'E' + currentNode[swapPos + 1:]
            tempString2 = tempString[:ePos] + str(itemToSwap) + tempString[ePos + 1:]
            move = '3R'
        temp = []
        temp.append(tempString2)
        temp.append(move)
        possibleStates.append(temp)
    return (possibleStates)

def endNodeChecker(string):
    B = []
    W = []
    for i in range(len(string)):
        if string[i] == 'B':
            B.append(i)
        if string[i] == 'W':
            W.append(i)
    if max(W) >= min(B):
        return False
    else:
        return True
        

########################################################################

nodeCart = {} # node : previous node, move made

testPuzzle = 'BBBBWWWWE'

OPEN = []
CLOSE = []

nodeCart[testPuzzle] = [None,None,1]

OPEN.append(testPuzzle)

previousNode = testPuzzle

limit = 30

noSolution = None

############################## LOOP POINT ##############################

print("current limit is: " + str(limit) + '\n')
while True:
    if len(OPEN) <= 0:
        print("solution not found")
        noSolution = False
        break
    currentNode = OPEN.pop(-1)
    depth = nodeCart[currentNode][2]
    possibleMoves = getPossibleMoves(currentNode)
    possibleStates = getPossibleStates(possibleMoves,currentNode)
    truePossibleStates = []
    truePossibleMoves = []
    if depth >= limit:
        continue
    else:
        depth = depth + 1
        for i in range(len(possibleStates)):
            if possibleStates[i][0] not in nodeCart:
                truePossibleStates.append(possibleStates[i])
                truePossibleMoves.append(possibleMoves[i])

        for i in range(len(truePossibleStates)):
            nodeCart[truePossibleStates[i][0]] = [truePossibleStates[i][1],currentNode,depth]

        for i in range(len(truePossibleStates)):
            OPEN.append(truePossibleStates[i][0])
            
        if endNodeChecker(currentNode) is True:
            print("solution found")
            print('end state is: ' + str(currentNode))
            break
        
        previousNode = currentNode
    CLOSE.append(currentNode)

if noSolution != False:
    nodes = []
    moves = []
    nodes.append(currentNode)
    while True:
        moves.append(nodeCart[currentNode][0])
        if nodeCart[currentNode][1] is not None:
            nodes.append(nodeCart[currentNode][1])
        else:
            break
        currentNode = nodeCart[currentNode][1]
    moves.insert(0,moves.pop(-1))
    nodes.reverse()
    moves.reverse()
    solution = []
    for i in range(len(nodes)):
        temp = []
        temp.append(nodes[i])
        temp.append(moves[i])
        solution.append(temp)
    print('state' + 'move'.rjust(len(currentNode)+4))
    print('----------------')
    for i in range(len(solution)):
        print(solution[i])

############################## END LOOP ##############################

#OPEN behaves like a stack
#take LAST item from OPEN
#evaluate next states
#check ancestory bloodline
#place in OPEN
#item deposit to CLOSE
#repeat


def testPossibleMoves():
    print(possibleMoves('BWBWE'))
    print(possibleMoves('BWEBW'))
    print(possibleMoves('EBWBW'))

def testEndNodeChecker():
    print(endNodeChecker('BBWWE'))
    print(endNodeChecker('BWEBW'))
    print(endNodeChecker('EBWBW'))
    print(endNodeChecker('WBWBE'))
    print(endNodeChecker('EWBWB'))
    print(endNodeChecker('WWBBE'))
    print(endNodeChecker('EWWBB'))

