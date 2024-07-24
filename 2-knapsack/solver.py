#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import attrgetter

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        v, w = int(parts[0]), int(parts[1])
        items.append(Item(i-1, v, w, float(v / w)))

    # # 1) calling trivial solution
    # value, opt_flag, taken = trivial(capacity, items)

    # # 2) calling quantity greedy algorithm
    # value, opt_flag, taken = greedy_quantity(capacity, items)

    # # 3) calling value greedy algorithm
    # value, opt_flag, taken = greedy_value(capacity, items)

    # # 4) calling value-density greedy algorithm
    # value, opt_flag, taken = greedy_value_density(capacity, items)

    # 5) calling bottom-up dynamic programming solution
    value, opt_flag, taken = dynamic_programming(capacity, items)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(opt_flag) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def trivial(capacity, items):
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    opt_flag = 0
        
    return value, opt_flag, taken

def greedy_quantity(capacity, items):
    # idea: more iems is best, start with small ones
    # take as many as you can
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in sorted(items, key=attrgetter('weight')):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    opt_flag = 0

    return value, opt_flag, taken

def greedy_value(capacity, items):
    # idea: valuable items are best, start with
    # the most valuable items
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in sorted(items, key=attrgetter('value'), reverse=True):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    opt_flag = 0

    return value, opt_flag, taken

def greedy_value_density(capacity, items):
    # idea: valuable items are best, start with
    # the most valuable items per unit mass
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in sorted(items, key=attrgetter('density'), reverse=True):
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    opt_flag = 0

    return value, opt_flag, taken

def dynamic_programming(capacity, items):
    n = len(items)
    taken = [0] * n
    sol_table = [[0 for j in range(n+1)] for i in range(capacity+1)]
    # i indexing weight/capacities (rows)
    # j indexing items (columns)
    for j in range(n+1):
        if j > 0:
            item_val = items[j-1].value
            item_weight = items[j-1].weight
        for i in range(capacity+1):
            if i == 0 or j == 0:
                continue
            # as we go down the col, if the weight of the item is greater than capacity,
            # the solution table takes the value 'to the left'
            elif item_weight > i:
                sol_table[i][j] = sol_table[i][j-1]
            else:
                val_take_current = item_val + sol_table[i-item_weight][j-1]
                val_keep_last    = sol_table[i][j-1]
                sol_table[i][j] = max(val_take_current, val_keep_last)

    # trace back
    value = sol_table[capacity][n]
    cap = capacity
    for k in reversed(range(0,n)):
        if sol_table[cap][k+1] == sol_table[cap][k]:
            taken[k] = 0
        else:
            taken[k] = 1
            cap -= items[k].weight

    opt_flag = 1

    return value, opt_flag, taken

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

