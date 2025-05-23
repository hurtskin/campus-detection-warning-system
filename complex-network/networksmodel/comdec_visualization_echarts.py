import sys
# Set root path
sys.path.append(r"complex-network")
from utils.util import *
from pyecharts import options as opts
from pyecharts.charts import Graph
import pandas as pd
import json

#if __name__ == "__main__":
def comdec():
    # Reads an edge list from a file and returns it as a list of tuples.
    edge_list = read_edgelist("complex-network\data\Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from
    # a file and return three lists containing node IDs, gang labels, and hierarchy attributes
    nodeId_array, gang_labels, hie_attribute, names = read_attributes(
        "complex-network\data\Sweden_gang_attributes.txt")

    # 提取节点和边信息
    nodes = []
    links = []
    
    # 设置不同社团节点颜色，标签1为浅橙色，标签2为浅蓝色
    node_colors = ["#FFA07A" if label == 1 else "#87CEFA" for label in gang_labels]

    for i, node in enumerate(nodeId_array):
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
            'formatter': f"<br/>Name: {names[i]}<br/>label: {gang_labels[i]}<br/>Hierarchy: {hie_attribute[i]}",
            'textStyle': {
                'fontSize': 14
            },
            'borderWidth': 0,
            'padding': 5,
            'order': 'seriesAsc'
            }
        })

    for edge in edge_list:
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
    
    result = {
        "nodes": nodes,
        "links": links
    }
 


    return result

