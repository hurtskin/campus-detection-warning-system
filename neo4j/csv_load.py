from py2neo import Graph, Node, Relationship
import csv

# 连接 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

# 读取 CSV 文件并导入数据
def import_csv_to_neo4j(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 创建节点
            source_node = Node("Entity", name=row['Source'])
            target_node = Node("Entity", name=row['Target'])
            
            # 创建关系
            relationship = Relationship(source_node, row['Relationship'], target_node)
            
            # 合并到图数据库（避免重复创建）
            graph.merge(source_node, "Entity", "name")
            graph.merge(target_node, "Entity", "name")
            graph.merge(relationship)

# 执行导入
import_csv_to_neo4j(r"neo4j\data.csv")

print("数据导入完成！")
