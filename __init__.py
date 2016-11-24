
if __name__ == '__main__':
    # buildCentrality()
    roads = load_map_from_csv()
    # path =UC.nearest(roads[0], 10,roads)
    # path = UC.ucs(roads[1],roads[3],roads)
    # print (path)
    # build_abstract_space(roads)

    # build_data_set(roads)
    # print UC.nearest_with_cost(roads[0], 2, roads)
    # print UC.ucs(roads[17998],roads[97121],roads)
    # test_dataset(roads)
    K=0.005
    lst = load_centrality()
    centralsCount = K * len(lst)
    centrals = lst[:int(centralsCount)]
    centralsLst = map(lambda x: x[0], centrals)

    # build_abstract_space(centralsLst,K,roads)

    # print UC.nearest_with_cost(roads[0], 2, roads)

    # print nearest_central(roads[0], centralsLst, roads)
    # print nearest_central_air(roads[0], centralsLst, roads)
