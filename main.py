'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions

import UC
from ways import load_map_from_csv
import utils

def base(source, target):
    'call function to find path using uniform cost, and return list of indices'
    roads = load_map_from_csv()
    return UC.ucs(roads[int(source)],roads[int(target)],roads)

    
def betterWaze(source, target,abstractMap=None):
    'call function to find path using better ways algorithm, and return list of indices'
    roads = load_map_from_csv()
    K=0.005
    lst = utils.load_centrality()
    centralsCount = K * len(lst)
    centrals = lst[:int(centralsCount)]
    centralsLst = map(lambda x: x[0], centrals)
    nearestCentral = utils.nearest_central(roads[int(source)], centralsLst, roads)
    path_a = UC.ucs(roads[int(source)],roads[int(nearestCentral)],roads)
    nearestCentralAir = int(utils.nearest_central_air(roads[int(target)], centralsLst, roads))
    path_b = UC.ucs(roads[int(nearestCentralAir)],roads[int(target)], roads)
    path_c = UC.ucs(abstractMap[nearestCentral],abstractMap[nearestCentralAir], abstractMap)

    if path_a and path_b and path_b:
        del path_a[-1]
        del path_c[0]
        del path_c[-1]
        del path_b[0]
        return path_a+path_c+path_b
    else:
        return UC.ucs(roads[int(source)],roads[int(target)],roads)



def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'base':
        path = base(source, target)
    elif argv[1] == 'bw':
        abstractMap = None
        if len(argv)>4:
             import pickle as pkl
             abstractMap = pkl.load(open(argv[4],'rb'))
        path = betterWaze(source, target,abstractMap)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
