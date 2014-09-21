"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
from textwrap import wrap
from alg_upa import UPATrial
from bfs_visited import *

# CodeSkulptor import
#import SimpleGUICS2Pygame.simpleplot as simpleplot
import SimpleGUICS2Pygame.codeskulptor as codeskulptor
codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    new_graph = copy_graph(ugraph)
    degree_sets = [set([]) for dummy_k in new_graph]
    for node in new_graph:
        degree = len(new_graph[node])
        degree_sets[degree].add(node)
    L = []
    for k in range(len(new_graph)-1, -1, -1):
        while len(degree_sets[k]) > 0:
            arb_set = degree_sets[k].pop()
            for neighbor in new_graph[arb_set]:
                deg = len(new_graph[neighbor])
                degree_sets[deg].discard(neighbor)
                degree_sets[deg-1].add(neighbor)
            L.append(arb_set)
            delete_node(new_graph, arb_set)
    return L
    

def make_complete_graph(num_nodes):
    """
    Generate complete underected graph of size num_nodes
    
    Returns:
    A dictionary of type {node: list of edges}
    """
    cmplt_graph = {}
    for node in range(num_nodes):
        cmplt_graph[node] = set([])
        for edge in range(num_nodes):
            if node != edge:
                cmplt_graph[node].add(edge)
    return cmplt_graph


def er(n, p):
    """
    Generate unddirected graph of size n with probability p

    Returns:
    A dictionary of type {node: list of edges}
    """
    V = {i: set([]) for i in range(n)}
    for i in V:
        for j in V:
            if i != j:
                a = random.random()
                if a < p:
                    V[i].add(j)
                    V[j].add(i)
    return V


def random_order(ugraph):
    """
    Delete nodes from underected graph in random way

    Returns:
    A list of removed nodes
    """
    ugraph_copy = copy_graph(ugraph)
    nodes = []
    while len(ugraph_copy) > 0:
        node = random.choice(ugraph_copy.keys())
        nodes.append(node)
        delete_node(ugraph_copy, node)
    return nodes


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def count_edges(graph):
    """
    Count edges in undirected graph
    """
    count = 0
    for node in graph:
        count += len(graph[node])
    return count /2


def upa_graph(n=1347, m=5):
    """
    Generate UPA graph"
    """
    trial = UPATrial(m)
    upa = make_complete_graph(m)
    for nd in range(m, n):
        upa[nd] = trial.run_trial(m)
        for neigh in upa[nd]:
            upa[neigh].add(nd)
    return upa


def resilience(function, lst_of_graphs):
    res = []
    for graph in lst_of_graphs:
        attack_order = function(graph)
        comp_res = compute_resilience(graph, attack_order)
        res.append(comp_res[:-1])
    return res


def compute_runtime(function, ugraph):
    start = time.time()
    function(ugraph)
    t = time.time()-start
    return t


def random_order_res_plot():
    GRAPHS = [load_graph(NETWORK_URL), er(1347, 0.00172), upa_graph()]
    resilient = resilience(random_order, GRAPHS)
    x_vals = range(len(resilient[0]))
    y_comp_net = resilient[0]
    y_er = resilient[1]
    y_upa = resilient[2]
    print y_comp_net[269], y_er[269], y_upa[269]
    plt.plot(x_vals, y_comp_net, '-b', label='Computer network')
    plt.plot(x_vals, y_er, '-r', label='ER with p=0.00172')
    plt.plot(x_vals, y_upa, '-g', label='UPA with m=5')
    plt.title("Compute random order resilience of graphs")
    plt.xlabel('Nodes removed')
    plt.ylabel('Largest connect component')
    plt.legend(loc='upper right')
    plt.show()


def targeted_order_res_plot():
    GRAPHS = [load_graph(NETWORK_URL), er(1347, 0.00172), upa_graph()]
    resilient = resilience(fast_targeted_order, GRAPHS)
    x_vals = range(len(resilient[0]))
    y_comp_net = resilient[0]
    y_er = resilient[1]
    y_upa = resilient[2]
    print y_comp_net[269], y_er[269], y_upa[269]
    plt.plot(x_vals, y_comp_net, '-b', label='Computer network')
    plt.plot(x_vals, y_er, '-r', label='ER with p=0.00172')
    plt.plot(x_vals, y_upa, '-g', label='UPA with m=5')
    plt.title("Compute targeted order resilience of graphs")
    plt.xlabel('Nodes removed')
    plt.ylabel('Largest connect component')
    plt.legend(loc='upper right')
    plt.show()


def running_time_plot():
    upa_graphs = [upa_graph(n, 5) for n in range(10, 1000, 10)]
    x_vals = [len(graph) for graph in upa_graphs]
    y_to = sorted([compute_runtime(targeted_order, graph) for graph in upa_graphs])
    y_fto = sorted([compute_runtime(fast_targeted_order, graph) for graph in upa_graphs])

    plt.plot(x_vals, y_to, '-r', label='target_order')
    plt.plot(x_vals, y_fto, '-g', label='fast_target_order')
    plt.title("\n".join(wrap(
        "Compute runtime of functions targeted_order vs. fast_targeted_order with time.time() for UPA graph", 60)))
    plt.xlabel('Nodes')
    plt.ylabel('Runtime in seconds')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    #random_order_res_plot()
    running_time_plot()
    #targeted_order_res_plot()
