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




def build_abstract_map(centrals,roads):
    dict = {}
    # UC.nearest(roads[int(0)], 3, roads)
    for central in centrals:
        lst = UC.nearest_with_cost(roads[int(central)], M * len(centrals), roads,centrals)
        abstractLst=[]
        for item in lst:
            abstractLst.append(graph.AbstractLink(item[1][1],int(item[0]),float(item[1][0]),-1))
        junc = roads[int(central)]
        dict[int(central)] = graph.Junction(junc.index,junc.lat,junc.lon, abstractLst)
    return dict


#builds abstract space pickle
def build_abstract_space(centrals, roads, file="abstractSpace.pkl"):
    pickle.dump(build_abstract_map(centrals,roads), open(file, "wb"))




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
    nearest = UC.nearest_with_cost(v, 1, roads,centrals)
    nearestCentrals = filter(lambda pair: str(pair[0]) in centrals, nearest)
    return find_min(nearestCentrals)


def nearest_central_air(v,centrals,roads):
    minDistance = utils.air_distance(int(centrals[0]),int(v.index),roads)
    minIndex = centrals[0]
    for centralIndex in centrals:
        if int(v.index) == int(centralIndex):
            continue
        d = utils.air_distance(int(centralIndex),int(v.index),roads)
        if d < minDistance:
            minDistance = d
            minIndex = centralIndex
    return minIndex




def get_centrals_list(K):
    lst = utils.load_centrality()
    centralsCount = K * len(lst)
    centrals = lst[:int(centralsCount)]
    centralsLst = map(lambda x: x[0], centrals)
    return centralsLst


def base(source,target):
    roads = load_map_from_csv()
    return UC.ucs(roads[int(source)],roads[int(target)],roads)




def better_waze(source,target,abstractMap,K):
    roads = load_map_from_csv()
    centralsLst = get_centrals_list(K)
    nearestCentral = utils.nearest_central(roads[int(source)], centralsLst, roads)
    path_a = UC.ucs(roads[int(source)], roads[int(nearestCentral)], roads)
    nearestCentralAir = int(utils.nearest_central_air(roads[int(target)], centralsLst, roads))
    path_b = UC.ucs(roads[int(nearestCentralAir)], roads[int(target)], roads)
    path_c = UC.ucs(abstractMap[nearestCentral], abstractMap[nearestCentralAir], abstractMap)
    if path_a and path_b and path_c:
        del path_a[-1]
        del path_c[0]
        del path_c[-1]
        del path_b[0]
        return path_a + path_c + path_b
    else:
        return UC.ucs(roads[int(source)], roads[int(target)], roads)




def better_waze_experiment(source,target,abstractMap,roads,K):
    centralsLst = get_centrals_list(K)
    print "getting nearest central"
    nearestCentral = utils.nearest_central(roads[int(source)], centralsLst, roads)
    print "calculating path_a.."
    cost_a , created_a = UC.ucs_expirement(roads[int(source)], roads[int(nearestCentral)], roads)
    print "getting nearest air"
    nearestCentralAir = int(utils.nearest_central_air(roads[int(target)], centralsLst, roads))
    print "calculating path_b"
    cost_b , created_b = UC.ucs_expirement(roads[int(nearestCentralAir)], roads[int(target)], roads)
    print "calculating path_c"
    cost_c , created_c = UC.ucs_expirement(abstractMap[nearestCentral], abstractMap[nearestCentralAir], abstractMap)


    if cost_c and cost_c and cost_c:
        cost = cost_a + cost_b + cost_c
        created = created_a + created_b + created_c
        return cost , created
    else:
        cost , created = UC.ucs_expirement(roads[int(source)], roads[int(target)], roads)
        return  cost , created + created_c


def data_set_experiment():
    K=[0.05]
    files = {0.0025 : 'abstractSpace0025.pkl', 0.005: 'abstractSpace.pkl' ,
             0.01 : 'abstractSpace01', 0.05:'abstractSpace05'}
    roads = load_map_from_csv()

    # for k in K:
    #     print "for k=" + str(k) + "making abstract map..."
    #     # abstractMaps[k] = build_abstract_map(get_centrals_list(k),roads)
    #     pickle.dump(build_abstract_map(get_centrals_list(k),roads), open(files[k], "wb"))
    #     print "Done!"


    exp = open('experiment05.csv', 'w')
    import csv
    with open('dataSet.csv', 'rb') as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            print "<------------ "+ row[0] +" to " + row[1] + "------------>"
            source = int(row[0])
            target = int(row[1])
            exp.write(str(source) + "," + str(target))
            ucCost , ucCreatedNodes = UC.ucs_expirement(roads[source],roads[target],roads)
            exp.write("," + str(ucCreatedNodes) + "," + str(ucCost))
            for k in K:
                print "loading pickle"
                import pickle as pkl
                abstractMap = pkl.load(open(files[k], 'rb'))
                absCost, absCreated = better_waze_experiment(source, target,abstractMap,roads,k)
                exp.write("," + str(absCreated) + "," + str(absCost))
            exp.write("\n")
    exp.close()
