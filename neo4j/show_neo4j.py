    # -*- coding: utf-8 -*-

from py2neo import Graph
from pyvis.network import Network

def get_neo4j_graph(namenode=None):
    # 连接到 Neo4j 数据库
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

    if namenode:
        query = """
        MATCH (n)-[r]->(m)
        WHERE n.name CONTAINS $name OR m.name CONTAINS $name
        RETURN n.name AS source, type(r) AS relationship, m.name AS target
        """
        result = graph.run(query, name=namenode)
        
    else:        # 查询数据
        query = """
        MATCH (n)-[r]->(m)
        WHERE n.name IS NOT NULL AND m.name IS NOT NULL
        RETURN n.name AS source, type(r) AS relationship, m.name AS target
        """
        result = graph.run(query)

    # 创建 pyvis 网络图
    net = Network(height="750px", width="100%", notebook=True, directed=True)

    # 添加节点和边
    for record in result:
        source = record["source"]
        target = record["target"]
        relationship = record["relationship"]

        # 添加节点
        net.add_node(source, label=source, title=source, color="skyblue")
        net.add_node(target, label=target, title=target, color="lightgreen")

        # 添加关系（边）
        net.add_edge(source, target, title=relationship, label=relationship, color="gray")


    graph_data = {
        "nodes": net.nodes,
        "edges": net.edges
    }

    return graph_data
