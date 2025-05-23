import sys
# Set root path
sys.path.append(r"complex-network")

import networkx as nx
import pandas as pd
from pyecharts.charts import Graph
from pyecharts import options as opts
from utils.util import *
import json

def centrality():

    sample_edge_list = []
    sample_node_list = []

    # Reads an edge list from a file and returns it as a list of tuples.
    edges_list = read_edgelist("complex-network\data\Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from
    # a file and return three lists containing node IDs, gang labels, and hierarchy attributes
    nodeId_array, gang_labels, hie_attribute, names = read_attributes(
        "complex-network\data\Sweden_gang_attributes.txt")

    # Generate a dictionary that maps node IDs to their gang labels and hierarchy attributes
    attributes_dict = {nodeId: (gang_label, hie_attr, names) for nodeId, gang_label, hie_attr, names in zip(
        nodeId_array, gang_labels, hie_attribute, names)}

    sample_node_list, sample_edge_list = constuct_subgraph_echarts(
        edges_list, attributes_dict)

    # 创建带有标签的真实子图
    # 设置不同社团节点颜色，标签1为浅橙色，标签2为浅蓝色
    node_colors = [
    "#7FFFD4" if attributes_dict[node][1] == 2 
    else "#FFA07A" if attributes_dict[node][1] == 3 
    else "#DC143C"
    for node in sample_node_list
    ] 
    nodes = []
    links = []   
    for i, node in enumerate(sample_node_list):
        nodes.append({
            'name': str(node),
            'fixed': 'false',
            'symbolSize': 30,
            'itemStyle': {
            'color': node_colors[i]
            },
            'emphasis': {},
            'blur': {},
            'select': {},
            'tooltip': {
            'show': 'true',
            'trigger': 'item',
            'triggerOn': 'mousemove|click',
            'axisPointer': {
                'type': 'line'
            },
            'showContent': 'true',
            'alwaysShowContent': 'false',
            'showDelay': 0,
            'hideDelay': 100,
            'enterable': 'false',
            'confine': 'false',
            'appendToBody': 'false',
            'transitionDuration': 0.4,
            'formatter': f"<br/>Name: {attributes_dict[node][2]}<br/>label: {attributes_dict[node][0]}<br/>Hierarchy: {attributes_dict[node][1]}",
            'textStyle': {
                'fontSize': 14
            },
            'borderWidth': 0,
            'padding': 5,
            'order': 'seriesAsc'
            }
        })

    for edge in sample_edge_list:
        links.append(
            {
              'source': str(edge[0]),
              'target': str(edge[1]),
              'emphasis': {},
              'blur': {},
              'select': {},
              'ignoreForceLayout': 'false'
            },
        )   
    
    SubG = nx.Graph()
    # Add edges to the subgraph
    SubG.add_edges_from(sample_edge_list)

    closeness_dict = compute_centrality_echarts(SubG, 0)
    betweeness_dict = compute_centrality_echarts(SubG, 1)
    
    # 创建接近中心性子图
    nodes_c = []
    links_c = [] 
    
    for i, node in enumerate(sample_node_list):
        nodes_c.append({
            'name': str(node),
            'fixed': 'false',
            'symbolSize': closeness_dict[node],
            'itemStyle': {
            'color': "#FFA07A"
            },
            'emphasis': {},
            'blur': {},
            'select': {},
            'tooltip': {
            'show': 'true',
            'trigger': 'item',
            'triggerOn': 'mousemove|click',
            'axisPointer': {
                'type': 'line'
            },
            'showContent': 'true',
            'alwaysShowContent': 'false',
            'showDelay': 0,
            'hideDelay': 100,
            'enterable': 'false',
            'confine': 'false',
            'appendToBody': 'false',
            'transitionDuration': 0.4,
            'formatter': f"<br/>Name: {attributes_dict[node][2]}<br/>label: {attributes_dict[node][0]}<br/>Hierarchy: {attributes_dict[node][1]}",
            'textStyle': {
                'fontSize': 14
            },
            'borderWidth': 0,
            'padding': 5,
            'order': 'seriesAsc'
            }
        })

    for edge in sample_edge_list:
        links_c.append(
            {
            'source': str(edge[0]),
            'target': str(edge[1]),
            'emphasis': {},
            'blur': {},
            'select': {},
            'ignoreForceLayout': 'false'
            },
        )
    
    # 创建介数中心性子图
    nodes_b = []
    links_b = [] 

    for i, node in enumerate(sample_node_list):
        nodes_b.append({
            'name': str(node),
            'fixed': 'false',
            'symbolSize': betweeness_dict[node],
            'itemStyle': {
            'color': "#87CEFA"
            },
            'emphasis': {},
            'blur': {},
            'select': {},
            'tooltip': {
            'show': 'true',
            'trigger': 'item',
            'triggerOn': 'mousemove|click',
            'axisPointer': {
                'type': 'line'
            },
            'showContent': 'true',
            'alwaysShowContent': 'false',
            'showDelay': 0,
            'hideDelay': 100,
            'enterable': 'false',
            'confine': 'false',
            'appendToBody': 'false',
            'transitionDuration': 0.4,
            'formatter': f"<br/>Name: {attributes_dict[node][2]}<br/>label: {attributes_dict[node][0]}<br/>Hierarchy: {attributes_dict[node][1]}",
            'textStyle': {
                'fontSize': 14
            },
            'borderWidth': 0,
            'padding': 5,
            'order': 'seriesAsc'
            }
        })

    for edge in sample_edge_list:
        links_b.append(
            {
            'source': str(edge[0]),
            'target': str(edge[1]),
            'emphasis': {},
            'blur': {},
            'select': {},
            'ignoreForceLayout': 'false'
            },
        )

    result = {
        "nodes": nodes,
        "links": links,
        "nodes_c": nodes_c,
        "links_c": links_c,
        "nodes_b": nodes_b,
        "links_b": links_b
    }


    return result
