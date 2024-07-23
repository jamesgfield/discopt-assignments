#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import attrgetter

Item = namedtuple("Item", ['index', 'value', 'weight'])

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
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # # 1) calling trivial solution
    # value, opt_flag, taken = trivial(capacity, items)

    # 2) calling quantity-greedy algorithm
    value, opt_flag, taken = greedy_quantity(capacity, items)
    
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

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

