import networkx as nx
import matplotlib.pyplot as plt


# The Graph
G = nx.Graph()


# Neighbour of a Node
def neighbors_of_node(node):
    n = []
    edges_list = list(G.edges)
    i = 0
    while i < len(edges_list):
        if node == edges_list[i][0]:
            n.append(edges_list[i][1])
        elif node == edges_list[i][1]:
            n.append(edges_list[i][0])
        i += 1
    return n


# Depth-First search algorithm
def count_of_components():
    nodes_list = list(G.nodes)

    count_of_comps = 0
    steps_count = 0

    while nodes_list:
        visited = [nodes_list[0]]
        stack = neighbors_of_node(visited[0])
        while stack:
            node = stack.pop()
            tmp_neighbors_list = neighbors_of_node(node)
            visited.append(node)

            i = 0
            while i < len(tmp_neighbors_list):
                if tmp_neighbors_list[i] not in visited and tmp_neighbors_list[i] not in stack:
                    stack.append(tmp_neighbors_list[i])
                i += 1

        visited.sort()
        nodes_list.sort()
        if visited == nodes_list and steps_count == 0:
            count_of_comps = 1
            return count_of_comps
        else:
            steps_count += 1
            count_of_comps += 1
            j = 0
            while j < len(visited):
                nodes_list.remove(visited[j])
                j += 1
            if nodes_list != []:
                visited = [nodes_list[0]]
    return count_of_comps


def count_of_bridges():
    edges_list = list(G.edges)
    count_of_bridges = 0

    first_count_of_comps = count_of_components()
    i = 0
    while i < len(edges_list):
        tmp = edges_list[i]
        G.remove_edge(tmp[0], tmp[1])
        tmp_count_of_comps = count_of_components()
        if tmp_count_of_comps > first_count_of_comps:
            count_of_bridges += 1
        G.add_edge(tmp[0], tmp[1])
        i += 1
    return count_of_bridges


def count_of_cut_vertices():
    nodes_list = list(G.nodes)
    count_of_cut_vertices = 0
    first_count_of_comps = count_of_components()

    i = 0
    while i < len(nodes_list):
        tmp = nodes_list[i]
        neighbors_list = neighbors_of_node(tmp)
        G.remove_node(tmp)
        tmp_count_of_comps = count_of_components()

        if tmp_count_of_comps > first_count_of_comps:
            count_of_cut_vertices += 1
        j = 0
        G.add_node(tmp)
        while j < len(neighbors_list):
            G.add_edge(tmp, neighbors_list[j])
            j += 1
        i += 1
    return count_of_cut_vertices


def generate_subsets(input_set):
    input_list = list(input_set)
    subsets = []

    def backtrack(start, path):
        subsets.append(set(path))
        for i in range(start, len(input_list)):
            path.append(input_list[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    subsets.sort(key=len)
    subsets.pop(0)
    return subsets


def node_connectivity_custom():
    g_components = count_of_components()
    nodes = list(G.nodes)
    all_nodes_subsets = generate_subsets(nodes)
    min_cut_size = len(nodes)
    found_cut = False

    for subset in all_nodes_subsets:
        removed_edges = []

        for node in subset:
            removed_edges.extend(G.edges(node))
            G.remove_node(node)
        new_components = count_of_components()

        for node in subset:
            G.add_node(node)
        for edge in removed_edges:
            G.add_edge(edge[0], edge[1])

        if new_components > g_components:
            min_cut_size = min(min_cut_size, len(subset))
            found_cut = True
    return min_cut_size if found_cut else 0


def edge_connectivity_custom():
    g_components = count_of_components()
    edges = list(G.edges)
    all_edges_subsets = generate_subsets(edges)
    min_cut_size = len(edges)
    found_cut = False

    for subset in all_edges_subsets:
        for edge in subset:
            G.remove_edge(*edge)
        new_components = count_of_components()
        for edge in subset:
            G.add_edge(*edge)

        if new_components > g_components:
            min_cut_size = min(min_cut_size, len(subset))
            found_cut = True
    return min_cut_size if found_cut else 0



edge_list = [
    (2, 4), (2, 5),
    (3, 5), (3, 8), (3, 9),
    (4, 8), (4, 6),
    (5, 6), (5, 7),
    (6, 7), (6, 8),
    #
    (10, 11), (10, 12), (11, 12), (11, 14),
    #
    (23, 24), (23, 25)
]

G.add_edges_from(edge_list)

print("Count of Components - ", count_of_components())
print("Count of Bridges - ", count_of_bridges())
print("Count of Cut Vertices - ", count_of_cut_vertices())
print("Node Connectivity - ", node_connectivity_custom())
print("Edge Connectivity - ", edge_connectivity_custom())
nx.draw_spring(G, with_labels=True)
plt.show()
