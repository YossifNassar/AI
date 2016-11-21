from ways import load_map_from_csv
import utils
import random
import numpy
import collections
import datetime
import UC
from ways import graph


PATHS = 500000
P = 0.99

def flip_coin():
    return numpy.random.choice(numpy.arange(0, 2), p=[1 - P, P])


def random_node(roads):
    return random.choice(roads.junctions())


def build_path(node, roads, allNodes):
    path = [node]
    while (flip_coin() == 1) and (node.links != []):
        allNodes.append(node.index)
        link = random.choice(node.links)
        node = roads[link.target]
        path.append(node)

    return path


def print_path(path):
    lst = []
    for j in path:
        lst.append(j.index)
    print lst


def buildCentrality():
    roads = load_map_from_csv()
    paths = []
    allNodes = []

    print datetime.datetime.now()

    for i in range(PATHS):
        print str((float(i)/PATHS)*100) +"% percent done... Now in path number: " + str(i)
        node = random_node(roads)
        path = build_path(node, roads, allNodes)
        paths.append(path)

    f = open('centrality.csv', 'w');
    for t in collections.Counter(allNodes).most_common():
        f.write(str(t[0]) +"," + str(t[1]) + "\n")
    f.close()

    print datetime.datetime.now()


if __name__ == '__main__':
    # buildCentrality()
    roads = load_map_from_csv(start=0, count=10)
    path = UC.nearest(roads[0], 2,roads)
    # path = UC.ucs(roads[1],roads[3],roads)
    print_path (path)