import itertools

# Easy way out
for a in itertools.combinations(['A', 'B', 'C', 'D', 'E'], 3):
    # print(a)
    pass


# Iterations
def iterate_combinations(list, k):
    '''
    :param list: list of elements to print all possible combinations
    :param k: size of the combination
    :return: yields all possible combinations as a iterator

        This function iterates through all possible combinations of a list of elements
        The combinations have size k
    '''

    def return_combination(indexes):
        to_return = []
        for index, list in zip(indexes, combinations_list_of_lists):
            to_return.append(list[index])
        return to_return

    def next_combination(current_combination):

        streak = True
        to_update = [0]
        for i in range(0, k):
            if current_combination[i] == len(combinations_list_of_lists[i]) - 1 and streak:
                if i < k - 1:
                    to_update.append(i + 1)
                else:
                    current_combination[k - 1] = 0
                    del to_update[-1]
            else:
                streak = False

        for e in reversed(to_update):
            current_combination[e] += 1
            if current_combination[e] == len(combinations_list_of_lists[e]):
                current_combination[e] = current_combination[e + 1] + 1

    combinations_list_of_lists = []
    for i in range(k):
        combinations_list_of_lists.append(list[:len(list)-i])

    current_comb = [i for i in range(0, k)]
    current_comb.reverse()
    end_comb = [i for i in range(0, k)]
    end_comb.reverse()

    while True:
        to_yield = return_combination(current_comb)
        to_yield.reverse()
        yield to_yield
        next_combination(current_comb)

        if current_comb == end_comb:
            break


# TODO Explanation
"""
    we create a list of lists with potential combinations
    [ [A, B, C, D, E],
      [A, B, C, D],
      [A, B, C]
    ]
    
    We have a list of indexes to access the list of lists
    [ i1 i2 i3 ] 
    This list refers to an specific combination
    
    We loop through the combinations by adding to this list of indexes 
    [ 0 0 0 ] => becomes [ 1 0 0 ]
    
    And the second part only updates when the first one reaches the end
    [ end 0 0 ] => becomes [ 0 1 0 ]
"""


def all_combis(candidates):
  x = len(candidates)
  for i in range(1 << x):
      yield([candidates[j] for j in range(x) if (i & (1 << j))])


# TODO Explanation
"""
    for j in range(x) if (i & (1 << j))
        
        This loops through 1,2,4,8 - until j**candidates - it loops as powers of 2
        
        i loops through everything from 0 to 2**candidates - 1
        
        For each i we take only the binary parts as candidates for the combination
        For example:
            if i == 5 => 101 which means it will be 101 & 001 (1) and 101 & 100 (4)
            001 (1) corresponds to j == 0 first element and
            100 (4) corresponds to j == 2 second element (since 1 << 2 = 4)
            
        Therefore i = 5 will result in the list with [candidate[0], candidate[1]]
"""