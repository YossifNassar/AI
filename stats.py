'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
import utils


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    BResult=utils.branch_factors(roads)
    linksResult = utils.link_distance(roads)
    return {
        'Number of junctions' : utils.num_of_junctions(roads),
        'Number of links' : utils.num_of_links(roads),
        'Outgoing branching factor' : Stat(BResult[0],BResult[1],BResult[2]),
        'Link distance' : Stat(max=linksResult[0], min=linksResult[1], avg=linksResult[2]),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : utils.link_type_histogram(roads),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
