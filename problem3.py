import sys
sys.setrecursionlimit(10**5) #Python recursion limit is 1000, not viable for this project, feel free to adjust depending on how many nodes tested
from typing import List,Set
import random

class Node:
    #neighbors: List
    def __init__(self, val: int, neighbors: Set) -> None:
        self.val=val
        self.neighbors=neighbors
    def __str__(self):
        neighs=self.neighbors
        res=""
        for node in neighs:
            res+=node.val+","
        res=res[:-1]
        return "Val: "+self.val +", Neighbors:"+"["+res+"]"

class Graph:
    def __init__(self):
        self.nodes=dict()
    
    def __str__(self) -> str:
        printable=dict()
        for node in self.nodes:
            temp=[]
            for neighbor in self.nodes[node].neighbors:
                temp.append(neighbor.val)
            printable[node]=temp
        return str(printable)

    def addNode(self, nodeVal: str) -> None:
        self.nodes[nodeVal]=Node(nodeVal,[])

    def addUndirectedEdge(self, first: Node, second: Node) -> None:
        #if first in self.nodes.values() and second in self.nodes.values():
        if second not in self.nodes[first.val].neighbors:
            self.nodes[first.val].neighbors.append(second)
        if first not in self.nodes[second.val].neighbors: 
            self.nodes[second.val].neighbors.append(first)
    def getAllNodes(self) -> Set:
        return set(self.nodes.values())
    def getPointer(self, nodeVal: str) -> Node:
        for nodePointer in self.getAllNodes():
            if nodePointer.val==nodeVal:
                return nodePointer
        return None 

class GraphSearch:
    def DFSRec(self, start: Node, end: Node) -> List:
        res=self.DFSRecHelper(start,end,[])
        if end.val in res:
            return res
            #return [node.val for node in res]
        return None

    def DFSRecHelper(self, start: Node, end: Node, visited: List) -> List:
        res=[start.val]
        if start.val==end.val:
            return res

        visited.append(start.val)
        for node in start.neighbors:
            if node.val not in visited:
                res.extend(self.DFSRecHelper(node,end,visited))
                if end.val in res:
                    return res
        return res
    
    def DFSIter(self, start: Node, end: Node) -> List:
        path,visited=[],[]
        stack=[start]

        while stack!=None:
            currNode=stack.pop()
            if currNode.val not in visited:
                path.append(currNode.val)
                if currNode.val==end.val:
                    break
                visited.append(currNode.val)
                stack.extend(currNode.neighbors[::-1]) 
                #So the recursive and iterative can have the same result to compare when reviewing, I reversed the neighbors list :)

        if path==[] or (end.val not in path):
            return None
        return path
    
    def BFTRec(self, graph: Graph) -> List:
        queue = []
        visited=[]
        for node in graph.getAllNodes():
            if node.val not in visited:
                self.BFTHelper(node,queue,visited)
        path=[]
        while queue:
            currNode = queue.pop()
            path.append(currNode.val)
        return path

    def BFTHelper(self, node: Node, queue: List, visited: List) -> None:
        visited.append(node.val)
        nextLevel=[node for node in node.neighbors]
        for neighbor in node.neighbors:
            if neighbor.val not in visited:
                self.BFTHelper(neighbor,queue,visited)
        for node in nextLevel:
            if node not in queue:
                queue.append(node)
    
    def BFTIter(self,graph: Graph) -> List:
        visited=[]
        path=[]
        for node in graph.getAllNodes():
            queue=[node]
            nextLevel=[]
            while queue:
                currNode=queue.pop()
                if currNode.val not in visited:
                    nextLevel.extend(currNode.neighbors)
                    visited.append(currNode.val)
                    path.append(currNode.val)
                if len(queue)==0 and len(nextLevel)!=0:
                    queue=[node for node in nextLevel]
                    nextLevel=[]
        return path
                
#Main program
def createLinkedList(n: int) -> Graph:
    linkedList=Graph()
    for i in range(n):
        linkedList.addNode(str(i))
        if i!=0:
            #Get the pointer for the first and second node.
            linkedList.addUndirectedEdge(linkedList.getPointer(str(i)),linkedList.getPointer(str(i-1)))
    return linkedList

def createRandomUnweightedGraphIter(n: int) -> Graph:
    randomGraph=Graph()
    for i in range(n):
        randomGraph.addNode(str(i))
        firstNode=randomGraph.getPointer(str(i))

        randomNum=random.randint(0,99)
        while randomNum<50 and i>0:
            secondNum=str(random.randint(0,i-1))
            randomGraph.addUndirectedEdge(firstNode,randomGraph.getPointer(secondNum))
            randomNum=random.randint(0,99)
            
    return randomGraph

def BFTRecLinkedList(graph: Graph) -> List:
    search=GraphSearch()
    graph=createLinkedList(10000)
    return search.BFTRec(graph)

def BFTIterLinkedList(graph: Graph) -> List:
    search=GraphSearch()
    graph=createLinkedList(10000)
    return search.BFTIter(graph)


#Drivers
search=GraphSearch()

LL=createLinkedList(100) #0-baseed indexing
#print(LL) #to view the list

##print(search.DFSRec(LL.getPointer("5"),LL.getPointer("10")))
##print(search.DFSIter(LL.getPointer("5"),LL.getPointer("10")))

#rand=createRandomUnweightedGraphIter(9) #numbers 0-8
#print(rand)
#print(search.DFSRec(rand.getPointer("0"),rand.getPointer("8")))
#print(search.DFSIter(rand.getPointer("0"),rand.getPointer("8")))

# BFTRecLinkedList(LL)
# BFTIterLinkedList(LL)
