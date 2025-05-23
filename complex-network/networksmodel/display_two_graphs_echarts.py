import sys
# Set root path
sys.path.append(r"D:\中环\科研与教研与企业特派员项目\科研\2021市教委自然科学基金项目材料\项目结项\结项代码\任务三\deepwalk_Sweden_gang_echarts")
from utils.util import *
from pyecharts import options as opts
from pyecharts.charts import Graph
import pandas as pd



if __name__ == "__main__":

    nodes = []
    links = []
    sample_edge_list = []
    sample_node_lst = []
    # Reads an edge list from a file and returns it as a list of tuples.
    edges_list = read_edgelist("data/Sweden_gang_edgelist.txt")

    # Reads node attributes (node IDs, gang labels, hierarchy attributes) from
    # a file and return three lists containing node IDs, gang labels, and hierarchy attributes
    nodeId_array, gang_labels, hie_attribute = read_attributes(
        "data/Sweden_gang_attributes.txt")

    # Generate a dictionary that maps node IDs to their gang labels and hierarchy attributes
    attributes_dict = {nodeId: (gang_label, hie_attr) for nodeId, gang_label, hie_attr in zip(
        nodeId_array, gang_labels, hie_attribute)}

    sample_node_list, sample_edge_list = constuct_subgraph_echarts(
        edges_list, attributes_dict)
    
    
    # 设置不同社团节点颜色，标签1为浅橙色，标签2为浅蓝色
    node_colors = [
    "#7FFFD4" if attributes_dict[node][1] == 2 
    else "#FFA07A" if attributes_dict[node][1] == 3 
    else "#DC143C"
    for node in sample_node_list
    ]    
    # 遍历节点ID数组，为每个节点创建GraphNode对象，并添加到nodes列表中
    for i, node in enumerate(sample_node_list):
        # 根据节点ID和相关属性，初始化GraphNode对象
        nodes.append(
            opts.GraphNode(
                name=str(node),  # 节点名称
                symbol_size=30,  # 节点符号大小
                itemstyle_opts=opts.ItemStyleOpts(
                    color=node_colors[i] ),  # 节点样式配置，设置颜色为浅橙色
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",  # 工具提示触发类型为“item”
                    # 工具提示的内容格式化，包含黑帮标签和层级信息
                    formatter=f"<br/>label: {attributes_dict[node][0]}<br/>Hierarchy: {attributes_dict[node][1]}"
                )
            )
        )

    # 创建图谱边表
    for edge in sample_edge_list:
        links.append(
            opts.GraphLink(
                source=str(edge[0]),
                target=str(edge[1]),
            )
        )
    
    # 创建图谱实例
    graph = (
        Graph(init_opts=opts.InitOpts(
            width='1200px', height='800px'))  # 初始化图谱的宽度和高度
        # 添加节点和链接，设置节点之间的排斥力和布局方式
        .add("", nodes, links, repulsion=100, is_draggable=True, layout="force")
        .set_global_opts(  # 设置全局配置项
            title_opts=opts.TitleOpts(  # 设置标题配置项
                title="挖掘出的风险社团关系图谱",  # 设置标题文本
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=20)  # 设置标题文本样式
            )
        )
        .set_series_opts(  # 设置系列配置项
            label_opts=opts.LabelOpts(  # 设置标签配置项
                is_show=True, font_size=10),  # 设置标签显示位置和字体大小
            linestyle_opts=opts.LineStyleOpts(curve=0.1)

        )
    )
    # 创建图谱实例
    graph1 = (
        Graph(init_opts=opts.InitOpts(
            width='1200px', height='800px'))  # 初始化图谱的宽度和高度
        # 添加节点和链接，设置节点之间的排斥力和布局方式
        .add("", nodes, links, repulsion=100, is_draggable=True, layout="force")
        .set_global_opts(  # 设置全局配置项
            title_opts=opts.TitleOpts(  # 设置标题配置项
                title="挖掘出的风险社团关系图谱",  # 设置标题文本
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=20)  # 设置标题文本样式
            )
        )
        .set_series_opts(  # 设置系列配置项
            label_opts=opts.LabelOpts(  # 设置标签配置项
                is_show=True, font_size=10),  # 设置标签显示位置和字体大小
            linestyle_opts=opts.LineStyleOpts(curve=0.1)

        )
    )
    # 生成 HTML 文件
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Two Knowledge Graphs</title>
        <!-- 引入 ECharts 文件 -->
        <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
    </head>
    <body>
        <div id="chart1" style="width: 600px; height: 400px;"></div>
        <div id="chart2" style="width: 600px; height: 400px;"></div>
        <script>
            // 初始化第一个图谱
            var chart1 = echarts.init(document.getElementById('chart1'));
            chart1.setOption(%s);

            // 初始化第二个图谱
            var chart2 = echarts.init(document.getElementById('chart2'));
            chart2.setOption(%s);
        </script>
    </body>
    </html>
    """ % (graph1.dump_options_with_quotes(), graph.dump_options_with_quotes())

    # 写入 HTML 文件
    with open("display_two_graphs.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
