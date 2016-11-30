import random

class Graph:
    """
    Directed Graph Class
    
    A graph is modelled as a dictionary that maps a vertex
    to the list of neighbours of that vertex.
    
    From the Jan 22/23 lectures.
    """

    def __init__(self, vertices = set(), edges = list()):
        """
        Construct a graph with a shallow copy of
        the given set of vertices and given list of edges.

        Efficiency: O(# vertices + # edges)
        for game: # nodes + edges = nodes + # possible roads

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g._alist.keys() == {1,2,3}
        True
        >>> g._alist[1] == [2]
        True
        >>> g._alist[2] == [3]
        True
        >>> g._alist[3] == []
        True
        >>> h1 = Graph()
        >>> h2 = Graph()
        >>> h1.add_vertex(1)
        >>> h2._alist.keys() == set()
        True
        """

        self._alist = dict()

        for v in vertices:
            self.add_vertex(v)
        for e in edges:
            self.add_edge(e)

    def add_vertex(self, v):
        """
        Add a vertex v to the graph.
        If v exists in the graph, do nothing.

        Efficiency: O(1)

        >>> g = Graph()
        >>> len(g._alist)
        0
        >>> g.add_vertex(1)
        >>> g.add_vertex("vertex")
        >>> "vertex" in g._alist
        True
        >>> 2 in g._alist
        False
        >>> h = Graph({1,2}, [(1,2)])
        >>> h.add_vertex(1)
        >>> h._alist[1] == [2]
        True
        """
        
        if v not in self._alist:
            self._alist[v] = list()

    def add_edge(self, e):
        """
        Add edge e to the graph.
        Raise an exception if the endpoints of
        e are not in the graph.

        Efficiency: O(1)

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_edge((1,2))
        >>> 2 in g._alist[1]
        True
        >>> 1 in g._alist[2]
        False
        >>> g.add_edge((1,2))
        >>> g._alist[1] == [2,2]
        True
        """

        if not self.is_vertex(e[0]) \
          or not self.is_vertex(e[1]):
            raise ValueError("an endpoint is not in graph")

        self._alist[e[0]].append(e[1])

    def is_vertex(self, v):
        """
        Check if vertex v is in the graph.
        Return True if it is, False if it is not.
        
        Efficiency: O(1) - Sweeping some discussion
        about hashing under the rug.

        >>> g = Graph({1,2})
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(3)
        False
        >>> g.add_vertex(3)
        >>> g.is_vertex(3)
        True
        """
        return v in self._alist

    def is_edge(self, e):
        """
        Check if edge e is in the graph.
        Return True if it is, False if it is not.

        Efficiency: O(# neighbours of e[0])

        >>> g = Graph({1,2}, [(1,2)])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.add_edge((1,2))
        >>> g.is_edge((1,2))
        True
        """

        if e[0] not in self._alist:
            return False
        else:
            return e[1] in self._alist[e[0]]

    def neighbours(self, v):
        """
        Return a list of neighbours of v.
        A vertex u appears in this list as many
        times as the (v,u) edge is in the graph.

        If v is not in the graph, then
        raise a ValueError exception.

        Efficiency: O(1)

        >>> Edges = [(1,2),(1,4),(3,1),(3,4),(2,4),(1,2)]
        >>> g = Graph({1,2,3,4}, Edges)
        >>> g.neighbours(1)
        [2, 4, 2]
        >>> g.neighbours(4)
        []
        >>> g.neighbours(3)
        [1, 4]
        >>> g.neighbours(2)
        [4]
        """

        if not self.is_vertex(v):
            raise ValueError("vertex not in graph")
        
        return self._alist[v]

    def vertices(self):
        """
        Returns the set of vertices in the graph.

        Efficiency: O(# vertices)

        >>> g = Graph({1,2})
        >>> g.vertices() == {1,2}
        True
        >>> g.add_vertex(3)
        >>> g.vertices() == {1,2,3}
        True
        """

        # dict.keys() is not exactly a set, so we have to create
        # one before returning
        return set(self._alist.keys()) 

    def edges(self):
        """
        Returns a list of tuples (u,v) corresponding to
        edges in the graph. Multiple copies of an edge in the graph
        appear in the returned list just as many times.

        Efficiency: O((# vertices) + (# edges))

        >>> g = Graph({1,2,3},[(1,2),(2,3),(1,3)])
        >>> set(g.edges()) == {(1,2),(2,3),(1,3)}
        True
        >>> g.add_edge((3,1))
        >>> set(g.edges()) == {(1,2),(2,3),(1,3),(3,1)}
        True
        >>> h = Graph({1,2},[(1,2),(1,2)])
        >>> h.edges() == [(1,2),(1,2)]
        True
        """

        # iterates over tuples (v,nbrs) where v is a key and nbrs = _alist[v]
        e = []
        for v,nbrs in self._alist.items():
            e.extend([(v,u) for u in nbrs])
        return e


#END OF CLASS DEFINITION

def is_walk(g, walk):
    """
    Given a graph 'g' and a list 'walk', return true
    if 'walk' is a walk in g.

    Recall a walk in a graph is a nonempty
    sequence of vertices
    in the graph so that consecutive vertices in the
    sequence are connected by a directed edge
    (in the correct direction)

    Efficiency: O((max neighbourhood size) * (walk length))

    >>> Edges = [(1,2),(1,3),(2,5),(3,4),(4,2),(5,4)]
    >>> g = Graph({1,2,3,4,5}, Edges)
    >>> is_walk(g, [3,4,2,5,4,2])
    True
    >>> is_walk(g, [5,4,2,1,3])
    False
    >>> is_walk(g, [2])
    True
    >>> is_walk(g, [])
    False
    >>> is_walk(g, [1,6])
    False
    >>> is_walk(g, [6])
    False
    """
    
    if not walk:
        return False

    if len(walk) == 1:
        return g.is_vertex(walk[0])

    # num iterations = O(len(walk))
    for i in range(len(walk)-1):
        # body of loop takes O(# neigbours of walk[i]) time
        if not g.is_edge((walk[i], walk[i+1])):
            return False

    return True

def is_path(g, path):
    """
    Given a graph 'g' and a list 'path', return true
    if 'path' is a path in g.

    Recall a path is a walk that does not visit
    a vertex more than once.

    Efficiency: O((max neighbourhood size) * (path length))

    >>> Edges = [(1,2),(1,3),(2,5),(3,4),(4,2),(5,4)]
    >>> g = Graph({1,2,3,4,5}, Edges)
    >>> is_path(g, [3,4,2,5,4,2])
    False
    >>> is_path(g, [3,4,2,5])
    True
    """

    # O(path length)
    if len(set(path)) < len(path):
        return False

    # O((# edges) * (path length))
    return is_walk(g, path)

def search(g, v):
    """
    Given a graph g and a vertex v of g, return a dictionary
    'reached' whose keys are the vertices that can be reached
    from v and reached[u] is the vertex that discovered u
    in the search (and reached[v] = v).

    If v is not in the graph, raise a ValueError exception.

    Efficiency: O(# edges)

    >>> edges = [(1,2),(1,3),(2,3),(2,4),(3,5),(4,5),(5,3),(6,2),(6,4)]
    >>> g = Graph({1,2,3,4,5,6}, edges)
    >>> search(g, 1).keys() == {1,2,3,4,5}
    True
    >>> search(g, 4).keys() == {4,5,3}
    True
    >>> search(g, 6).keys() == {2,3,4,5,6}
    True
    """

    if not g.is_vertex(v):
        raise ValueError("vertex not in graph")

    reached = {v:v}
    stack = [v]

    # see lecture 6 notes on eClass for running time analysis
    while stack: 
        curr = stack.pop()
        for succ in g.neighbours(curr):
            if succ not in reached:
                reached[succ] = curr
                stack.append(succ)

    return reached
        
def find_path(g, start, end):
    """
    Given a graph g and two vertices start, end in g,
    return a path (as a list of vertices) from start to end.

    If there is no such path, return None.

    Efficiency: O(num edges)
    
    >>> edges = [(1,2),(1,3),(2,3),(2,4),(3,5),(4,5),(5,3),(6,2),(6,4)]
    >>> g = Graph({1,2,3,4,5,6}, edges)
    >>> path = find_path(g, 1, 5)
    >>> is_path(g, path) and path[0] == 1 and path[-1] == 5
    True
    >>> find_path(g, 5, 2)

    >>> find_path(g, 2, 2) == [2]
    True
    """
    
    reached = search(g, start)

    if end not in reached:
        return None

    path = [end]
    curr = end
    while curr != start:
        curr = reached[curr]
        path.append(curr)
    
    path.reverse()

    return path

def random_graph(n, m):
    """
    Generate a random graph with n vertices and m edges.
    Each edge (u,v) has both u and v chosen randomly
    among the n vertices.
    
    Useful for seeing how well the search performs on large graphs.

    Efficiency: O(n + m)
    """
    
    edges = [(random.randint(0,n-1),random.randint(0,n-1)) \
                 for i in range(m)]
    return Graph(set(range(n)), edges)
















            
