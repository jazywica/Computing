# -*- encoding: utf-8 -*-
""" Project #3 - Clustering and Closest Pair of Points - version with indexes as function arguments """

import alg_cluster


# 1. Closest pair of clusters
def pair_distance(cluster_list, idx1, idx2):
    """ Function that computes Euclidean distance between two clusters in a list where idx1 and idx2 are integer indices for two clusters. Output: tuple (dist, idx1, idx2) where dist is distance between clusters """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list, idx1=0, idx2=0):
    """ Compute the distance between the closest pair of clusters in a list (SLOW). Output: tuple (dist, idx1, idx2) where the centers of the clusters have minimum distance dist """
    if idx2 == 0:
        idx2 = len(cluster_list)  # since we can't use 'idx2=len(cluster_list)' as a function argument we have to use such a structure
    min_dist = (float('inf'), -1, -1)  # this is the initialized output format

    for idx_u in range(idx1, idx2 - 1):
        for idx_v in range(idx_u + 1, idx2):
            distance = pair_distance(cluster_list, idx_u, idx_v)
            if distance[0] < min_dist[0]:
                min_dist = distance

    return min_dist


def fast_closest_pair(cluster_list, idx1=0, idx2=0):  # the 'cluster list' has to be sorted (by the horizonatal coordinates in this case)
    """ Compute the distance between the closest pair of clusters in a list (FAST). Input: sorted list by vertical coordinates. Output: tuple (dist, idx1, idx2) where the centers of the clusters have minimum distance dist """
    if idx2 == 0:
        idx2 = len(cluster_list)
    length = idx2 - idx1

    if length <= 3:
        return slow_closest_pair(cluster_list, idx1, idx2)  # BASE CASE outputs a tuple: (dist, idx1, idx2)
    else:
        mid = idx1 + length // 2  # here we calculate the mid point slightly different
        cluster_left = fast_closest_pair(cluster_list, idx1, mid)  # this will go as far down-left as possible
        cluster_right = fast_closest_pair(cluster_list, mid, idx2)  # this will pick up from the smallest, next to the right
        min_dist = cluster_left if cluster_left[0] <= cluster_right[0] else cluster_right  # here we pick up the smallest value form both sides in order to compare it to the strip

        horizontal_center = (cluster_list[mid - 1].horiz_center() + cluster_list[mid].horiz_center()) / 2  # here we calculate the middle (on x-axis) for the two border points
        strip = closest_pair_strip(cluster_list, horizontal_center, min_dist[0], idx1, idx2)
        min_dist = strip if strip[0] < min_dist[0] else min_dist

    if min_dist[1] > min_dist[2]:  # extra condition that indices in output must be in ascending order
        min_dist = (min_dist[0], min_dist[2], min_dist[1])

    return min_dist


def closest_pair_strip(cluster_list, horiz_center, half_width, idx1=0, idx2=0):  # (clusters produced by fast_closest_pair, horizontal position of the strip's vertical center line, half the width of the strip (i.e; the maximum horizontal distance that a cluster can lie from the center line))
    """ Helper function to compute the closest pair of clusters in a vertical strip. Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters that lie in the strip and have minimum distance dist """
    if idx2 == 0:
        idx2 = len(cluster_list)

    min_dist = (float('inf'), -1, -1)  # this is the initialized output format
    strip = []  # this is the initial list for our strip, in this version we are not going to use dictioanry, we will store the indexes as a tuple inside the strip
    for idx in range(idx1, idx2):
        if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width:
            strip.append((cluster_list[idx], idx))  # here we append both the object and its initial index into the strip to keep track of the original indexing

    strip_length = len(strip)
    strip.sort(key = lambda cluster: cluster[0].vert_center())  # the whole idea here is to sort the strip AFTER it has been stripped, as sorting is O(n)
    strip_no_idx = [obj for obj, dummy_idx in strip]  # this is just to pass the objets only into the 'pair_distance' function

    for idx_u in range(strip_length):  # now we are looking for points with smallest distance. theoretically we could stop idx_u on 3rd element from the end, but it doesn't work for small lists, it stops too early
        for idx_v in range(idx_u + 1, min(idx_u + 4, strip_length)):  # this range is for the next 3 elements or to the end of the list
            min_dist = min(min_dist, pair_distance(strip_no_idx, idx_u, idx_v))  # this by default will return a tuple with the smallest first element

    if min_dist[0] != float('inf'):  # we have to condition the output, as searching for keys in 'indexing' dictionary will return a key error
        min_dist = (min_dist[0], strip[min_dist[1]][1], strip[min_dist[2]][1])

        if min_dist[1] > min_dist[2]:  # extra condition that indices in output must be in ascending order
            min_dist = (min_dist[0], min_dist[2], min_dist[1])

    return min_dist


def closest_pair_strip_dictionary(cluster_list, horiz_center, half_width, idx1=0, idx2=0):  # (clusters produced by fast_closest_pair, horizontal position of the strip's vertical center line, half the width of the strip (i.e; the maximum horizontal distance that a cluster can lie from the center line))
    """ Version of 'closest_pair_strip' with a dictionary as a data structure, made only for performance comparison with the indexed version above """
    if idx2 == 0:
        idx2 = len(cluster_list)

    indexing = {}  # we first initialize a dictionary in which we are going to store the indexes, we use dictionary here, as searching for keys is theoretically O(1)
    for idx in range(idx1, idx2):
        indexing[str(cluster_list[idx].horiz_center()) + str(cluster_list[idx].vert_center())] = idx  # as keys we are going to use glued verical and horizontal coords, as this is the most unique combination

    strip = [obj for obj in cluster_list[idx1:idx2] if abs(obj.horiz_center() - horiz_center) < half_width]
    strip.sort(key = lambda cluster: cluster.vert_center())  # the whole idea here is to sort the strip AFTER it has been stripped, as sorting is O(n)
    strip_length = len(strip)
    min_dist = (float('inf'), -1, -1)  # this is the initialized output format

    for idx_u in range(strip_length):  # theoretically we could idx2 on 3rd element from the end, but it doesn't work for small lists, it stops too early
        for idx_v in range(idx_u + 1, min(idx_u + 4, strip_length)):  # this range is for the next 3 elements or to the end of the list
            min_dist = min(min_dist, pair_distance(strip, idx_u, idx_v))

    if min_dist[0] != float('inf'):  # we have to condition the output, as searching for keys in 'indexing' dictionary will return a key error
        min_dist = (min_dist[0], indexing[str(strip[min_dist[1]].horiz_center()) + str(strip[min_dist[1]].vert_center())], indexing[str(strip[min_dist[2]].horiz_center()) + str(strip[min_dist[2]].vert_center())])
        if min_dist[1] > min_dist[2]:  # there is also a condition that indexes in output must be in ascending order
            min_dist = (min_dist[0], min_dist[2], min_dist[1])

    return min_dist


# 2. Hierarchical clustering
def hierarchical_clustering(cluster_list, num_clusters):
    """ Compute a hierarchical clustering of a set of clusters, Note: the function may mutate cluster_list. Input: List of clusters, integer number of clusters. Output: List of clusters whose length is num_clusters """
    cluster_list = [cluster.copy() for cluster in cluster_list]  # first we create a list of cluster object copies, as we need to work on a copy and the 'fips_codes' don't come as sets fot the cancer data

    while len(cluster_list) > num_clusters:  # this function is searching for two closest points in a set and merges them until there are as many elements in the list left, as there were supposed to be clusters
        # Clusters passed to 'fast_closest_pair' need to be in horizontally sorted order. As a result, we will need to resort the list of clusters after each call to 'merge_clusters' as it may change clusters' coordinates
        cluster_list.sort(key=lambda c: c.horiz_center())  # we have to sort the list by its x-values before we can use the fast algorithm
        closest_pair = fast_closest_pair(cluster_list)  # this function will return the distance, and two indices
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])  # we use the provided function to merge two clusters, we have to resort the list now before we go for fast function again
        cluster_list.pop(closest_pair[2])  # we merged the points into 'closest_pair[1]' point, so we have to remove the other one

    return cluster_list


# 3. K-means Clustering
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """ Compute the k-means clustering of a set of clusters. Note: the function may not mutate cluster_list. Input: List of clusters, integers number of clusters and number of iterations Output: List of clusters whose length is num_clusters """
    cluster_list = [cluster.copy() for cluster in cluster_list]  # first we create a list of cluster object copies, as we need to work on a copy and the 'fips_codes' don't come as sets fot the cancer data
    initial_centers = sorted(cluster_list, reverse=True, key=lambda cls: cls.total_population())[:num_clusters]  # position initial clusters of size num_clusters at the location of clusters with largest populations

    for dummy_iteration in range(num_iterations):  # the main loop that counts for the number of iterations
        clusters = [(alg_cluster.Cluster(set([]), 0, 0, 0, 0), cluster) for cluster in initial_centers]  # we need an empty cluster to merge with the incoming clusters, we also add the initial coords to simplify future ops.
        for cluster in cluster_list:
            new_cluster, dummy_center = min(clusters, key=lambda cls: cls[1].distance(cluster))  # as we iterate, we store 'cluster' object as 'new_cluster' where the initial coords are the closest
            new_cluster.merge_clusters(cluster)  # by using the reference to the cluster object, we merge the object in 'clusters' with the one we picked
        initial_centers = [cluster for cluster, dummy_center in clusters]  # now we have to update, the initial centers for the next iteration, as this is where the initial positions into 'clusters' came from

    return initial_centers
