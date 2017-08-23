def eyStar(puzzle):
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

def getHeuristic(puzzle):
    counter = 0
    for i in range(len(puzzle)):
        if puzzle[i] == 'B':
            for j in range(i,len(puzzle)):
                if puzzle[j] == 'W':
                    counter = counter + 1
                    puzzle = puzzle[:j] + 'Z' + puzzle[j+1:]
                    break
    print(puzzle)
    return counter

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

nodeCart = {} #format: g, h, f, previous node, move made

testPuzzle = 'BBWWE'

g = 0
h = getHeuristic(testPuzzle)
f = g + h

nodeCart[testPuzzle] = [g,h,f,None,None]

OPEN = [testPuzzle]
CLOSE = []
NEXT = []

############################## LOOP POINT ##############################

currentNode = OPEN[0]
del OPEN[0]

#maximum 6 possible moves for empty tile (3L,2L,1L,1R,2R,3R)
possibleMoves = getPossibleMoves(currentNode)
print(possibleMoves)

#each possible move corresponds to a state
possibleStates = getPossibleStates(possibleMoves,currentNode)
print(possibleStates)

#check ancestors
for i in range(len(possibleStates)):
    state = possibleStates[i][0]
    if state not in nodeCart:
        NEXT.append(possibleStates[i])

#g,h,f evaluation for NEXT
rearranger = []
for i in range(len(NEXT)):
    node = NEXT[i][0]
    move = NEXT[i][1]
    if move == '3L' or move == '3R':
        G = g + 2
    else:
        G = g + 1
    H = getHeuristic(node)
    F = G + H
    nodeCart[node] = [G,H,F,currentNode,move]
    temp = []
    temp.append(node)
    temp.append(F)
    rearranger.append(temp)

#reorder NEXT states
mergesort(rearranger)

#add to OPEN
for i in range(len(rearranger)):
    OPEN.append(rearranger[i])

CLOSE.append(currentNode)
NEXT = []

############################## END LOOP ##############################

#take first item from OPEN
#evaluate next states for ancestory bloodline
#pure bloods gets g,h,f evaluation and entry in nodeCart
#reorder next states based on asc f
#place in OPEN
#item deposit to CLOSE
#clear NEXT
#repeat


def testPossibleMoves():
    print(possibleMoves('BWBWE'))
    print(possibleMoves('BWEBW'))
    print(possibleMoves('EBWBW'))
