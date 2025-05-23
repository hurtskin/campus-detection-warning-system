import sys
# Set root path
sys.path.append(r"complex-network")
from datetime import datetime
import json
from utils.util import *
from utils.com_dec import *
import matplotlib.pyplot as plt
from networksmodel.deepwalk import *




def node():

    # Reads an edge list from a file and returns it as a list of tuples.
    edge_list = read_edgelist("complex-network/data/Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from a file
    nodeId_array, gang_labels, hie_attribute, _ = read_attributes("complex-network/data/Sweden_gang_attributes.txt")

    # Create an undirected graph
    G = nx.Graph()
    G.add_nodes_from(nodeId_array)
    G.add_edges_from(edge_list)

    for i, node in enumerate(nodeId_array):
        G.nodes[node]['labels'] = gang_labels[i]
        G.nodes[node]['hie_attribute'] = hie_attribute[i]

    # Define DeepWalk model
    model = DeepWalk(G, num_walks=300, walk_length=25)
    model.train()

    # Get the embeddings
    node_embeddings_dict = model.get_embeddings()
    embeddings_list = np.array([node_embeddings_dict[str(node)] for node in G.nodes()])

    # Apply t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, init='pca', random_state=0, n_iter=500)
    node_embeddings_2d = tsne.fit_transform(embeddings_list).tolist()

    # 根据标签划分节点
    class_0 = [node_embeddings_2d[i] for i, node in enumerate(G.nodes) if G.nodes[node]['labels'] == 0]
    class_1 = [node_embeddings_2d[i] for i, node in enumerate(G.nodes) if G.nodes[node]['labels'] == 1]

    # 获取 x_data 和 y_data 的最小值和最大值
    x_min = np.min(np.array(node_embeddings_2d)[:, 0])
    x_max = np.max(np.array(node_embeddings_2d)[:, 0])
    y_min = np.min(np.array(node_embeddings_2d)[:, 1])
    y_max = np.max(np.array(node_embeddings_2d)[:, 1])

    # 构造前端所需的 JSON 数据
    chart_data = {
        "series": [
            {
                "type": "scatter",
                "name": "community 1",
                "symbolSize": 5,
                "data": class_0,
                "itemStyle": {"color": "blue"},
            },
            {
                "type": "scatter",
                "name": "community 2",
                "symbolSize": 5,
                "data": class_1,
                "itemStyle": {"color": "red"},
            },
        ],
        "xAxis": [
            {
                "type": "value",
                "min": x_min - 1,
                "max": x_max + 1,
            }
        ],
        "yAxis": [
            {
                "type": "value",
                "min": y_min - 1,
                "max": y_max + 1,
            }
        ],
        "title": {
            "text": "Node Embeddings Visualization",
        },
    }
    
    return chart_data

