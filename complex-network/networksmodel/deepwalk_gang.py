import sys
# Set root path
sys.path.append(r"d:\中环\科研与教研与企业特派员项目\科研\2021市教委自然科学基金项目材料\项目结项\结项代码\任务三\deepwalk_Sweden_gang_echarts")
from datetime import datetime
import json
import networkx as nx
from utils.util import *
from utils.com_dec import *
import matplotlib.pyplot as plt
from networksmodel.deepwalk import *


if __name__ == "__main__":
    # Reads an edge list from a file and returns it as a list of tuples.
    edge_list = read_edgelist("data/Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from
    # a file and return three lists containing node IDs, gang labels, and hierarchy attributes
    nodeId_array, gang_labels, hie_attribute = read_attributes(
        "data/Sweden_gang_attributes.txt")

    # Create an undirected graph with node attributes concerning gang datasets
    G = nx.Graph()

    # Add node numbers into G
    G.add_nodes_from(nodeId_array)
    # Add edges into G
    G.add_edges_from(edge_list)
    # Add attributes into G
    for node in list(G.nodes):
        G.nodes[node]['labels'] = gang_labels[node-1]
        G.nodes[node]['hie_attribute'] = hie_attribute[node-1]

    # print(f"G.nodes:{G.nodes(data=True)}")
    # print(f"G.edges():{G.edges()}")

    # Visualize a graph with community detection.
    visualization_graph(G)

    # Constructs a subgraph of gang members from the given edge list and visualize it
    SubG = constuct_subgraph(edge_list, gang_labels)
    visualization_graph(SubG, False)

    # Compute and visualize the closeness centrality of a subgraph
    # centrality_type (int): If 0, compute and visualize closeness centrality.If 1, compute and visualize betweenness centrality.
    compute_visualize_centrality(SubG, 0)
    compute_visualize_centrality(SubG, 1)

    # Define DeepWalk model
    model = DeepWalk(G, num_walks=300, walk_length=25)
    # Train model
    model.train()

    # Get the embeddings
    node_embeddings_dict = model.get_embeddings()
    # print(node_embeddings_dict)

    # Convert the embeddings from dictionary to list
    embeddings_list = np.array(
        [node_embeddings_dict[str(node)] for node in G.nodes()])
    # print(embeddings_list)
    # Perform the community detection task
    cd = CommunityDetection(G, embeddings_list)
    cd.cluster()  # clustering task
    silhouette, accuracy, nmi = cd.evaluate(gang_labels)

    print('The model silhouette=', silhouette)
    print('The model accuracy=', accuracy)
    print('The model normalized mutual information=', nmi)

    # Get the current time and format it
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'embedding/output_data_{timestamp}.json'

    # Save embeddings_list and metrics to a file
    output_data = {
        "embeddings_list": embeddings_list.tolist(),  # Convert numpy array to list
        "metrics": {
            "silhouette": float(silhouette),
            "accuracy": float(accuracy),
            "normalized_mutual_information": float(nmi)
        }
    }

    # Write to a JSON file
    with open(file_name, 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"Data saved to {file_name}")

    # Visualizes node embeddings using t-SNE.
    plot_embedding(G, embeddings_list)
