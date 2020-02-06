import networkx as nx
import matplotlib.pyplot as plt


decoded_list = []


def network_graph_func(ip_src_dest_count):
    """Function handles creation of network graph"""
    g = nx.DiGraph()
    plt.figure(1, figsize=(10, 10))

    for key,val in ip_src_dest_count.items():
        # Takes dictionary values as Key and items as val.
        key1 = (str(key).split(':', 1))
        g.add_node(str(key1[0]))
        g.add_node(str(key1[1]))
        g.add_edge(str(key1[0]), str(key1[1]), weight=(val / 90))
        # Takes 2 keys, which are the IP's with a weight of val / 90

    pos = nx.spring_layout(g,k=2,iterations=30,weight=10)
    # Configures the layout for the graph, with weight.
    nx.draw_networkx_nodes(g,pos,node_size=300)
    # Draws the graph nodes.
    nx.draw_networkx_labels(g,pos,font_size=10)
    # Draws the graph labels
    edge_size = [d['weight'] for (u,v,d) in g.edges(data=True)]
    # Sets the size of the edges.
    nx.draw_networkx_edges(g,pos,width=edge_size)
    # Draws the lines between nodes.


