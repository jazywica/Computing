# -*- encoding: utf-8 -*-
""" Project #1 - Degree Distributions for Graphs """


EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 4, 5, 6, 7, 3])}


def make_complete_graph(num_nodes):
    """ Takes the number of nodes 'num_nodes' and returns a dictionary corresponding to a complete directed graph with the specified number of nodes """
    complete_graph = {}
    all_nodes = range(num_nodes)  # we first create all possible edges that we are going to apply to each node

    for node in range(num_nodes):
        complete_graph[node] = set(all_nodes) - set([node])  # this is the correction preventing edging to itself

    return complete_graph


def compute_in_degrees(digraph):
    """ Takes a directed graph 'digraph' (represented as a dictionary) and computes the in-degrees for the nodes in the graph """
    in_degrees = {}
    all_nodes = []

    for node in digraph.values():  # same as: all_nodes = [x for x in digraph.values() for x in list(x)]
        all_nodes.extend(list(node))

    for node in digraph:
        in_degrees[node] = all_nodes.count(node)

    return in_degrees  # returns a dictionary with the amount of nodes coming into each individual node


def in_degree_distribution(digraph):
    """ Takes a directed graph 'digraph' (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph """
    distribution = {}
    in_degrees = compute_in_degrees(digraph).values()

    for node in set(in_degrees):  # for the keys in our future dictionary we are going to use only unique numbers, hence the set() expression
        distribution[node] = in_degrees.count(node)  # for each in-degree amount we are going to return the amount of the in-degree edges

    return distribution  # returns a dictionary with the distribution of in-degrees for all recorded in-degree numbers (including 0 !!!)
