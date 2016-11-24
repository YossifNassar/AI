from ways import info
import collections
import math
from ways import load_map_from_csv
import utils
import random
import numpy
import collections
import datetime
import UC
import pickle
import sys
from ways import graph

PATHS = 500000
P = 0.99
M = 0.1
DATA_SET_LENGTH = 20
DATA_SET_ADGACENTS = 30000
DATA_SET_OPERATIONS = 200

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

def air_distance(sourceIndex,destIndex,roads):
    sourceNode = roads[sourceIndex]
    destNode = roads[destIndex]
    delta_x = sourceNode.lat - destNode.lat
    delta_y = sourceNode.lon - destNode.lon
    return float(math.sqrt( math.pow(delta_x,2) + math.pow(delta_y,2)))


def load_centrality(filename='centrality.csv'):
    import csv
    lst = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append((row[0], row[1]))
    return lst


def flip_coin():
    return numpy.random.choice(numpy.arange(0, 2), p=[1 - P, P])


def random_node(roads):
    return random.choice(roads.junctions())


def build_path(node, roads, allNodes):
    while (flip_coin() == 1) and (node.links != []):
        allNodes.append(node.index)
        link = random.choice(node.links)
        node = roads[link.target]


def print_path(path):
    lst = []
    for j in path:
        lst.append(j.index)
    print lst


def buildCentrality():
    roads = load_map_from_csv()
    allNodes = []
    for i in range(PATHS):
        print str((float(i) / PATHS) * 100) + "% percent done... Now in path number: " + str(i)
        node = random_node(roads)
        build_path(node, roads, allNodes)
    f = open('centrality.csv', 'w');
    for t in collections.Counter(allNodes).most_common():
        f.write(str(t[0]) + "," + str(t[1]) + "\n")
    f.close()


def build_abstract_space(centrals,K, roads):
    dict = {}
    # UC.nearest(roads[int(0)], 3, roads)
    for central in centrals:
        lst = UC.nearest_with_cost(roads[int(central)], M * len(centrals), roads)
        abstractLst=[]
        for item in lst:
            abstractLst.append(graph.AbstractLink(item[1][1],item[0],item[1][0],-1))
        dict[int(central)] = abstractLst
    pickle.dump(dict, open("abstractSpace.pkl", "wb"))


def build_data_set(roads):
    pairs = {}
    f = open('dataSet.csv', 'w')
    for i in range(DATA_SET_LENGTH):
        keepDigging = True
        while keepDigging:
            id1 = random.choice(roads.keys())
            id2 = -1
            if pairs.has_key(id1):
                continue
            v = roads[id1]
            nearest = UC.nearest(v, DATA_SET_ADGACENTS, roads)
            if not nearest:
                continue
            for item in nearest:
                if len(item[1]) >= DATA_SET_OPERATIONS:
                    id2 = item[0]
                    keepDigging = False
            if not keepDigging:
                pairs[id1] = id2
                f.write(str(id1) + "," + str(id2) + "\n")
    f.close()


def test_dataset(roads):
    passed = True
    import csv
    with open('dataSet.csv', 'rb') as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            length = len(UC.ucs(roads[int(row[0])], roads[int(row[1])], roads))
            if length < DATA_SET_OPERATIONS:
                print length
                passed = False
    if passed:
        print "Test Passed!"
    else:
        print "Test Failed!"


def find_min(nearestCentrals):
    minCost = nearestCentrals[0][1][0]
    id = nearestCentrals[0][0]
    for item in nearestCentrals:
        if item[1][0] < minCost:
            minCost = item[1][0]
            id = item[0]
    return id


def nearest_central(v, centrals, roads):
    nearest = UC.nearest_with_cost(v, sys.maxsize, roads)
    nearestCentrals = filter(lambda pair: str(pair[0]) in centrals, nearest)
    return find_min(nearestCentrals)

def nearest_central_air(v,centrals,roads):
    minDistance = utils.air_distance(int(centrals[0]),int(v.index),roads)
    minIndex = centrals[0]
    for centralIndex in centrals:
        d = utils.air_distance(int(centralIndex),int(v.index),roads)
        if d < minDistance:
            minDistance = d
            minIndex = centralIndex
    return minIndex

