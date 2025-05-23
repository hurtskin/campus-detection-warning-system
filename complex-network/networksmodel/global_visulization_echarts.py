import json
import sys
# Set root path
sys.path.append(r"complex-network")
from utils.util import *
from pyecharts import options as opts
from pyecharts.charts import Graph
import pandas as pd
#\中环\科研与教研与企业特派员项目\科研\2021市教委自然科学基金项目材料\项目结项\结项代码\任务三\

def global_graph():
    # Reads an edge list from a file and returns it as a list of tuples.
    edge_list = read_edgelist(r"complex-network/data/Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from
    # a file and return three lists containing node IDs, gang labels, and hierarchy attributes
    nodeId_array, gang_labels, hie_attribute, names = read_attributes(
        "complex-network/data/Sweden_gang_attributes.txt")

    # 提取节点和边信息
    nodes = []
    links = []

    for i, node in enumerate(nodeId_array):
        nodes.append({
            'name': str(node),
            'fixed': 'false',
            'symbolSize': 30,
            'itemStyle': {
            'color': '#87CEFA'
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
