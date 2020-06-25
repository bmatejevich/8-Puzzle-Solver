#!/usr/bin/env python
# coding: utf-8

"""Welcome to the 8-puzzle solver! Below are functions that assist in the
brute force search (BFS) of the 8-puzzle."""
import numpy as np

def BlankTileLocation(state):
    """searches the puzzle for the location of the empyt space"""
    for row in range(len(state)):
        for col in range(len(state)):
            if state[row][col]==0:
                return row,col



def AddNode(nodes,newNode):
    """if a move is possible and not a repeated state it is added to the nodes list"""
    inSet = False
    for node in nodes:
        node1 = node[0][0]+node[0][1]+node[0][2]
        node1 = int(''.join(map(str, node1)))
        node2 = newNode[0][0]+newNode[0][1]+newNode[0][2]
        node2 = int(''.join(map(str, node2)))
        if node1 == node2:
            inSet = True
            #print("in set!")
    if node2 == 0:
        canMove = False
        #print("cant move")
    elif not inSet:
        nodes.append(newNode)



def ActionMoveLeft(node):
    """moves empty space to the left if possible, else returns fake node"""
    state = node
    row,col = BlankTileLocation(state[0])
    if col == 0:
        status = False
        newNode = [[[0,0,0],[0,0,0],[0,0,0]],1,1]
    else:
        status = True
        state[0][row][col] = state[0][row][col-1]
        state[0][row][col-1] = 0
        newNode = [state[0],node[1],node[1]]
    return status,newNode

def ActionMoveRight(node):
    """moves empty space to the right if possible, else returns fake node"""
    state = node
    row,col = BlankTileLocation(state[0])
    if col == 2:
        status = False
        newNode = [[[0,0,0],[0,0,0],[0,0,0]],1,1]
    else:
        status = True
        state[0][row][col] = state[0][row][col+1]
        state[0][row][col+1] = 0
        newNode = [state[0],node[1],node[1]]
    return status,newNode

def ActionMoveUp(node):
    """moves empty space to the up if possible, else returns fake node"""
    state = node
    row,col = BlankTileLocation(state[0])
    if row == 0:
        status = False
        newNode = [[[0,0,0],[0,0,0],[0,0,0]],1,1]
    else:
        status = True
        state[0][row][col] = state[0][row-1][col]
        state[0][row-1][col] = 0
        newNode = [state[0],node[1],node[1]]
    return status,newNode

def ActionMoveDown(node):
    """moves empty space to the down if possible, else returns fake node"""
    state = node
    row,col = BlankTileLocation(state[0])
    if row == 2:
        status = False
        newNode = [[[0,0,0],[0,0,0],[0,0,0]],1,1]
    else:
        status = True
        state[0][row][col] = state[0][row+1][col]
        state[0][row+1][col] = 0
        newNode = [state[0],node[1],node[1]]
    return status,newNode




def copyNode(node):
    """returns a copy of the node"""
    copy = [[0,0,0],[0,0,0],[0,0,0]]
    for y in range(3):
        for x in range(3):
            copy[y][x] = node[0][y][x]
    return [copy,node[1],node[2]]

def checkSolvable(node):
    """The checkColvable function checks whether the given start node is solvable.
     It does this by counting the number of iversions, or times a smaller number
     comes after a larger number when the node is in a list format.
     EX: 1,2,3,4,5,6,8,7,0 this function has 1 inversion. The 0 term is
     considered a "9"."""
    list = []
    for row in range(3):
        for col in range(3):
            list.append(node[row][col])
    inversions = 0
    for first in range(9):
        for second in range(8):
            if second+1 > first:
                if list[second+1]<list[first] and list[first] !=0 and list[second+1] !=0:
                    inversions +=1
    if inversions%2 == 1:
        return False;
    else:
        return True;


def solve(startNode):
    """ solve function takes in the initial state and will solve the puzzle if possible """
    nodes = []
    goal = [[1,2,3],[4,5,6],[7,8,0]]
    nodes.append(startNode)
    finished = False
    i = 0

    if not checkSolvable(startNode[0]):
        finished = True
        print("unsolvable!")
    while not finished:
        copy = copyNode(nodes[i])
        status,newNode = ActionMoveDown(copy)
        newNode[1] = len(nodes)+1
        AddNode(nodes,newNode)

        if newNode[0] == goal:
            finished=True
            print("Solved!")
            finalNode = newNode

        copy = copyNode(nodes[i])
        status,newNode = ActionMoveRight(copy)
        newNode[1] = len(nodes)+1
        AddNode(nodes,newNode)

        if newNode[0] == goal:
            finished=True
            print("Solved!")
            finalNode = newNode

        copy = copyNode(nodes[i])
        status,newNode = ActionMoveLeft(copy)
        newNode[1] = len(nodes)+1
        AddNode(nodes,newNode)

        if newNode[0] == goal:
            finished=True
            print("Solved!")
            finalNode = newNode

        copy = copyNode(nodes[i])
        status,newNode = ActionMoveUp(copy)
        newNode[1] = len(nodes)+1
        AddNode(nodes,newNode)

        if newNode[0] == goal:
            finished=True
            print("Solved!")
            finalNode = newNode

        i +=1
    return finalNode,nodes


def generatePath(finalNode,nodes):
    """ uses backtracking to find the path from start to goal state"""
    currentNode = finalNode
    parent_node_index = -1
    path = []
    while parent_node_index != 1:
        parent_node_index = currentNode[2]
        current_index = currentNode[1]
        path.append([current_index,parent_node_index])
        currentNode = nodes[parent_node_index-1]
    path.append([1,0])
    path.reverse()
    return path


def createNodePath(path,nodes):
    """ writes the path returned by generate path to a txt file for later use"""
    file1 = open("NodePath.txt","w")
    for node in path:
        currentNode = nodes[node[0]-1][0]
        for row in range(3):
            for col in range(3):
                file1.write(str(currentNode[col][row])+" ")
                if row ==2 and col == 2:
                    file1.write("\n")
    file1.close()


def createNodesInfo(path):
    """saves node path information to a txt file """
    file1 = open("NodesInfo.txt","w")
    for node in path:
        file1.write(str(node[0])+" " + str(node[1])+ "\n")
        #print(node[0],node[1])
    file1.close()

def createNodes(path,nodes):
    """saves a list of all explored nodes """
    file1 = open("Nodes.txt","w")
    count = 1
    for node in nodes:
        currentNode = node[0]
        for row in range(3):
            for col in range(3):
                file1.write(str(currentNode[col][row])+" ")
        file1.write("\n")
        count+=1
    file1.close()


def print_matrix(state):
    """function used to print solution step by step """
    counter = 0
    for row in range(0, len(state), 3):
        if counter == 0 :
            print("-------------")
        for element in range(counter, len(state), 3):
            if element <= counter:
                print("|", end=" ")
            print(int(state[element]), "|", end=" ")
        counter = counter +1
        print("\n-------------")


def main():
    finalNode,nodes = solve(startNode)
    path = generatePath(finalNode,nodes)
    createNodePath(path,nodes)
    createNodes(path,nodes)
    createNodesInfo(path)
    fname = 'nodePath.txt'
    data = np.loadtxt(fname)

    if len(data[1]) != 9:
        print("Format of the text file is incorrect, retry ")
    else:
        for i in range(0, len(data)):
            if i == 0:
                print("Start Node")
            elif i == len(data)-1:
                print("Achieved Goal Node")
            else:
                print("Step ",i)
            print_matrix(data[i])
            print()
            print()




startNode = [[[1,2,3],
              [4,6,0],
              [7,5,8]]   ,1,0]

"""this node will provide unsolvable"""
#startNode = [[[8,1,2],
              #[0,4,3],
              #[7,6,5]]   ,1,0]
main()
