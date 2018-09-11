# -*- encoding: utf-8 -*-
""" Project #2 - Breadth-First Search, Connected Components and Graph Resilience """

from collections import deque


def bfs_visited (ugraph, start_node):
    """ Algorithm that checks the connection from 'source_node' to all other nodes """
    queue = deque([start_node])  # this is an empty queue to which we enqueue the initial element
    visited = set([start_node])  # we initialize a set of visited nodes for output

    while queue:
        node = queue.popleft()
        for neighbor in ugraph[node]:  # here we are scanning the neighbors of that particular node
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # after we marked this node as visited, we can now add it to the queue for scanning in future iterations

    return visited  # this returns the connected nodes ONLY


def cc_visited (adj_list):
    """ Algorithm that calculates a set of connected components of a graph. It is based on the connection-to-node data provided by the 'BFS_Distance' above """
    remaining_nodes = set(adj_list.keys())
    connected_components = []  # this is an empty list for storing connected components

    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = set(bfs_visited(adj_list, node))  # here we refer to the 'bfs' procedure written above
        connected_components.append(visited)
        remaining_nodes = remaining_nodes - visited  # since they are both sets, we can simply subtract them

    return connected_components  # this returns the connected components for the whole graph


def largest_cc_size(ugraph):
    """ Takes the undirected graph 'ugraph' and returns the size (an integer) of the largest connected component in ugraph """
    connected_components = cc_visited(ugraph)
    return max(map(len, connected_components)) if connected_components else 0


def compute_resilience(ugraph, attack_order):
    """ Takes the undirected graph 'ugraph', a list of nodes 'attack_order' and iterates through the nodes in attack_order. We remove the attacked nodes one by one and output the sequence of largest 'cc' as we go """
    resilience = [largest_cc_size(ugraph)]  # we start by making an output list with the first element already in

    for node in attack_order:
        neighbours = ugraph[node]
        ugraph.pop(node)  # remove the node so we don't have to scan through it. The graph then becomes smaller and smaller so the running time is: O(nlog(n) + m)
        for edge in neighbours:  # now we have to remove the edges associated to the node we just removed
            ugraph[edge].remove(node)
        resilience.append(largest_cc_size(ugraph))

    return resilience  # as a result we get the history of biggest possible groups there were left in a graph, with the rightmost element being the most recent
