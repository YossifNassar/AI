# Head ends here
import heapq
from ways import graph

def children(point,roads,centrals=None):
    j = roads[int(point)]
    lst = []
    for link in j.links:
        if centrals and not str(link.target) in centrals:
            continue
        if type(link) is graph.Link:
            lst.append((link.target,link.distance))
        else:
            lst.append((link.target,link.cost))
    return lst

#maxSeen number of maximum
def ucs_aux(node, goal, roads,maxAdjacents,centrals=None):
    createdNodes = 1
    # Initialize the queue with the root node
    q = [(0, node.index, [])]
    # The list of seen items
    seen = {}
    # While the queue isn't empty
    while q:
        # Pop the cost, point and path from the queue
        cost, point, path = heapq.heappop(q)
        # If it has been seen, and has a lower cost, bail
        if seen.has_key(point) and seen[point][0] < cost:
            continue
        # Update the path
        path = path + [point]
        # If we have found the goal, return the point
        if goal == None:
            if len(seen) >= maxAdjacents:
                return (path,seen,None,createdNodes)
        else:
            if point == goal.index:
                return (path,seen,cost,createdNodes)

        # Loop through the children
        for child in children(point,roads,centrals):
            # Calculate the basic cost
            child_cost = child[1]
            # If the child hasn't been seen
            if child[0] not in seen:
                # Add it to the heap
                createdNodes = createdNodes+1
                heapq.heappush(q, (cost + child_cost, child[0], path))
        # Add the point to the seen items
        seen[point] = (cost,path)
    return (None,seen,None,createdNodes)

#returns path
def ucs(start,goal,roads):
    return ucs_aux(start,goal,roads,0)[0]

#returns path , cost , createdNodes
def ucs_expirement(start,goal,roads):
    res = ucs_aux(start,goal,roads,0)
    return res[0], res[2],res[3]

# returns a list of (index,path)
def nearest(v,maxAdjacents,roads):
    dict = ucs_aux(v,None,roads,maxAdjacents+1)[1]
    del dict[v.index]
    return [(k,v[1]) for k,v in dict.iteritems()]

# returns a list of (index,(cost,path))
def nearest_with_cost(v,maxAdjacents,roads,centrals=None):
    dict = ucs_aux(v,None,roads,maxAdjacents+1,centrals)[1]
    del dict[v.index]
    return [(k,v) for k,v in dict.iteritems()]
