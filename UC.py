# Head ends here
import heapq

def children(point,roads):
    lst = []
    for link in point.links:
        lst.append((roads[link.target],link.distance))
    return lst

#maxSeen number of maximum
def ucs_aux(node, goal, roads,maxAdjacents):
    # Initialize the queue with the root node
    q = [(0, node, [])]
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
        if point == goal or (len(seen) >= maxAdjacents and goal==None):
            return (path,seen)
        # Loop through the children
        for child in children(point,roads):
            # Calculate the basic cost
            child_cost = child[1]
            # If the child hasn't been seen
            if child[0] not in seen:
                # Add it to the heap
                heapq.heappush(q, (cost + child_cost, child[0], path))
        # Add the point to the seen items
        seen[point] = (cost,path)
    return (None,seen)

def ucs(start,goal,roads):
    return ucs_aux(start,goal,roads,0)[0]

def nearest(v,maxAdjacents,roads):
    lst = ucs_aux(v,None,roads,maxAdjacents+1)[1]
    l = []
    for u in lst:
        if not u.index == v.index:
            l.append(u)
    return l