from heapq import *

toy_map = {'A': {'coords': (100, 100), 'next': {'B': 140, 'E': 200, 'F': 200}},
           'B': {'coords': (200, 140), 'next': {'A': 140, 'C': 260, 'F': 140}},
           'C': {'coords': (360,  40), 'next': {'B': 260, 'D': 360}},
           'D': {'coords': (320, 360), 'next': {'C': 360, 'F': 280}},
           'E': {'coords': ( 80, 280), 'next': {'A': 200, 'F': 120}},
           'F': {'coords': (160, 240), 'next': {'A': 200, 'B': 140, 'D': 280, 'E': 120}} }


def extract_min_dist(frontier, dist_heap):

    pop_min = heappop(dist_heap)[1]
    while pop_min not in frontier:
        pop_min = heappop(dist_heap)[1]
    frontier.remove(pop_min)

    return pop_min


def neighbors(graph, x):
    return list(graph[x]['next'].keys())


def distance(graph, x, y):
    return graph[x]['next'][y]


def PCCs(graph, s):

    frontier = set(s)
    dist = {s: 0}
    dist_heap = [tuple((dist[key], key)) for key in dist]
    heapify(dist_heap)

    while len(frontier) > 0:

        ### extraction of the node of the boundary having the minimum distance ###
        x = extract_min_dist(frontier, dist_heap)

        ### for each updated neighbor of the border and its distance ###
        for i, y in enumerate(neighbors(graph, x)):

            if y not in dist:
                frontier.add(y)

            new_dist = dist[x] + distance(graph, x, y)
            if y not in dist or dist[y] > new_dist:
                dist[y] = new_dist
                heappush(dist_heap, (new_dist, y))

    return dist


def all_distances(toy_map):

    all_pccs = {}
    for n1 in toy_map:
        pcc_dict = PCCs(toy_map, n1)
        for n2 in pcc_dict:
            all_pccs[(n1, n2)] = pcc_dict[n2]

    return all_pccs

