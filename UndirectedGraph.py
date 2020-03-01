
# coding: utf-8

# In[229]:


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import numpy.random as rand
import time


# In[710]:


"""
Networks is a module that implements a network of nodes connected by
edges, and various algorithms and measurements implemented on networks.
(This type of data structure is also known in mathematics as a graph.
What we deal with specifically here are undirected graphs, where there is
no direction or asymmetry between the nodes that delineate an edge.)
This module contains the core code needed to define and manipulate
networks, independently of how they are created or what their context is.
We use the Networks module as part of other problem modules, such as
SmallWorld and Percolation.
"""

# Import the necessary libraries.
import NetGraphics  # a separate module supporting network visualization
import imp
imp.reload(NetGraphics) 

# -----------------------------------------------------------------------
#
# Defining undirected graph class: used by both Small World and Percolation
# exercises.
#
# -----------------------------------------------------------------------

class UndirectedGraph:
    """An UndirectedGraph g contains a dictionary (g.connections) that
    maps a node identifier (key) to a list of nodes connected to (values).
    g.connections[node] returns a list [node2, node3, node4] of neighbors.
    Node identifiers can be any non-mutable Python type (e.g., integers,
    tuples, strings, but not lists).
    """
    def __init__(self):
        """UndirectedGraph() creates an empty graph g.
        g.connections starts as an empty dictionary.  When nodes are
        added, the corresponding values need to be inserted into lists.

        A method/function definition in a class must begin with an instance
        of the class in question; by convention, the name "self" is used for
        this instance."""
        self.connections = {}

    def HasNode(self, node):
        """Returns True if the graph contains the specified node, and
        False otherwise.  Check directly to see if the dictionary of
        connections contains the node, rather than (inefficiently)
        generating a list of all nodes and then searching for the
        specified node."""
        # Hint: use the "in" operator to test if a key is in a dictionary
        for key, value in self.connections.items():
            #print(str(key) +': '+str(value))
            if key == node:
                return True
        return False

    def AddNode(self, node):
        """Uses HasNode(node) to determine if node has already been added."""
        if self.HasNode(node) == False:
            self.connections[node] = []
            #print('Added')

    def AddEdge(self, node1, node2):
        """
        Add node1 and node2 to network first
        Adds new edge 
        (appends node2 to connections[node1] and vice-versa, since it's
        an undirected graph)
        Do so only if old edge does not already exist 
        (node2 not in connections[node1])
        """
        self.AddNode(node1)
        self.AddNode(node2)
        
        
        #add node1 to node2
        for key, value in self.connections.items():
            #First find node1...:
            if key == node1:
                #print('Neighbors: '+str(self.GetNeighbors(key))+ ' and: '+str(node2 in self.GetNeighbors(key)))
                neighb = value
                if node2 not in neighb:
                    value.append(node2)
        #add node2 to node1
        for key, value in self.connections.items():
            #First find node2...:
            if key == node2:
                neighb = value
                if node1 not in neighb:
                    value.append(node1)
                
        pass

    def GetNodes(self):
        """g.GetNodes() returns all nodes (keys) in connections"""
        n = []
        for key, value in self.connections.items():
            n.append(key)
        return n

    def GetNeighbors(self, node):
        """g.GetNeighbors(node) returns a copy of the list of neighbors of
        the specified node.  A copy is returned (using the [:] operator) so
        that the user does not inadvertently change the neighbor list."""
        for key, value in self.connections.items():
            #print(str(key) +': '+str(value))
            if key == node:
                return value
        return null

# Simple test routines

# <codecell>
def pentagraph():
    """pentagraph() creates a simple 5-node UndirectedGraph, and then uses
    the imported NetGraphics module to layout and display the graph.
    The graph is returned from the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,2)
    g.AddEdge(0,3)
    g.AddEdge(1,3)
    g.AddEdge(1,4)
    g.AddEdge(2,4)
    NetGraphics.DisplayCircleGraph(g)
    return g

# <codecell>
def circle8():
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    g.AddEdge(0,1)
    g.AddEdge(1,2)
    g.AddEdge(2,3)
    g.AddEdge(3,4)
    g.AddEdge(4,5)
    g.AddEdge(5,6)
    g.AddEdge(6,7)
    g.AddEdge(7,0)
    NetGraphics.DisplayCircleGraph(g)
    return g


def smallWorldNetwork(L,Z,p, show = True):
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    minn = 2
    for i in range(L):
        g.AddNode(i)
    
    for i in range(L):
        on = 1
        getNext = i + on
        getPrev = i - on
        if getNext >= L:
            #print(getNext)
            getNext = getNext - L
        if getPrev < 0:
            #print(getPrev)
            getPrev = L + getPrev
        g.AddEdge(i,getNext)
        g.AddEdge(i,getPrev)
        
    for i in range(L):
        on = 2
        for j in range(Z-minn):
            n = 0
            if j%2 == 0:
                n = i + on
            else:
                n = i - on
                on += 1
            if n >= L:
                n = n - L
            if n < 0:
                n = L + n
            #print('added: '+str(i)+' to '+str(n))
            g.AddEdge(i,n)
        
        
    #Now random
    ran = int(p * L * int(Z/2))
    #print('Random Lines:' +str(ran))
    Edges = []
    start = 0
    end = 0
    edge = []
    #print(ran)
    for i in range(ran):
        dist = 0
        #print(i)
        while (dist < Z/2 or edge in Edges):
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            if start > L/2 and end > L/2:
                dist = np.abs(start-end)
            elif end > L/2:
                end2 = L - end
                dist2 = np.abs(start+end2)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            elif start > L/2:
                start2 = L - start
                dist2 = np.abs(start2+end)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            else:
                dist = np.abs(start-end)
                
                
            edge = [start, end]
        g.AddEdge(start, end)
        Edges.append(edge)
    if show:
        NetGraphics.DisplayCircleGraph(g)
    return g

def smallWorldNetworkLong(L,Z,p, show = True, depth = 10):
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    minn = 2
    for i in range(L):
        g.AddNode(i)
    
    for i in range(L):
        on = 1
        getNext = i + on
        getPrev = i - on
        if getNext >= L:
            #print(getNext)
            getNext = getNext - L
        if getPrev < 0:
            #print(getPrev)
            getPrev = L + getPrev
        g.AddEdge(i,getNext)
        g.AddEdge(i,getPrev)
        
    for i in range(L):
        on = 2
        for j in range(Z-minn):
            n = 0
            if j%2 == 0:
                n = i + on
            else:
                n = i - on
                on += 1
            if n >= L:
                n = n - L
            if n < 0:
                n = L + n
            #print('added: '+str(i)+' to '+str(n))
            g.AddEdge(i,n)
        
        
    #Now random
    ran = int(p * L * int(Z/2))
    #print('Random Lines:' +str(ran))
    Edges = []
    start = 0
    end = 0
    edge = []
    #print(ran)
    for i in range(ran):
        dist = 0
        #print(i)
        while (dist < Z/2 or edge in Edges) or dist < depth:
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            dist = getDist(L, start, end)
                
            edge = [start, end]
        #print(str(start) +' to '+str(end) +': '+str(dist))
        #if dist < depth:
        #    print(dist)
        g.AddEdge(start, end)
        Edges.append(edge)
    if show:
        NetGraphics.DisplayCircleGraph(g)
    return g

def smallWorldNetworkPerfect(L,Z,p, show = True):
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    minn = 2
    for i in range(L):
        g.AddNode(i)
    
    for i in range(L):
        on = 1
        getNext = i + on
        getPrev = i - on
        if getNext >= L:
            #print(getNext)
            getNext = getNext - L
        if getPrev < 0:
            #print(getPrev)
            getPrev = L + getPrev
        g.AddEdge(i,getNext)
        g.AddEdge(i,getPrev)
        
    for i in range(L):
        on = 2
        for j in range(Z-minn):
            n = 0
            if j%2 == 0:
                n = i + on
            else:
                n = i - on
                on += 1
            if n >= L:
                n = n - L
            if n < 0:
                n = L + n
            #print('added: '+str(i)+' to '+str(n))
            g.AddEdge(i,n)
        
        
    #Now random
    ranTot = int(p * L * int(Z/2))
    ranLong = int(ranTot/12)
    ranShort = ranTot - ranLong
    #print('Random Lines:' +str(ran))
    Edges = []
    start = 0
    end = 0
    edge = []
    #print(ran)
    for i in range(ranLong): # Have a few long relationships
        dist = 0
        #print(i)
        while (dist < Z/2 or edge in Edges) or dist < L/2 - L/8: # Need to have long ones
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            if start > L/2 and end > L/2:
                dist = np.abs(start-end)
            elif end > L/2:
                end2 = L - end
                dist2 = np.abs(start+end2)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            elif start > L/2:
                start2 = L - start
                dist2 = np.abs(start2+end)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            else:
                dist = np.abs(start-end)
                
            edge = [start, end]
        #print(str(start) +' to '+str(end) +': '+str(dist))
        #if dist < depth:
        #    print(dist)
        g.AddEdge(start, end)
        Edges.append(edge)
    for i in range(ranShort): # Have 3 times as many short relationships
        dist = 0
        #print(i)
        while (dist < Z/2 or edge in Edges) or dist > L/4: # Need to have short ones ones
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            if start > L/2 and end > L/2:
                dist = np.abs(start-end)
            elif end > L/2:
                end2 = L - end
                dist2 = np.abs(start+end2)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            elif start > L/2:
                start2 = L - start
                dist2 = np.abs(start2+end)
                dist3 = np.abs(start-end)
                if dist2 < dist3:
                    dist = dist2
                else:
                    dist = dist3
            else:
                dist = np.abs(start-end)
                
            edge = [start, end]
        #print(str(start) +' to '+str(end) +': '+str(dist))
        #if dist < depth:
        #    print(dist)
        g.AddEdge(start, end)
        Edges.append(edge)
    if show:
        NetGraphics.DisplayCircleGraph(g)
    return g
def getDist(L, start, end):
    dist = 0
    if start == 0 and end == 0:
        return 0
    if start > L/2 and end > L/2:
        return np.abs(start-end)
    elif end > L/2:
        end2 = L - end
        dist2 = np.abs(start+end2)
        dist3 = np.abs(start-end)
        if dist2 < dist3:
            return dist2
        else:
            return dist3
    elif start > L/2:
        start2 = L - start
        dist2 = np.abs(start2+end)
        dist3 = np.abs(start-end)
        if dist2 < dist3:
            return dist2
        else:
            return dist3
    else:
        return np.abs(start-end)
    return dist
def smallWorldNetworkShort(L,Z,p, show = True, depth = 10):
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    minn = 2
    for i in range(L):
        g.AddNode(i)
    
    for i in range(L):
        on = 1
        getNext = i + on
        getPrev = i - on
        if getNext >= L:
            #print(getNext)
            getNext = getNext - L
        if getPrev < 0:
            #print(getPrev)
            getPrev = L + getPrev
        g.AddEdge(i,getNext)
        g.AddEdge(i,getPrev)
        
    for i in range(L):
        on = 2
        for j in range(Z-minn):
            n = 0
            if j%2 == 0:
                n = i + on
            else:
                n = i - on
                on += 1
            if n >= L:
                n = n - L
            if n < 0:
                n = L + n
            #print('added: '+str(i)+' to '+str(n))
            g.AddEdge(i,n)
        
        
    #Now random
    ran = int(p * L * int(Z/2))
    #print('Random Lines:' +str(ran))
    Edges = []
    start = 0
    end = 0
    edge = []
    #print(ran)
    for i in range(ran):
        dist = 0
        #print(i)
        while dist < Z/2 or edge in Edges or dist > depth :
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            dist = np.abs(start-end)
            edge = [start, end]
            #if dist > Z/2 and (edge in Edges) == False and dist <
        #print(dist)
        g.AddEdge(start, end)
        Edges.append(edge)
    if show:
        NetGraphics.DisplayCircleGraph(g)
    return g

def smallWorldNetworkSpecific(L,Z,p, show = True, depth = 10):
    """circle8() creates an 8-node UndirectedGraph, where the nodes are
    arranged in a circle (ring), and then uses the imported NetGraphics
    module to layout and display the graph.  The graph is returned from
    the function.
    """
    g = UndirectedGraph()
    minn = 2
    for i in range(L):
        g.AddNode(i)
    
    for i in range(L):
        on = 1
        getNext = i + on
        getPrev = i - on
        if getNext >= L:
            #print(getNext)
            getNext = getNext - L
        if getPrev < 0:
            #print(getPrev)
            getPrev = L + getPrev
        g.AddEdge(i,getNext)
        g.AddEdge(i,getPrev)
        
    for i in range(L):
        on = 2
        for j in range(Z-minn):
            n = 0
            if j%2 == 0:
                n = i + on
            else:
                n = i - on
                on += 1
            if n >= L:
                n = n - L
            if n < 0:
                n = L + n
            #print('added: '+str(i)+' to '+str(n))
            g.AddEdge(i,n)
        
        
    #Now random
    ran = int(p * L * int(Z/2))
    #print('Random Lines:' +str(ran))
    Edges = []
    start = 0
    end = 0
    edge = []
    #print(ran)
    for i in range(ran):
        dist = 0
        while (dist < Z/2 or edge in Edges) or dist != depth:
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            dist = int(getDist(L, start, end))
            edge = [start, end]
            if dist == depth:
                break
        g.AddEdge(start, end)
        Edges.append(edge)
    if show:
        NetGraphics.DisplayCircleGraph(g)
    return g
# ***** After building and testing your network class, build some    ***** #
# ***** Small World or Percolation networks, making use of the       ***** #
# ***** corresponding hints file. Then return to analyze these       ***** #
# ***** networks using the general-purpose routines you write below. ***** #

# ***** Small World exercise routines start here                     ***** #

# -----------------------------------------------------------------------
#
# Routines for finding path lengths on graphs: used by the Small World
# Network exercise only
#
# -----------------------------------------------------------------------

def FindPathLengthsFromNode(graph, node):
    """Breadth--first search. See "Six degrees of separation" exercise
    from Sethna's book.  Use a dictionary to store the distance to
    each node visited.  Keys in the dictionary thus serve as markers
    of nodes that have already been visited, and should not be considered
    again."""
    l = 0
    currentShell = [node] #graph.GetNeighbors(node)
    distances = {}
    nextShell = []
    while len(currentShell) > 0:
        #print(currentShell)
        for i in currentShell:
            added = False
            for key, value in distances.items():
                if i == key:
                    added = True
            n = []
            if added == False:
                distances[i] = l
                n = graph.GetNeighbors(i)
            for j in n:
                add = True
                for k in nextShell:
                    if k ==j:
                        add = False
                if add:
                    nextShell.append(j)
        currentShell = nextShell
        l += 1
        nextShell = []
    return distances

def FindAllPathLengths(graph):
    #which generates a list of all lengths (one per pair of nodes in the graph) 
    nodes = graph.GetNodes()
    distances = []
    included = []
    dists = []
    time1 = time.time()
    for n in nodes:
        #print(n)
        d = FindPathLengthsFromNode(graph, n)
        for key, value in d.items():
            point = [n, key]
            #point2 = [key, n]
            if point not in included:
                #print(str(point) +' is not in '+str(included))
                included.append([n, key])
                included.append([key, n])
                #print(str(value) +' between '+str(n)+' and '+str(key))
                distances.append([value,[n, key]])
                dists.append(value)
        #print(distances)
    timeToRun = time.time() - time1
    #print(timeToRun)
    return distances, dists

def FindAllPathLengthsFaster(graph):
    #which generates a list of all lengths (one per pair of nodes in the graph) 
    nodes = graph.GetNodes()
    distances = []
    included = []
    done = []
    dists = []
    time1 = time.time()
    for n in nodes:
        #print(n)
        d = FindPathLengthsFromNode(graph, n)
        for key, value in d.items():
            if key in done:
                continue
            point = [n, key]
            point2 = [key, n]
            if point in included:
                continue
            if point2 in included:
                continue
            #print(str(point) +' is not in '+str(included))
            included.append([n, key])
            dist = value
            distances.append([dist,point])
            dists.append(dist)
        done.append(n)
        #print(distances)
    timeToRun = time.time() - time1
    print(timeToRun)
    return distances, dists


def FindAverageAveragePathLength(graph):
    avglengths = []
    for i in graph:
        avglengths.append(FindAveragePathLength(i))
    avg = np.average(avglengths)
    
    sumSquared = 0
    for i in avglengths:
        sumSquared += (i - avg)**2
    if len(avglengths) > 1:
        dev = np.sqrt(sumSquared/(len(avglengths)-1))
    else:
        dev = 0
    return avg, dev
        
def FindAveragePathLength(graph):
    """Averages path length over all pairs of nodes"""
    dists = FindAllPathLengths(graph)[1]
    return np.average(dists)

# -----------------------------------------------------------------------
#
# Routine for calculating the clustering coefficient of a graph.
# This was a piece of the original Small World paper, but is not part of the 
# assigned exercise.
#
# -----------------------------------------------------------------------

def ComputeClusteringCoefficient(graph):
    """Computes clustering coefficient of graph"""
    pass

# -----------------------------------------------------------------------
#
# Routines for calculating "betweenness", which measures how many shortest
# paths between pairs of nodes on a graph pass through a given node or edge.
# Used in the Small Worlds exercise.
#
# References: (on the Web site)
# Mark E. J. Newman, "Scientific collaboration networks. ii. shortest paths,
# weighted networks, and criticality", Physical Review E 64: 016132, 2002.
# Michelle Girvan and Mark E. J. Newman, "Community structure in social
# and biological networks. Proceedings of the National Academy of Sciences
# 12, 7821-7826, 2002.
#
# -----------------------------------------------------------------------

def EdgeAndNodeBetweennessFromNode(graph, node):
    """
    Newman's edge and node betweenness inner loop
    Returns partial sum of edge, node betweenness
    """

    pass

def EdgeAndNodeBetweenness(graph):
    """Returns Newman's edge, node betweenness"""
    pass

# -----------------------------------------------------------------------
#
# Sample routines for reading in external files defining networks. Used
# primarily for the later portions of the Small World exercise.
#
# -----------------------------------------------------------------------

def ReadGraphFromEdgeFile(filename, conversion=None):
    """Reads file with (node1,node2) for each edge in graph"""
    pass

def ReadGraphFromNeighborFile(filename, conversion=None):
    """
    Reads file with [node1,node2,node3] for completely interconnected
    group of nodes (as in actors in a movie)
    Should be read in as a bipartite graph!
    """
    pass


# ***** Percolation exercise routines start here                     ***** #
# -----------------------------------------------------------------------
#
# Routines for finding clusters in networks. Used in the Percolation exercise.
#
# -----------------------------------------------------------------------

def FindClusterFromNode(graph, node, visited=None):
    """Breadth--first search
    The dictionary "visited" should be initialized to False for
    all the nodes in the cluster you wish to find
    It's used in two different ways.
    (1) It's passed back to the
        calling program with all the nodes in the current cluster set to
        visited[nodeInCluster]=True, so that the calling program can skip
        nodes in this cluster in searching for other clusters.
    (2) It's used internally in this algorithm to keep track of the
        sites in the cluster that have already been found and incorporated
    See "Building a Percolation Network" in text for algorithm"""
    pass

def FindAllClusters(graph):
    """For example, find percolation clusters
    Set up the dictionary "visited" for FindClusterFromNode
    Set up an empty list "clusters"
    Iterate over the nodes;
        if it haven't been visited,
            find the cluster containing it
            append it to the cluster list
        return clusters
    Check your answer using
    NetGraphics.DrawSquareNetworkBonds(g, cl) and
    NetGraphics.DrawSquareNetworkSites(g, cl)

    Optional: You may wish to sort your list of clusters according to their
    lengths, biggest to smallest
    For a list ell, the built-in method ell.sort() will sort the list
    from smallest to biggest;
    ell.sort(cmp) will sort the list according to the comparison function
    cmp(x, y) returns -1 if x < y, returns 0 if x==y, and returns 1 if x>y
    Define ReverseLengthCompare to compare two lists according to the
    unusual definition of inequality, l1<l2 if # len(l1) > len(l2)!
    """
    pass

def GetSizeDistribution(clusters):
    """Given the clusters, makes up a dictionary giving the number
    of clusters of a given size.
    """
    pass

# Copyright (C) Cornell University
# All rights reserved.
# Apache License, Version 2.0


    


# In[11]:


g = UndirectedGraph()


# In[12]:


g.HasNode(2)


# In[13]:


g.AddNode(2)


# In[14]:


g.HasNode(2)


# In[15]:


g.HasNode(3)


# In[16]:


g.HasNode(2)


# In[17]:


g.AddEdge(3,4)


# In[18]:


g.AddEdge(3,4)


# In[19]:


g.AddEdge(3,4)


# In[20]:


g.GetNodes()


# In[21]:


g.GetNeighbors(4)


# In[22]:


g.GetNodes()


# In[23]:


penta = pentagraph()


# In[24]:


c8 = circle8()


# In[25]:


FindPathLengthsFromNode(c8, 0)


# In[26]:


FindPathLengthsFromNode(penta, 0)


# In[27]:


allPenta = FindAllPathLengths(penta)


# In[202]:


sw = smallWorldNetwork(20,4,0)


# In[200]:


sw = smallWorldNetwork(30,30,0)


# In[55]:


sw = smallWorldNetwork(1000,2,0)


# # Number 2 on http://pages.physics.cornell.edu/~myers/teaching/ComputationalMethods/ComputerExercises/SmallWorld/SixDegreesOfSeparation.pdf

# In[56]:


allSW = FindAllPathLengths(sw)


# In[57]:


print(allSW)


# In[498]:


test = smallWorldNetwork(100,2,0)


# In[499]:


allTest = FindAllPathLengths(test)
#print(allTest[1])


# In[500]:


plt.hist(allTest[1], bins = 101)
plt.show()


# In[522]:


number2p1p1 = smallWorldNetworkSpecific(100,2,.01, depth = 5)


# In[523]:


number2p1p2 = smallWorldNetworkSpecific(100,2,.01, depth = 30)


# In[524]:


number2p1 = smallWorldNetworkSpecific(100,2,.01, depth=50)


# In[526]:


allTest = FindAllPathLengths(number2p1)
allTest2 = FindAllPathLengths(number2p1p1)
allTest3 = FindAllPathLengths(number2p1p2)
#print(allTest[1])


# In[527]:


plt.hist(allTest[1], bins = 101)
plt.hist(allTest2[1], bins = 101)
plt.hist(allTest3[1], bins = 101)
plt.show()


# In[531]:


plt.title('One line, long')
plt.hist(allTest[1], bins = 101)
plt.show()

plt.title('One line, short')
plt.hist(allTest2[1], bins = 101)
plt.show()

plt.title('One line, medium')
plt.hist(allTest3[1], bins = 101)
plt.show()


# So this tells me that longer lines are more important for reducing number of moves to connect the nodes... Anyways, let's find the six degrees of separation

# In[532]:


number2p2 = smallWorldNetwork(100,2,1.15)


# In[495]:


allTest = FindAllPathLengths(number2p2)


# In[496]:


plt.hist(allTest[1], bins = 101)
plt.show()


# **Six degrees of separation**
# various somewhat uncontrolled studies have shown that any random pair of people in
# the world can be connected to one another by a
# short chain of people (typically around six), each of
# whom knows the next fairly well.

# In[572]:


sixdeg = smallWorldNetworkLong(100,2,1.06)


# In[573]:


allTest = FindAllPathLengths(sixdeg)
plt.hist(allTest[1], bins = 101)
plt.show()


# **I found at a p = 1.06 we get six degrees of separation which means there are 106 connections/shortcuts which represents that each node has a relationship with 2 people (from the start, the person to the node's left and to the node's right) as well as an additional 2 people. That means everyone knows at least 2 people and on average everyone knows 2 + 106*2/100 people = 4.12 people on average. (Note multiply by 2 because each connection connects 2 people) This is not always going to give us six degrees of separation because it is randomly assigned the relationships. What does matter, in any case, is that the distances in relationships are randomly dispersed between short and long**
# 

# # Aside: let's see the difference between short paths and long paths

# In[321]:


depth50 = smallWorldNetworkSpecific(100,2,.02,depth=50)


# In[323]:


allTest = FindAllPathLengths(depth50)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 0.02 so 2 shortcuts')
plt.show()


# Distances are shorter

# In[324]:


depth5 = smallWorldNetworkSpecific(100,2,.02,depth=5)


# In[325]:


allTest = FindAllPathLengths(depth5)
plt.hist(allTest[1], bins = 101)
plt.title('Short relationships, p = 0.02 so 2 shortcuts')
plt.show()


# This seems really close to when we have no shortcuts! So short shortcuts are neglible?

# In[326]:


depth50pt2 = smallWorldNetworkSpecific(100,2,.2,depth=50)


# In[328]:


depth5pt2 = smallWorldNetworkSpecific(100,2,.2,depth=5)


# In[533]:


allTest = FindAllPathLengths(depth50pt2)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 0.2, many shortcuts')
plt.show()

allTest = FindAllPathLengths(depth5pt2)
plt.hist(allTest[1], bins = 101)
plt.title('Short relationships, p = 0.2, many shortcuts')
plt.show()


# This is convincing that long relationships are more meaningful than short... So:

# With long relationships, what p do we need for 6 degrees? It should be less than 1.06, right?

# In[558]:


long1 = smallWorldNetworkLong(100,2,1.5,depth=41)
long2 = smallWorldNetworkLong(100,2,1.3,depth=41, show=False)
long3 = smallWorldNetworkLong(100,2,1.06,depth=41, show=False)
long4 = smallWorldNetworkLong(100,2,2,depth=41, show=False)


# In[559]:


allTest = FindAllPathLengths(long3)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 1.06, many shortcuts')
plt.show()

allTest = FindAllPathLengths(long2)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 1.3, many shortcuts')
plt.show()

allTest = FindAllPathLengths(long1)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 1.5, many shortcuts')
plt.show()

allTest = FindAllPathLengths(long4)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 2, many shortcuts')
plt.show()


# With lines that are really big, we need a p = 2 to get 6 degrees of separation.

# **Conclusion: You need randomness, long relationships, and short relationships in order to achieve 6 degrees of separation. Think about it...**
# 
# If I am trying to give a package to someone in Beijing, and I have a friend who lives somewhere in Beijing (long relationship), so I give him the package. If we have a graph like implemented above, then he only knows someone far away, too, so he has to give the package to someone in Paris. IF we had both short and long relationships then he could give it to someone else in China that is closer to the person I am trying to give the package to. Instead, since he only knows people far from him, which is also unrealistic, he has to ship it to Paris and hope someone in Paris knows the person I am looking for in China.

# **Now I am going to graph max length vs minimum relationship length at a constant p of 1.06**

# In[581]:


depths = np.linspace(0,45,46)
#print(depths)
xs = []
xs2 = []
for i in depths:
    #print(i)
    sw = smallWorldNetworkLong(100,2,1.06,depth=i, show=False)
    xs.append(max(FindAllPathLengths(sw)[1]))
    xs2.append(FindAveragePathLength(sw))


# In[582]:


plt.xlabel('Minmum length of relationships')
plt.ylabel('Maximum distance of separation')
plt.title('Max distance of separation vs minimum length of relationship')
plt.plot(depths, xs, '.')
plt.show()


# The graph above shows that when the minimum length of relationships is between 0 and 35, we can get six degrees of separation at a p = 1.06, however when we have only long relationships like at p = 40 and above, it gets increasingly unlikely.

# In[584]:


plt.xlabel('Minmum length of relationships')
plt.ylabel('Average length of separation')
plt.title('Average distance of separation vs average length of relationship')
plt.plot(depths, xs2, '.')
plt.show()


# **Shows an increase of length as the minumum length of relationship increases**

# In[482]:


L=200
Z=4
p=.1
linesPerNode = Z + (p * L * Z / 2) / L
perfect1 = smallWorldNetworkLong(L, Z, p)


# In[483]:


print(str(linesPerNode)+' lines per node')
allTest = FindAllPathLengths(perfect1)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 1.05, many shortcuts')
plt.show()


# In[484]:


L=200
Z=2
p=2.2
linesPerNode = Z + (p * L * Z / 2) / L
compare1 = smallWorldNetwork(L, Z, p)


# In[485]:


print(str(linesPerNode)+' lines per node')
allTest = FindAllPathLengths(compare1)
plt.hist(allTest[1], bins = 101)
plt.title('Long relationships, p = 1.05, many shortcuts')
plt.show()


# **Since short relationships in real life are more likely, does our distribution show this?** Let's look at average length for this

# # End Aside

# In[208]:


test10001 = smallWorldNetwork(300,2,0.02, show=False)
print('1')
test10002 = smallWorldNetwork(300,2,0.2, show=False)
print('2')
test10003 = smallWorldNetwork(300,2,1.05, show=False)
print('3')
test10004 = smallWorldNetwork(300,2,2, show=False)
print('4')
gr1 = FindAllPathLengths(test10001)
print('resulted 1')
gr2 = FindAllPathLengths(test10002)
print('resulted 2')
gr3 = FindAllPathLengths(test10003)
print('resulted 3')
gr4 = FindAllPathLengths(test10004)
print('resulted 3')


# In[236]:


test10005 = smallWorldNetwork(300,2,0, show=False)
gr5 = FindAllPathLengths(test10005)


# In[238]:


test1006 = smallWorldNetwork(300,2,0, show=False)
gr6 = FindAllPathLengthsFaster(test1006)


# In[259]:


plt.title('p = 0.02')
plt.hist(gr1[1], bins=85)
plt.show()


# In[288]:


plt.title('p = 1.05')
plt.hist(gr3[1], bins=85)
plt.show()


# In[289]:


plt.title('p = 2')
plt.hist(gr4[1], bins=85)
plt.show()


# **So here, there are 2 * 300 * 2 /2 = 600 short cuts. That means on average, everyone knows 2 + 600*2/300 = 6.**
# 
# With a p of 1.05 we get: 1.05 * 300 * 2 / 2 = 315 short cuts so on average: 2 + 315 * 2/ 300 = 4.1
# 
# With a p  of 1.15 we get: 345 short cuts.... 2 + 345 * 2 / 300 = 4.3 on average. LETS TRY IT:

# In[290]:


test10008 = smallWorldNetwork(300,2,1.15, show=False)
gr8 = FindAllPathLengths(test10008)
plt.title('p = 1.15')
plt.hist(gr8[1], bins=85)
plt.show()


# In[260]:


plt.hist(gr6[1], bins=150)
plt.show()


# # Problem 3: Average length

# **FindAveragePathLength(graph). Try L = 100, Z = 2, p = .1, and average should be around l = 10, why does it vary?**

# In[168]:


number3p1 = smallWorldNetwork(100,2,.1)


# In[171]:


FindAveragePathLength(number3p1)


# In[172]:


number3p1p2 = smallWorldNetwork(100,2,.1)


# In[175]:


FindAveragePathLength(number3p1p2)


# In[176]:


number3p1p3 = smallWorldNetwork(100,2,.1)
print(FindAveragePathLength(number3p1p3))


# **There are huge amounts of variation in the random shortcuts which leads to the variation in the average lengths...**

# What is average length for the p we found for six degrees of separation? 1.06 = p.

# In[574]:



print(FindAveragePathLength(sixdeg))


# **Use FindAverageAveragePathLength on several random small world networks with L=100,Z=2, and p=0.1. How wildly do these fluctuate?**

# In[657]:


smallWorlds = []
for i in np.arange(30):
    smallWorlds.append(smallWorldNetwork(100,2,.1, show=False))
print(FindAverageAveragePathLength(smallWorlds))


# **(c) Plot the average path length between nodes l(p)
# divided by l(p = 0) for Z = 2, L = 50, with p on a
# semi-log plot from p = 0.001 to p = 1. (Hint: Your
# curve should be similar to that of with Watts and
# Strogatz [142, fig. 2], with the values of p shifted
# by a factor of 100; see the discussion of the continuum limit below.) Why is the graph fixed at one
# for small p?**

# In[399]:


ps = 10**(-1 * np.linspace(0,3,100))
Z = 2
L = 50
lp0 = FindAveragePathLength(smallWorldNetwork(L,Z,0, show=False))
xs = []
for p in ps:
    x = FindAveragePathLength(smallWorldNetwork(L,Z,p, show=False))
    xs.append(x/lp0)


# In[402]:


plt.semilogx(ps,xs, '.')
plt.ylabel('Average l / lp0')
plt.xlabel('p')
plt.title('semilogx of the average length vs p')
plt.show()


# Why is the graph fixed at one for small p?
# 
# Because for small p, the amount of shortcuts added is 0 until around 10**-1.4
# 
# **Large N and the emergence of a continuum limit** This shows that no shortcuts are added for a really small p and they are identical to having a p=0. This is the idea that the number of shortcuts is proportional to the equation of shortcuts = p * L * Z / 2, so if p is really small, L * Z needs to be really big. As L increases, p can decrease proportionally to have the same number of shortcuts. This idea is explored below.

# In[242]:


smallWorldNetwork(L,Z,10**-1)


# In[243]:


smallWorldNetwork(L,Z,10**-2)


# In[244]:


smallWorldNetwork(L,Z,10**0)


# # D: Create and display a circle graph of your geometry from part (c) 
# (Z = 2, L = 50) at p = 0.1; create and display circle graphs of Watts and Strogatz’s geometry (Z = 10, L = 1000) at p = 0.1 and
# p = 0.001. Which of their systems looks statistically more similar to yours? 

# In[253]:


Z= 2
L = 50
p = .1
smallWorldNetwork(L,Z,p)


# In[246]:


print('Watts and Strogatz’s geometry (Z = 10, L = 1000) at p = 0.1')
Z=10
L=1000
p=.1

smallWorldNetwork(L,Z,p)


# In[264]:


print('Watts and Strogatz’s geometry (Z = 10, L = 1000) at p = 0.001')
Z=10
L=1000
p=.0015

smallWorldNetwork(L,Z,p)


# Using a p = 0.001 for Watts and Strogatz's geometry reflects ours better of using a p = 0.1. In fact, using a p=0.0015 is almost identical and that is because of ratios. Below, shows the smiliar graphs with a varied p:

# In[404]:


Z= 2
L = 50
p = .1
print('Z = 2, L = 50) at p = .1')
print('Mathematically: shortcuts = .1 * 2 * 50 / 2 = 5')
smallWorldNetwork(L,Z,p)


# In[405]:


print('Watts and Strogatz’s geometry (Z = 10, L = 1000) at p = 0.001)')
print('Mathematically: shortcuts = 0.001 * 10 * 1000 / 2 = 5')
print('We have to decrease p by a factor of 100 because L * Z increases by a fact of 10')
Z=10
L=1000
p=.0015

smallWorldNetwork(L,Z,p)


# **Plot (perhaps using the scaling collapse routine provided) the rescaled
# average path length πZL/2 versus the total number
# of shortcuts pLZ/2, for a range 0.001 < p < 1, for
# L = 100 and 200, and for Z = 2 and 4.**

# In[637]:


swTest = smallWorldNetwork(10,2,.2)


# In[638]:


results22 = FindAllPathLengths(swTest)


# In[639]:


print(results22)


# In[711]:


sw = smallWorldNetworkSpecific(100,2,1.06,depth=30)
resultsLong1 = FindAllPathLengths(sw)
plt.hist(resultsLong1[1], bins = 16)
plt.title('Long relationships, p = 1.5')
plt.xlabel('Steps Taken (Lines Traveled)')
plt.ylabel('Frequency')
plt.show()

