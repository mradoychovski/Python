"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2

    Returns tuple (dist, idx1, idx2) with idx1 < idx2
    where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm

    Returns the set of all tuples of the form (dist, idx1, idx2)
    where the cluster_list[idx1] and cluster_list[idx2]
    have minimum distance dist.

    """
    num = len(cluster_list)
    (min_dist, ith, jth) = ('inf', -1, -1)
    cluster_set = set([(min_dist, ith, jth)])
    for idx in range(num-1):
        for jdx in range(idx+1, num):
            (dist, index, jndex) = \
                pair_distance(cluster_list, idx, jdx)
            if dist < min_dist:
                cluster_set = set([(dist, index, jndex)])
                (min_dist, ith, jth) = (dist, index, jndex)
            if dist == min_dist:
                cluster_set.add((dist, index, jndex))
                (min_dist, ith, jth) = (dist, index, jndex)
    return cluster_set


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm

    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """

    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance
        between closest pair of points
        Running time is O(n * log(n))

        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically

        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters

        """
        num = len(horiz_order)
        # base case
        if num <= 3:
            (dist, ith, jth) = ('inf', -1, -1)
            for idx in range(num-1):
                for jdx in range(idx+1, num):
                    (dist, ith, jth) = \
                        min((dist, ith, jth),
                        pair_distance(
                        cluster_list, horiz_order[idx], horiz_order[jdx]))
            return (dist, ith, jth)
#            return min(slow_closest_pairs(cluster_list))

        # divide
        mid = (cluster_list[horiz_order[num/2-1]].horiz_center() +
            cluster_list[horiz_order[num/2]].horiz_center())/2

        #horiz_l, horiz_r = horiz_order[:num/2], horiz_order[num/2:num]

        vert_l = [vert_order[idx] for idx in range(num)
            if vert_order[idx] in set(horiz_order[:num/2])]
        vert_r = [vert_order[idx] for idx in range(num)
            if vert_order[idx] in set(horiz_order[num/2:num])]

        (dist_l, ith_l, jth_l) = \
            fast_helper(cluster_list, horiz_order[:num/2], vert_l)
        (dist_r, ith_r, jth_r) = \
            fast_helper(cluster_list, horiz_order[num/2:num], vert_r)

        # conquer
        (dist, ith, jth) = min((dist_l, ith_l, jth_l), (dist_r, ith_r, jth_r))
        closest = [ver for ver in vert_order if abs(
            cluster_list[ver].horiz_center() - mid) < dist]
        for idx in range(len(closest)-1):
            for jdx in range(idx+1, min(idx+3, len(closest))):
                (dist, ith, jth) = min((dist, ith, jth),
                    pair_distance(cluster_list, closest[idx], closest[jdx]))
        return (dist, ith, jth)

    # compute list of indices for the clusters ordered
    # in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx)
                        for idx in range(len(cluster_list))]
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1]
        for idx in range(len(hcoord_and_index))]
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx)
                        for idx in range(len(cluster_list))]
    vcoord_and_index.sort()
    vert_order = \
        [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order)
    return (answer[0], min(answer[1:]), max(answer[1:]))


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list

    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        (clstr_i, clstr_j) = fast_closest_pair(cluster_list)[1:]
        cluster_list.append(
            cluster_list[clstr_i].merge_clusters(cluster_list[clstr_j]))
        cluster_list.remove(cluster_list[clstr_j])
        cluster_list.remove(cluster_list[clstr_i])
    #distortion = sum([clstr.cluster_error(data_table) for clstr in cluster_list])
    return cluster_list     #, distortion


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list

    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    #initialize k-means clusters to be initial clusters with largest populations
    num = len(cluster_list)
    lrgst_pop = sorted([clstr.total_population()
        for clstr in cluster_list], reverse=True)[:num_clusters]
    init_points = [(clstr.horiz_center(), clstr.vert_center())
        for clstr in cluster_list if clstr.total_population() >= min(lrgst_pop)]
    for dummy_i in range(num_iterations):
        empty_clstrs = [alg_cluster.Cluster(set([]), point[0], point[1], 0, 0)
            for point in init_points]
        for jth in range(num):
            pnt_jth = (cluster_list[jth].horiz_center(),
                cluster_list[jth].vert_center())
            index = \
                min([(math.sqrt((pnt_jth[0]-init_points[kth][0])**2 +
                (pnt_jth[1]-init_points[kth][1])**2), kth)
                for kth in range(num_clusters)])[1]
            empty_clstrs[index].merge_clusters(cluster_list[jth])

        for item in range(num_clusters):
            init_points[item] = (empty_clstrs[item].horiz_center(),
                empty_clstrs[item].vert_center())
    
    return empty_clstrs


