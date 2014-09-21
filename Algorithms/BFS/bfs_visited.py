"""
    Project 2 - Connected components and graph resilience
"""

from poc_queue import Queue

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node and returns
    the set consisting of all nodes that are visited by a breadth-first search
    that starts at start_node.
    """
    queue_obj = Queue()
    visited = set([start_node])
    queue_obj.enqueue(start_node)
    while len(queue_obj) != 0:
        dequeue_list = queue_obj.dequeue()
        for item in ugraph[dequeue_list]:
            if not item in visited:
                visited.add(item)
                queue_obj.enqueue(item)
    return visited


def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, where each set
    consists of all the nodes (and nothing else) in a connected component,
    and there is exactly one set in the list for each connected component in
    ugraph and nothing else.
    """
    remaining_nodes = [node for node in ugraph]
    cc_list = []
    while len(remaining_nodes) != 0:
        arb_node = remaining_nodes[0]
        bfs_result = bfs_visited(ugraph, arb_node)
        cc_list.append(bfs_result)
        rem_nds = [node for node in remaining_nodes if not node in bfs_result]
        remaining_nodes = rem_nds
    return cc_list


def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) of
    the largest connected component in ugraph.
    """
    connections = cc_visited(ugraph)
    if len(connections) == 0:
        return 0
    conn_lengths = [len(connect) for connect in connections]
    return max(conn_lengths)


def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates
    through the nodes in attack_order. For each node in the list, the function
    removes the given node and its edges from the graph and then computes
    the size of the largest connected component for the resulting graph.
    """
    largest_conn = [largest_cc_size(ugraph)]
    for node in attack_order:
        neighbors = ugraph[node]
        ugraph.pop(node)
        for neighbor in neighbors:
            ugraph[neighbor].remove(node)
        largest_conn.append(largest_cc_size(ugraph))
    return largest_conn
