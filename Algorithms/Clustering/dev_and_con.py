from random import randrange
from alg_cluster import Cluster
from alg_project3_solution import *
import matplotlib.pyplot as plt
from time import time


def CountInversions(A):
    len_A = len(A)
    if len_A == 1:
        return 0
    B = A[:len_A/2]
    C = A[len_A/2:len_A]
    il = CountInversions(B)
    ir = CountInversions(C)
    im = Merge(B, C, A)
    return il + ir + im


def Merge(B, C, A):
    count = 0
    i, j, k = 0, 0, 0
    p = len(B)
    q = len(C)
    while i < p and j < q:
        if B[i] <= C[j]:
            A[k] = B[i]
            i += 1
        else:
            A[k] = C[j]
            j += 1
            count += p - i
        k += 1
    if i == p:
        A[k:p+q] = C[j:q]
    else:
        A[k:p+q] = B[i:p]
    return count


def mystery(A, l, r):
    if l > r:
        return -1
    m = (l + r)/2
    if A[m] == m:
        return m
    else:
        if A[m] < m:
            return mystery(A, m+1, r)
        else:
            return mystery(A, l, m-1)


#def hierarchicalClustering(P, k):
#    n = len(P)
#    C = [P[i] for i in range(n)]
#    while len(C) > k:


def gen_random_clusters(num_clusters):
    cluster_list = \
        [Cluster(set([]), randrange(-1.0, 1.0, int=float),
        randrange(-1.0, 1.0, int=float), 0, 0)
            for dummy_i in range(num_clusters)]
    return cluster_list


def run(fun, cluster_list):
    start = time()
    fun(cluster_list)
    stop = time()-start
    return stop


cluster_list = [gen_random_clusters(num) for num in range(2, 201)]

slow = [run(slow_closest_pairs, clstr_l) for clstr_l in cluster_list]
fast = [run(fast_closest_pair, clstr_l) for clstr_l in cluster_list]
#print slow[25]

x_vals = [item+2 for item in range(len(cluster_list))]
plt.plot(x_vals, slow, '-b', label='slow')
plt.plot(x_vals, fast, '-r', label='fast')
plt.title("slow_closest_pairs() vs. fast_closest_pair() - Runtime")
plt.xlabel('Number of clusters')
plt.ylabel('Runtime in sec')
plt.legend(loc='upper left')
plt.show() 


#print mystery([-2,0,1,3,7,12,15],0,6)
#A = [5,4,3,6,7]
#print CountInversions(A)
