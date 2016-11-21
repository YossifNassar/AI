import ways.graph
from ways import info
import collections

def num_of_junctions(roads):
    return len(roads)

def num_of_links(roads):
    cnt = 0
    for link in roads.iterlinks():
        cnt += 1
    return cnt

def link_type_histogram(roads):
    lst=[]
    for link in roads.iterlinks():
        lst.append(info.ROAD_TYPES[link.highway_type])
    return collections.Counter(lst)


def link_distance(roads):
    max = 0.0
    min = 0.0
    avg = 0.0
    sum = 0.0
    for link in roads.iterlinks():
        d = float(link.distance)
        if (d >= max):
            max = d
        if (min >= d):
            min = d
        sum += d
    avg = sum / num_of_junctions(roads)
    return [max,min,avg]

def branch_factors(roads):
    max = 0
    min = 0
    avg = 0.0
    sum = 0.0
    for j in roads.junctions():
        bF = len(j.links)
        if (bF >= max):
            max = bF
        if (min >= bF):
            min = bF
        sum += bF
    avg = sum / num_of_junctions(roads)
    return [max, min, avg]


def questionB():
    print "Hello world"