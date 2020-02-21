#!/usr/bin/env python
# coding: utf-8

# Welcome to the 8-puzzle solver! Below are functions that assist in the brute force search (BFS) of the 8-puzzle.

# The BlankTileLocation function will search the current node for the position of the black tile and return it in rol col format.

# In[1]:


def BlankTileLocation(state):
    for row in range(len(state)):
        for col in range(len(state)):
            if state[row][col]==0:
                return row,col


# The AddNode function will add a "new" node to the nodeList if the node has not been seen before. If the nodes has been seen OR the node is not possible (move blank tile outside of puzzle) the node will not be added to the list.

# In[2]:


def AddNode(nodes,newNode):
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


# The below functions will move the blank tile in the given direction. If the move is not possible the function creates a faulty node which is recognized in the above function.

# In[3]:


def ActionMoveLeft(node):
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


# The below function "copyNode" was created because for some reason I was unable to find a way to pass the node by value and any changes I made to the node in the "ActionMove----" affected the original node.

# In[4]:


def copyNode(node):
    copy = [[0,0,0],[0,0,0],[0,0,0]]
    for y in range(3):
        for x in range(3):
            copy[y][x] = node[0][y][x]
    return [copy,node[1],node[2]]


# The checkColvable function checks whether the given start node is solvable. It does this by counting the number of iversions, or times a smaller number comes after a larger number when the node is in a list format. EX: 1,2,3,4,5,6,8,7,0 this function has 1 inversion. The 0 term is considered a "9".

# In[5]:


def checkSolvable(node):
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


# Below is my solver. It begins with the initial state of the system and an empty list of nodes. The goal state is defined and the start node is added to the nodelist. A counter to keep track of the current parent node is created along with a boolean variable to tell whether we have reached the goal state or not.

# In[16]:


def solve(startNode):
    nodes = []
    
    #this node will provide unsolvable
    #startNode = [[[8,1,2],
                  #[0,4,3],
                  #[7,6,5]]   ,1,0]

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
    
    #print()
    #x = 1   
    #for node in nodes:
     #       print("number: "+ str(x))
      #      print(node[0][0])
       #     print(node[0][1])
        #    print(node[0][2])
         #   print()
          #  x +=1

    #print("Steps: "+str(len(nodes)))
    
    return finalNode,nodes
    


# The generatePath function creates a list using the format of [current index,parent index]. This list outlines the steps to complete the puzzle, it creates this list via backtracking.

# In[14]:


def generatePath(finalNode,nodes):
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


# The below function takes the path and writes it to NodePath.txt for later use.

# In[22]:


def createNodePath(path,nodes):
    file1 = open("NodePath.txt","w") 
    for node in path:
        currentNode = nodes[node[0]-1][0]
        for row in range(3):
            for col in range(3):
                #print(currentNode[col][row],end=" ")
                file1.write(str(currentNode[col][row])+" ")
                if row ==2 and col == 2:
                    file1.write("\n")
        #print()
    file1.close() 


# The below function creates the nodesInfo.txt file which follows the format of our generated path.

# In[23]:


def createNodesInfo(path):
    file1 = open("NodesInfo.txt","w") 
    for node in path:
        file1.write(str(node[0])+" " + str(node[1])+ "\n")
        #print(node[0],node[1])
    file1.close() 


# The below function creates a Nodes.txt file which documents all of the explored nodes in the system by our solver.

# In[25]:


def createNodes(path,nodes):
    file1 = open("Nodes.txt","w") 
    count = 1
    for node in nodes:
        currentNode = node[0]
        for row in range(3):
            for col in range(3):
                file1.write(str(currentNode[col][row])+" ")
                #print(currentNode[col][row],end=" ")
        file1.write("\n")
        #print()
        count+=1
    file1.close() 


# The below function was copied from the proffesor's supplied plot_path.py file to help visulize the solution.

# In[11]:


def print_matrix(state):
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


# In[26]:


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


# In[21]:

#change start node to any configuration to attempt a solve.
import numpy as np
startNode = [[[1,2,3],
              [4,6,0],
              [7,5,8]]   ,1,0]
main()


# In[ ]:




