import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import numpy.random as rand
import time



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
        #print(i)
        while (dist < Z/2 or edge in Edges) or dist != depth:
            start = rand.randint(0,L)
            end = rand.randint(0,L)
            dist = np.abs(start-end)
            edge = [start, end]
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
            '''if point not in included:
                #print(str(point) +' is not in '+str(included))
                included.append([n, key])
                included.append([key, n])
                dist = value
                distances.append([dist,point])
                dists.append(dist)'''
            
            if point not in included:
                #print(str(point) +' is not in '+str(included))
                included.append([n, key])
                included.append([key, n])
                print(str(value) +' between '+str(n)+' and '+str(key))
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
    

def FindAveragePathLength(graph, include0 = True):
    """Averages path length over all pairs of nodes"""
    if include0:
        dists = FindAllPathLengths(graph)[1]
        return np.average(dists)
    else:
        dists = FindAllPathLengths(graph)[1]
        dr = []
        for i in dists:
            if i != 0:
                dr.append(i)
        return np.average(dr)
    
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


