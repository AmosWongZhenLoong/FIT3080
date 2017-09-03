import argparse as ap
import time

######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python solvepuzzle.py <puzzle> <procedure> <output_file> <flag>
#   for example: python solvepuzzle.py BBWEW A result 0
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################
def graphsearch(puzzle, flag, procedure_name):
    solution = ""
    if procedure_name == "DLS":

        if puzzleValidity(puzzle) is False:
            print('invalid puzzle')
            exit()
        
        bound = 30  # bound of 30 can reliabilly solve puzzles up to length 9

        startTime = time.time()

        # dictionary as database for all visited and expanded nodes
        nodeCart = {} # node : previous node, move made

        testPuzzle = puzzle

        OPEN = []
        CLOSE = []

        identifierCount = 0     # each node has an identifier N0, N1, N2, ...
        identifier = 'N' + str(identifierCount)

        cost = 0

        nodeCart[testPuzzle] = [None,None,1,identifier,cost]

        OPEN.append(testPuzzle)

        previousNode = testPuzzle

        limit = bound

        noSolution = None   # becomes false if selected depth does not have solution

        ############################## LOOP POINT ##############################

        print("current limit is: " + str(limit) + '\n')
        while True:
            if len(OPEN) <= 0:  # open becomes empty if solution is not found at the selected limit
                print("solution not found at this limit")
                noSolution = False
                break
            
            currentNode = OPEN.pop(-1)
            currentCost = nodeCart[currentNode][4]
            depth = nodeCart[currentNode][2]
            # possible moves are (3L,2L,1L,1R,2R,3R)
            possibleMoves = getPossibleMoves(currentNode)
            # possible states are based on the possible moves
            possibleStates = getPossibleStates(possibleMoves,currentNode)
            truePossibleStates = []
            truePossibleMoves = []
            if depth >= limit:
                continue
            else:
                depth = depth + 1
                for i in range(len(possibleStates)):
                    if possibleStates[i][0] not in nodeCart:    # check ancestors
                        truePossibleStates.append(possibleStates[i])
                        truePossibleMoves.append(possibleMoves[i])

                for i in range(len(truePossibleStates)):
                    identifierCount += 1
                    identifier = 'N' + str(identifierCount)
                    # figure out the move cost
                    if truePossibleMoves[i] == '3L' or truePossibleMoves[i] == '3R':
                        childCost = 2
                    else:
                        childCost = 1
                    finalCost = currentCost + childCost
                    # store in a database
                    nodeCart[truePossibleStates[i][0]] = [truePossibleStates[i][1],currentNode,depth,identifier,finalCost]

                for i in range(len(truePossibleStates)):
                    OPEN.append(truePossibleStates[i][0])
                    
                if endNodeChecker(currentNode) is True: # check if a solution is reached
                    print("solution found")
                    print('end state is: ' + str(currentNode))
                    break
                
                previousNode = currentNode
            CLOSE.append(currentNode)

        endTime = time.time()

        if noSolution != False:
            nodes = []
            moves = []
            costs = []
            identifiers = []
            nodes.append(currentNode)
            while True:
                moves.append(nodeCart[currentNode][0])
                costs.append(nodeCart[currentNode][4])
                identifiers.append(nodeCart[currentNode][3])
                if nodeCart[currentNode][1] is not None:
                    nodes.append(nodeCart[currentNode][1])
                else:
                    break
                currentNode = nodeCart[currentNode][1]
            moves[-1] = 'START'
            nodes.reverse()
            moves.reverse()
            costs.reverse()
            identifiers.reverse()
            ans = []
            for i in range(len(nodes)):
                temp = []
                temp.append(moves[i])
                temp.append(nodes[i])
                temp.append(costs[i])
                temp.append(identifiers[i])
                ans.append(temp)
                
            print('move' + 'state'.rjust(len(currentNode)+2) + 'cost'.rjust(len(currentNode)) + 'identifier'.rjust(len(currentNode)+5))
            print('-------------------------------')

            # the number of lines printed to console depends on flag value
            if flag > 0 and len(ans) > flag:
                for i in range(flag):
                    line = (str(ans[i][0]) + '    ' + str(ans[i][1]) + '    ' + str(ans[i][2]))
                    lineDiag = (str(ans[i][0]) + '    ' + str(ans[i][1]) + '    ' + str(ans[i][2]) + '    ' + str(ans[i][3]))
                    print(lineDiag)
                    solution = solution + line + '\n'
                for i in range(flag,len(ans)):
                    line = (str(ans[i][0]) + '    ' + str(ans[i][1]) + '    ' + str(ans[i][2]))
                    solution = solution + line + '\n'
            else:
                for i in range(len(ans)):
                    line = (str(ans[i][0]) + '    ' + str(ans[i][1]) + '    ' + str(ans[i][2]))
                    lineDiag = (str(ans[i][0]) + '    ' + str(ans[i][1]) + '    ' + str(ans[i][2]) + '    ' + str(ans[i][3]))
                    print(lineDiag)
                    solution = solution + line + '\n'
        print("time taken to search: " + str(endTime-startTime))
        print('write to file complete')
        
    elif procedure_name == "A":

        if puzzleValidity(puzzle) is False:
            print('invalid puzzle')
            exit()

        startTime = time.time()

        nodeCart = {} # node : g, h, f, previous node, move made
        biasedCart = {} # f : node, priority(1,2,3)

        testPuzzle = str(puzzle)
        if getHeuristic(testPuzzle) == 0:   # if puzzle is already solved
            print('puzzle is already at end state')
            time.sleep(2)
            exit()
        g = 0
        h = getHeuristic(testPuzzle)
        f = g + h

        identifierCount = 0
        identifier = 'N' + str(identifierCount)

        nodeCart[testPuzzle] = [g,h,f,None,None,identifier]
        biasedCart[f] = []
        biasedCart[f].append([testPuzzle,1])

        OPEN = [[testPuzzle,f]]
        CLOSE = []
        NEXT = []

        endFound = False
        ############################## LOOP POINT ##############################
        while True:
            smallestHeuristic = getSmallestHeuristic(OPEN)
            got = False
            # if there are more than one node with the same cost
            # the chosen node is based on certain priorities
            # prefer right movements over left movements
            # prefer hops over shifts
            if len(biasedCart[smallestHeuristic]) == 1:
                currentNode = biasedCart[smallestHeuristic][0][0]
                del biasedCart[smallestHeuristic][0]
            else:
                for i in range(len(biasedCart[smallestHeuristic])):
                    if biasedCart[smallestHeuristic][i][1] == 1:
                        currentNode = biasedCart[smallestHeuristic][i][0]
                        del biasedCart[smallestHeuristic][i]
                        got = True
                        break
                if got == False:
                    for i in range(len(biasedCart[smallestHeuristic])):
                        if biasedCart[smallestHeuristic][i][1] == 2:
                            currentNode = biasedCart[smallestHeuristic][i][0]
                            del biasedCart[smallestHeuristic][i]
                            got = True
                            break
                if got == False:
                    for i in range(len(biasedCart[smallestHeuristic])):
                        if biasedCart[smallestHeuristic][i][1] == 3:
                            currentNode = biasedCart[smallestHeuristic][i][0]
                            del biasedCart[smallestHeuristic][i]
                            got = True
                            break

            for i in range(len(OPEN)):
                if OPEN[i][0] == currentNode:
                    del OPEN[i]
                    break

            #maximum 6 possible moves for empty tile (3L,2L,1L,1R,2R,3R)
            possibleMoves = getPossibleMoves(currentNode)

            #each possible move corresponds to a state
            possibleStates = getPossibleStates(possibleMoves,currentNode)

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
                G = nodeCart[currentNode][0]
                if move == '3L' or move == '3R':
                    G = G + 2
                else:
                    G = G + 1
                H = getHeuristic(node)
                F = G + H
                if H == 0:      # a solution node will give a heuristic of 0
                    identifierCount += 1
                    identifier = 'N' + str(identifierCount)
                    nodeCart[node] = [G,H,F,currentNode,move,identifier]
                    endNode = node
                    endFound = True
                    break
                else:
                    identifierCount += 1
                    identifier = 'N' + str(identifierCount)
                    nodeCart[node] = [G,H,F,currentNode,move,identifier]
                if F in biasedCart:
                    if move == '3L' or move == '2L':
                        biasedCart[F].append([node,1])
                    elif move == '2R' or move == '3R' or move == '1L':
                        biasedCart[F].append([node,2])
                    elif move == '1R':
                        biasedCart[F].append([node,3])
                else:
                    biasedCart[F] = []
                    if move == '3L' or move == '2L':
                        biasedCart[F].append([node,1])
                    elif move == '2R' or move == '3R' or move == '1L':
                        biasedCart[F].append([node,2])
                    elif move == '1R':
                        biasedCart[F].append([node,3])
                temp = []
                temp.append(node)
                temp.append(F)
                rearranger.append(temp)

            if endFound == True:
                break

            #reorder NEXT states
            mergesort(rearranger)

            #add to OPEN
            for i in range(len(rearranger)):
                OPEN.append(rearranger[i])

            CLOSE.append(currentNode)
            NEXT = []

        endTime = time.time()

        print('the end state is: ' + endNode + '\n')
        gs = []
        nodes = []
        moves = []
        identifiers = []
        while True:
            gs.append(nodeCart[endNode][0])
            nodes.append(endNode)
            identifiers.append(nodeCart[endNode][5])
            if nodeCart[endNode][3] is not None:
                moves.append(nodeCart[endNode][4])
                endNode = nodeCart[endNode][3]
            else:
                break

        moves.append('START')
        index = 0
        resultCollector = [] #format: [move, node, cost, identifier]
        for i in range(len(moves)):
            index = index - 1
            temp = []
            temp.append(moves[index])
            temp.append(nodes[index])
            temp.append(gs[index])
            temp.append(identifiers[index])
            resultCollector.append(temp)

        print("move" + "node".rjust(len(endNode) + 2) + "cost".rjust(9) + 'identifier'.rjust(12))
        print("----------------------------------")

        # amount of lines to print depends on value of flag
        if flag > 0 and len(resultCollector) > flag:
            for i in range(flag):
                line = (str(resultCollector[i][0]) + '    ' + str(resultCollector[i][1]) + '    ' + str(resultCollector[i][2]))
                lineDiag = (str(resultCollector[i][0]) + '    ' + str(resultCollector[i][1]) + '    ' + str(resultCollector[i][2]) + '    ' + str(resultCollector[i][3]))
                print(lineDiag)
                solution = solution + line + '\n'
            for i in range(flag,len(resultCollector)):
                line = (str(resultCollector[i][0]) + '    ' + str(resultCollector[i][1]) + '    ' + str(resultCollector[i][2]))
                solution = solution + line + '\n'
        else:
            for i in range(len(resultCollector)):
                line = (str(resultCollector[i][0]) + '    ' + str(resultCollector[i][1]) + '    ' + str(resultCollector[i][2]))
                lineDiag = (str(resultCollector[i][0]) + '    ' + str(resultCollector[i][1]) + '    ' + str(resultCollector[i][2]) + '    ' + str(resultCollector[i][3]))
                print(lineDiag)
                solution = solution + line + '\n'
                
        print('\n')
        print("time taken to search: " + str(endTime-startTime))
        print("write to file complete")

    else: 
        print("invalid procedure name")

    return solution

############################# Functions Used ##################################
def puzzleValidity(string):
    if len(string) < 3:
        return False
    eCount = 0
    for i in range(len(string)):
        if string[i] != 'B' and string[i] != 'E' and string[i] != 'W':
            return False
        if string[i] == 'E':
            eCount += 1
    if eCount > 1:
        return False
    if eCount == 0:
        return False
    return True

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

def getHeuristic(puzzle):
    counter = 0
    for i in range(len(puzzle)):
        if puzzle[i] == 'B':
            for j in range(i,len(puzzle)):
                if puzzle[j] == 'W':
                    counter = counter + 1
                    puzzle = puzzle[:j] + 'Z' + puzzle[j+1:]
                    break
    #print(puzzle)
    return counter

def getSmallestHeuristic(container):
    smallest = 999
    for i in range(len(container)):
        if container[i][1] < smallest:
            smallest = container[i][1]
    return smallest
    
###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("puzzle_string", help= "comprises a sequence of symbols, can be B, W, E", type= str)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be BK, DLS, A", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
# print("The puzzle is " + arguments.puzzle_string)
# print("The procedure_name is " + arguments.procedure_name)
# print("The output_file_name is " + arguments.output_file_name)
# print("The flag is " + str(arguments.flag))
##############################################################################

    # Extract the required arguments
    puzzle = arguments.puzzle_string
    procedure_name = arguments.procedure_name
    output_file_name = arguments.output_file_name
    flag = arguments.flag

    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "DLS" or procedure_name == "A":
        solution_string = graphsearch(puzzle, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()
