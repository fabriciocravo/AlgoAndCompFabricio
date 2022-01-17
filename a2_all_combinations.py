import copy
import itertools
from math import floor

import a1_recap

toy_map = {'A': {'coords': (100, 100), 'next': {'B': 140, 'E': 200, 'F': 200}},
           'B': {'coords': (200, 140), 'next': {'A': 140, 'C': 260, 'F': 140}},
           'C': {'coords': (360,  40), 'next': {'B': 260, 'D': 360}},
           'D': {'coords': (320, 360), 'next': {'C': 360, 'F': 280}},
           'E': {'coords': (80, 280), 'next': {'A': 200, 'F': 120}},
           'F': {'coords': (160, 240), 'next': {'A': 200, 'B': 140, 'D': 280, 'E': 120}} }

"""
    Problem
    k hospitals
    Minimize the maximum distance of a city to a hospital
    k candidate cities
"""


# Just a small map reforming
def all_distances_dict(toy_map):

    all_distances = a1_recap.all_distances(toy_map)

    all_distances_dict = {}
    for key in all_distances:
        all_distances_dict[key[0]] = {}

    for key in all_distances:
        all_distances_dict[key[0]][key[1]] = all_distances[key]

    return all_distances_dict


# Get the closest hospital to a city
def closest_hospital(city, hospitals, distance_dict):

    min_dict = {}
    for h in hospitals:
        min_dict[h] = distance_dict[city][h]

    min_key = min(min_dict, key=min_dict.get)
    return min_dict[min_key], min_key


# get the Maxium distance to a hospital
def maximum_distance(hospitals, distance_dict):

    cities = distance_dict.keys()
    max_city = {}
    for city in cities:
        max_city[city] = closest_hospital(city, hospitals, distance_dict)

    max_key = max(max_city, key=max_city.get)
    return max_city[max_key][0], (max_key, max_city[max_key][1])


def all_combis(candidates, k):
  x = len(candidates)
  for i in range(1 << x):
      to_yield = [candidates[j] for j in range(x) if (i & (1 << j))]
      if len(to_yield) == k:
          yield to_yield


def brute_force(toy_map, k):

    distance_dict = all_distances_dict(toy_map)
    min_distance = 1000000000
    for comb in all_combis(list(distance_dict.keys()), k):
        current_dist = maximum_distance(comb, distance_dict)[0]
        if current_dist < min_distance:
            min_distance = current_dist
            best_comb = comb

    return best_comb, min_distance


def greedy(toy_map, k):
    """
    :param toy_map: the map to analise
    :param k: the number of hospitals allowed
    :return: greedy placement for hospital

        This function is a greedy algorithm that computes a potential placement for a hospital
        It tests every node to see which place would yield a minimal maximum distance to all remaining cities
        And it adds cities accordingly to this decision until it reaches the maximum k value
    """
    distance_dict = all_distances_dict(toy_map)

    winning_candidates = []
    for hospital in range(k):

        min_placement = 1000000000
        for city in list(distance_dict.keys()):
            candidates = copy.deepcopy(winning_candidates)
            candidates += [city]

            if maximum_distance(candidates, distance_dict)[0] < min_placement:
                next_city = city
                min_placement = maximum_distance(candidates, distance_dict)[0]

        winning_candidates.append(next_city)

    return winning_candidates, min_placement


def voisins(node_combi):
    selected, to_select = node_combi

    to_select_copy = to_select[:]
    for _ in to_select:
        next_city = to_select_copy.pop()
        yield (selected + [next_city], to_select_copy[:])


def combi_gen_k(candidates, k):
    r = ([], candidates)
    visited = []
    next = [r]
    while len(next) > 0:
        n = next.pop()
        visited.append(n)

        if len(n[0]) == k:
            yield (n[0])
            continue

        for v in voisins(n):
            next.append(v)


def heuristic_algorithm(toy_map, l, k):
    """
        :param toy_map: toy map
        :param l: size of combinations to test per turn
        :param k: number of hospitals
        :return: best placement according to this heuristic

            This heuristic works similarly to the greedy algo but instead of testing a node at a time
            It tests combinations of l nodes per time
            The final test uses the remaining nodes to add until it reaches k hospitals
    """
    number_of_loops = floor(k/l)
    final_loop_cities_number = int(k - floor(k/l)*l)
    distance_dict = all_distances_dict(toy_map)

    winning_comb = []
    for i in range(number_of_loops):
        min_placement = 1000000000
        for city_comb in combi_gen_k(list(toy_map.keys()), l):

            candidates = copy.deepcopy(winning_comb)
            candidates += city_comb

            if maximum_distance(candidates, distance_dict)[0] < min_placement:
                next_comb = city_comb
                min_placement = maximum_distance(candidates, distance_dict)[0]

        winning_comb += next_comb

    min_placement = 1000000000
    for city_comb in combi_gen_k(list(toy_map.keys()), final_loop_cities_number):

        candidates = copy.deepcopy(winning_comb)
        candidates += city_comb

        if maximum_distance(candidates, distance_dict)[0] < min_placement:
            next_comb = city_comb
            min_placement = maximum_distance(candidates, distance_dict)[0]

    winning_comb += next_comb

    return winning_comb


print(heuristic_algorithm(toy_map, 2, 3))


