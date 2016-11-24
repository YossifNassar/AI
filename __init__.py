from ways import load_map_from_csv
import utils
import random
import numpy
import collections
import datetime
import UC
import pickle

PATHS = 500000
P = 0.99
K = 0.005
M = 0.1
DATA_SET_LENGTH = 20
DATA_SET_ADGACENTS = 30000
DATA_SET_OPERATIONS = 200


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


def build_abstract_space(roads):
    lst = load_centrality()
    centralsCount = K * len(lst)
    centrals = lst[:int(centralsCount)]
    dict = {}
    # UC.nearest(roads[int(0)], 3, roads)
    for central in centrals:
        dict[central[0]] = UC.nearest(roads[int(central[0])], M * centralsCount, roads)
    pickle.dump(dict, open("abstractSpace.pkl", "wb"))


def build_data_set(roads):
    pairs = {}
    f = open('dataSet2.csv', 'w')
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


if __name__ == '__main__':
    # buildCentrality()
    roads = load_map_from_csv()
    # path =UC.nearest(roads[0], 10,roads)
    # path = UC.ucs(roads[1],roads[3],roads)
    # print (path)
    # build_abstract_space(roads)

    print datetime.datetime.now()
    build_data_set(roads)
    print datetime.datetime.now()

    # print UC.ucs(roads[17998],roads[97121],roads)
    # test_dataset(roads)
