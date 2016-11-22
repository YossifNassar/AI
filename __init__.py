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
K=0.005
M=0.1

def load_centrality(filename='centrality.csv'):
    import csv
    lst = []
    with open(filename,'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append((row[0],row[1]))
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
    start_time= datetime.datetime.now()

    for i in range(PATHS):
        print str((float(i)/PATHS)*100) +"% percent done... Now in path number: " + str(i)
        node = random_node(roads)
        build_path(node, roads, allNodes)

    f = open('centrality.csv', 'w');
    for t in collections.Counter(allNodes).most_common():
        f.write(str(t[0]) +"," + str(t[1]) + "\n")
    f.close()


if __name__ == '__main__':
    # buildCentrality()
    roads = load_map_from_csv()
    # path =UC.nearest(roads[0], 10,roads)
    # path = UC.ucs(roads[1],roads[3],roads)
    # print (path)
    lst = load_centrality()
    centralsCount = K*len(lst)
    centrals=lst[:int(centralsCount)]
    dict={}
    # UC.nearest(roads[int(0)], 3, roads)

    for central in centrals:
        dict[central[0]] = UC.nearest(roads[int(central[0])], M*centralsCount,roads)

    pickle.dump( dict, open( "abstractSpace.pkl", "wb" ) )
