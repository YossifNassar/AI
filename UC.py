# Head ends here
import heapq
from ways import graph


def children(point,roads):
    j = roads[int(point)]
    lst = []
    for link in j.links:
        if type(link) is graph.Link:
            lst.append((link.target,link.distance))
        else:
            lst.append((link.target,link.cost))
    return lst


def ucs_aux(node, goal, roads,maxAdjacents,centrals=None):
    limit = len(roads.keys())
    stage = 0
    createdNodes = 1
    # Initialize the queue with the root node
    q = [(0, node.index, [])]
    # The list of seen items
    seen = {}
    nearestCentrals = {}
    # While the queue isn't empty
    while q:
        stage = stage + 1
        # Pop the cost, point and path from the queue
        cost, point, path = heapq.heappop(q)
        # If it has been seen, and has a lower cost, bail
        if seen.has_key(point) and seen[point][0] < cost:
            continue
        if centrals and str(point) in nearestCentrals:
            continue
        # Update the path
        path = path + [point]
        # If we have found the goal, return the point
        if goal == None:
            if len(seen) >= maxAdjacents and centrals is None:
                return (path,seen,None,createdNodes)
            if (len(nearestCentrals) >= maxAdjacents or stage >= limit) and centrals :
                return (path,nearestCentrals,None,createdNodes)
            if centrals and str(point) in centrals:
                nearestCentrals[point] = (cost, path)
        else:
            if point == goal.index:
                return (path,seen,cost,createdNodes)


        # Loop through the children
        for child in children(point,roads):
            # Calculate the basic cost
            child_cost = child[1]
            # If the child hasn't been seen
            if child[0] not in seen:
                # Add it to the heap
                createdNodes = createdNodes+1
                heapq.heappush(q, (cost + child_cost, child[0], path))
        # Add the point to the seen items
        seen[point] = (cost,path)

    if centrals:
        return (None,nearestCentrals,None,createdNodes)
    return (None,seen,None,createdNodes)


def ucs_aux_experience(node, goal, roads,maxAdjacents,centrals=None):
    limit = len(roads.keys())
    stage = 0
    createdNodes = 1
    # Initialize the queue with the root node
    q = [(0, node.index)]
    # The list of seen items
    seen = {}
    nearestCentrals = {}
    # While the queue isn't empty
    while q:
        stage = stage + 1
        # Pop the cost, point and path from the queue
        cost, point = heapq.heappop(q)
        # If it has been seen, and has a lower cost, bail
        if seen.has_key(point) and seen[point][0] < cost:
            continue
        if centrals and str(point) in nearestCentrals:
            continue
        # If we have found the goal, return the point
        if goal == None:
            if len(seen) >= maxAdjacents and centrals is None:
                return (seen,None,createdNodes)
            if (len(nearestCentrals) >= maxAdjacents or stage >= limit) and centrals :
                return (nearestCentrals,None,createdNodes)
            if centrals and str(point) in centrals:
                nearestCentrals[point] = (cost)
        else:
            if point == goal.index:
                return (seen,cost,createdNodes)


        # Loop through the children
        for child in children(point,roads):
            # Calculate the basic cost
            child_cost = child[1]
            # If the child hasn't been seen
            if child[0] not in seen:
                # Add it to the heap
                createdNodes = createdNodes+1
                heapq.heappush(q, (cost + child_cost, child[0]))
        # Add the point to the seen items
        seen[point] = (cost)

    if centrals:
        return (nearestCentrals,None,createdNodes)
    return (seen,None,createdNodes)

#returns path
def ucs(start,goal,roads):
    res=ucs_aux(start,goal,roads,0)
    return res[0]


#returns  cost , createdNodes
def ucs_expirement(start,goal,roads):
    res = ucs_aux(start,goal,roads,0)
    return res[1],res[2]


# returns a list of (index,path)
def nearest(v,maxAdjacents,roads):
    dict = ucs_aux(v,None,roads,maxAdjacents+1)[1]
    del dict[v.index]
    return [(k,v[1]) for k,v in dict.iteritems()]


# returns a list of (index,(cost,path))
def nearest_with_cost(v,maxAdjacents,roads,centrals=None):
    dict = ucs_aux(v,None,roads,maxAdjacents+1,centrals)[1]
    return [(k,v) for k,v in dict.iteritems()]
