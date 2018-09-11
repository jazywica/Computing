""" Provided code for application portion of module 1. Helper class for implementing efficient version of DPA algorithm """

import random

class DPATrial:
    """ Simple class to encapsulate optimized trials for DPA algorithm. Maintains a list of node numbers with multiple instances of each number. The number of instances of each node number are in the same proportion as the desired probabilities """
    def __init__(self, num_nodes):
        """ Initialize a DPATrial object corresponding to a complete graph with num_nodes nodes. Note the initial list of node numbers has num_nodes copies of each node number """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]  # this will imitate complete graph's starting point for the sum of 'total in-degree' + |V| (probability from pseudocode)

    def run_trial(self, num_nodes):
        """ Conduct num_node trials using by applying random.choice() to the list of node numbers. Updates the list of node numbers so that the number of instances of each node number is in the same ratio as the desired probabilities """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number appears in the correct ratio
        self._node_numbers.append(self._num_nodes)  # each time when we create new connections we add the number itself (as part of |V| requirement)
        self._node_numbers.extend(list(new_node_neighbors))  # and the in-degrees (as part of 'total in-degree')

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

