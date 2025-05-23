import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE  # Dimension Reduction Tool
import time
import pyecharts.options as opts
from pyecharts.charts import Scatter


def read_edgelist(path: str):
    """
    Reads an edge list from a file and returns it as a list of tuples.

    Parameters:
    path (str): The path to the file containing the edge list.

    Returns:
    list: A list of tuples where each tuple represents an edge.
    """
    with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
        edge_list = []
        fin.readline()  # Skip the header line

        # Read the edge list
        while True:  # Infinite loop to read each line
            line = fin.readline().strip()  # Read and strip whitespace from the line
            if line == '':  # If the line is empty, end of file is reached
                break
            edge_list_item = line.split()  # Split the line into components
            # Convert components to integers and append as a tuple to edge_list
            edge_list.append((int(edge_list_item[0]), int(edge_list_item[1])))

    return edge_list  # Return the list of edges


def read_attributes(path: str):
    """
    Reads node attributes (node IDs, gang labels, hierarchy attributes) from a file.

    Parameters:
    path (str): The path to the file containing node attributes.

    Returns:
    tuple: Three lists containing node IDs, gang labels, and hierarchy attributes.
    """

    nodeId_list = []
    gang_list = []
    hie_list = []
    name_list = []

    with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
        # Skip lines until reaching the start of attributes
        while True:
            line = fin.readline().strip()
            if line == '*Vertices 234':  # Check for the start of attributes section
                break

        # Read attributes
        while True:
            line = fin.readline().strip()
            if line == '':  # Exit if reading into the end of the file
                break
            text_list = line.split()
            nodeId_list.append(text_list[0])
            gang_list.append(text_list[6])
            hie_list.append(text_list[8])
            name_list.append(text_list[-1])

    # Convert lists to appropriate data types and formats
    nodeId_array = np.array(list(map(int, nodeId_list)))
    gang_labels = [0 if gang == '0' else 1 for gang in gang_list]
    hie_attribute = list(map(int, hie_list))
    names = list(map(str, name_list))

    # Print and return results
    # print(f"nodeId_array: {nodeId_array}")
    # print(f"gang_labels: {gang_labels}")
    # print(f"hie_attribute: {hie_attribute}")

    return nodeId_array, gang_labels, hie_attribute, names


def visualization_graph(G: nx.Graph, mullabels: bool = True):
    """
    Visualizes a graph with community detection.

    Parameters:
    G (networkx.Graph): The input graph to be visualized. The graph should have
                        a node attribute 'labels' indicating the community 
                        each node belongs to. 
    mullabels (bool): Whether the graph contains multiple labels. True if yes, False otherwise.                    
    """
    # Set node colors based on their labels
    # Nodes with label 1 are colored red ('r'), others are colored yellow ('y')
    if mullabels:
        node_colors = ['r' if G.nodes[node]['labels']
                       == 1 else 'y' for node in G.nodes]

        # Draw the graph using Kamada-Kawai layout
        nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=True,
                node_color=node_colors, node_size=40, font_size=5)

        # Save the plot as an image file

    else:
        nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=True,
                node_size=200, font_size=10)

    # Set the title of the graph
    if mullabels:
        plt.title('Sweden Gang Graph containing all nodes')
        plt.savefig("pics/All_Graph.png", dpi=300)
    else:
        plt.title('Sweden Gang graph only containing gang members')
        plt.savefig("pics/Sub_Graph.png", dpi=300)

    # Display the graph
    plt.show()


def constuct_subgraph(edge_list: list[tuple], gang_labels: list[int]):
    """
    Constructs a subgraph of gang members from the given edge list.

    Parameters:
    edge_list (list of tuple): The list of edges where each edge is represented as a tuple (source, destination).
    gang_labels (list of int): The list of labels indicating whether a node is a gang member (1) or not (0).

    Returns:
    networkx.Graph: The subgraph containing only the nodes and edges where both nodes are gang members.
    """
    # Construct the subgraph for gang members
    sample_edge_list = []
    for source, dest in edge_list:
        if gang_labels[source-1] == 1 and gang_labels[dest-1] == 1:
            # Add edge to sample_edge_list if both nodes are gang members
            sample_edge_list.append((source, dest))

    SubG = nx.Graph()
    # Add edges to the subgraph
    SubG.add_edges_from(sample_edge_list)

    return SubG


def constuct_subgraph_echarts(edges_list: list, attributes_dict: dict) -> tuple[list, list]:
    """
    构建子图数据。

    根据给定的边列表和节点属性字典，构造一个新的子图，其中只包含满足特定条件的节点和边。

    参数:
    edges_list (list): 一个包含所有边的列表，每个边由一个源节点和一个目标节点组成。
    attributes_dict (dict): 一个字典，其中键是节点，值是一个列表，其中第一个元素是决定节点是否被包含的属性。

    返回:
    tuple[list, list]: 一个包含两个列表的元组，第一个列表是子图中的节点，第二个列表是子图中的边。
    """
    # 初始化空的边和节点列表
    sample_edge_list = []
    sample_node_lst = []
    # 创建一个空集合，用于存储唯一的节点
    edge_set = set()

    # 遍历所有边，筛选出符合条件的边
    for source, dest in edges_list:
        # 如果源节点和目标节点都满足条件，则将这条边添加到子图边列表中
        if attributes_dict[source][0] == 1 and attributes_dict[dest][0] == 1:
            sample_edge_list.append((source, dest))

    # 遍历筛选后的边列表，将所有涉及的节点添加到集合中，自动去重
    for edge in sample_edge_list:
        edge_set.update(edge)  # 更新集合，添加元组中的所有元素

    # 将集合转换为列表，得到所有唯一的节点
    sample_node_lst = list(edge_set)

    # 返回子图中的节点列表和边列表
    return sample_node_lst, sample_edge_list


def compute_visualize_centrality(G: nx.Graph, centrality_type: int):
    """
    Computes and visualizes either the closeness centrality or betweenness centrality of a graph.

    Parameters:
    G (networkx.Graph): The input graph to be visualized.
    centrality_type (int): If 0, compute and visualize closeness centrality.
                            If 1, compute and visualize betweenness centrality.

    This function:
    - Computes the specified centrality of the graph.
    - Prints the nodes sorted by their centrality values in descending order.
    - Visualizes the graph with node colors representing the centrality values.
    """

    # Compute the specified centrality
    if centrality_type == 0:
        centrality_dict = nx.closeness_centrality(G)
        centrality_label = "Closeness centrality"
    elif centrality_type == 1:
        centrality_dict = nx.betweenness_centrality(G)
        centrality_label = "Betweenness centrality"
    else:
        print("Centrality type is wrong")
        return

    # Print the sorted centrality values
    sorted_centrality_dict = dict(
        sorted(centrality_dict.items(), key=lambda item: item[1], reverse=True))
    # print(f"{centrality_label}: {sorted_centrality_dict}")

    # Extract the centrality values
    cen_val = list(centrality_dict.values())

    # Normalize the centrality values to the range [0.0, 1.0] with MinMax normalization
    norm = plt.Normalize(vmin=min(cen_val), vmax=max(cen_val))

    # Use the 'Reds' colormap
    cmap = plt.cm.Reds

    # Map all normalized values to RGBA (Red, Green, Blue, Alpha) values
    node_colors = cmap(norm(cen_val))

    # Draw the graph with node colors representing centrality values
    fig, ax = plt.subplots()
    nx.draw(G, pos=nx.spring_layout(G), node_color=node_colors,
            with_labels=True, node_size=200, font_size=10)

    # Create a ScalarMappable and color bar to represent the centrality values
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(cen_val)
    cbar = plt.colorbar(sm, ax=ax)

    cbar.set_label(centrality_label)
    plt.savefig(f"pics/{centrality_label}.png", dpi=300)
    # Display the plot
    plt.show()

def compute_centrality_echarts(G: nx.Graph, centrality_type: int):
    """
    Computes and visualizes either the closeness centrality or betweenness centrality of a graph.

    Parameters:
    G (networkx.Graph): The input graph to be visualized.
    centrality_type (int): If 0, compute and visualize closeness centrality.
                            If 1, compute and visualize betweenness centrality.

    This function:
    - Computes the specified centrality of the graph.
    - Prints the nodes sorted by their centrality values in descending order.
    - Visualizes the graph with node colors representing the centrality values.
    """

    # Compute the specified centrality
    if centrality_type == 0:
        centrality_dict = nx.closeness_centrality(G)
        centrality_label = "Closeness centrality"
    elif centrality_type == 1:
        centrality_dict = nx.betweenness_centrality(G)
        centrality_label = "Betweenness centrality"
    else:
        print("Centrality type is wrong")
        return

    # Print the sorted centrality values
    sorted_centrality_dict = dict(
        sorted(centrality_dict.items(), key=lambda item: item[1], reverse=True))
    # print(f"{centrality_label}: {sorted_centrality_dict}")
    
    if centrality_type == 0:
        transformed_dict = {key: int(((value*100) ** 2)/70) for key, value in sorted_centrality_dict.items()}
    
    else:
        transformed_dict = {key: int((value*100) + 10) for key, value in sorted_centrality_dict.items()}
    return transformed_dict


def plot_embedding_echarts(G: nx.Graph, embeddings_list: list[list]):
    """
    Visualizes node embeddings using t-SNE.

    Parameters:
    G (networkx.Graph): The graph containing nodes and edges.
    embeddings_list (list[list]): The list of node embeddings.

    Returns:
    None
    """
    # Apply t-SNE to reduce embeddings to 2D
    tsne = TSNE(n_components=2, init='pca', random_state=0, n_iter=500)
    node_embeddings_2d = tsne.fit_transform(embeddings_list).tolist()

    # Get node colors based on community labels
    node_colors = ['red' if G.nodes[node]['labels'] == 1 else 'yellow' for node in G.nodes]
    
    # 获取x_data和y_data的最小值和最大值
    x_min = np.min(np.array(node_embeddings_2d)[:, 0])
    x_max = np.max(np.array(node_embeddings_2d)[:, 0])
    y_min = np.min(np.array(node_embeddings_2d)[:, 1])
    y_max = np.max(np.array(node_embeddings_2d)[:, 1])
    
    # 根据标签划分节点
    class_0 = [node_embeddings_2d[i] for i, node in enumerate(G.nodes) if G.nodes[node]['labels'] == 0]
    class_1 = [node_embeddings_2d[i] for i, node in enumerate(G.nodes) if G.nodes[node]['labels'] == 1]
    # 创建一个 Scatter 对象
    scatter = (
        Scatter()
        .add_xaxis(xaxis_data=[item[0] for item in class_0])  # 添加 x 轴的数据
        .add_yaxis(
            series_name="community 1",  
            y_axis=[item[1] for item in class_0],  # y 轴的数据
            symbol_size=5,  # 散点大小
            itemstyle_opts=opts.ItemStyleOpts(color="blue"),  # 设置颜色,
        )
        .add_xaxis(xaxis_data=[item[0] for item in class_1])  # 添加 x 轴的数据
        .add_yaxis(
            series_name="community 2",  # 图表系列名称
            y_axis=[item[1] for item in class_1],  # y 轴的数据
            symbol_size=5,  # 散点大小
            itemstyle_opts=opts.ItemStyleOpts(color="red"),  # 设置颜色,
        )
        
        
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Node Embeddings Visualization"),  # 设置标题
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=""
            ),
            xaxis_opts=opts.AxisOpts(type_="value", min_=x_min - 1, max_=x_max + 1),
            yaxis_opts=opts.AxisOpts(type_="value", min_=y_min - 1, max_=y_max + 1),
        )
        .set_series_opts(  # 设置系列配置项
            label_opts=opts.LabelOpts(is_show=False),  # 设置节点标签不显示
        )
    )

    # 渲染图表到 HTML 文件
    scatter.render("node_embedding_charts.html")


def plot_embedding(G: nx.Graph, embeddings_list: list[list]):
    """
    Visualizes node embeddings using t-SNE.

    Parameters:
    G (networkx.Graph): The graph containing nodes and edges.
    embeddings_list (list[list]): The list of node embeddings.

    Returns:
    None
    """
    # Apply t-SNE to reduce embeddings to 2D
    # n_components: Dimension of the embedded space (2 for 2D visualization)
    # n_iter: Maximum number of iterations for the optimization. Should be at least 250.
    tsne = TSNE(n_components=2, init='pca')
    node_embeddings_2d = tsne.fit_transform(embeddings_list)

    # Get node colors based on community labels
    # Nodes with label 1 are colored red ('r'), others are colored yellow ('y')
    node_colors = ['r' if G.nodes[node]['labels']
                   == 1 else 'y' for node in G.nodes]

    # Solve font issues for displaying Chinese characters
    # Used to display Chinese labels
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # Used to display the negative sign normally
    plt.rcParams['axes.unicode_minus'] = False

    # Create a scatter plot for the embeddings
    for i, label in enumerate(G.nodes()):
        x, y = node_embeddings_2d[i, :]
        plt.scatter(x, y, c=node_colors[i])

    # Set the title and labels of the plot
    plt.title("t-SNE嵌入可视化")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")

    # Save the plot to a file with high resolution
    plt.savefig(
        f"pics/embeddings_{time.strftime('%Y%m%d_%H%M%S')}.png", dpi=300)

    # Show the plot
    plt.show()
