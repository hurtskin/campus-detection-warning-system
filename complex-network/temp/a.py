# echarts.min.js官网地址 https://echarts.apache.org/zh/index.html
from pyecharts.globals import CurrentConfig
from pyecharts.charts import Graph
from pyecharts import options as opts

# 将echarts.min.js渲染配置在本地路径
CurrentConfig.ONLINE_HOST = './'

from pyecharts.charts import Graph
from pyecharts import options as opts

# 定义节点列表
nodes = [
    opts.GraphNode(name="Alice", symbol_size=20, itemstyle_opts=opts.ItemStyleOpts(color="#87CEFA")),  # Light Blue
    opts.GraphNode(name="Bob", symbol_size=15, itemstyle_opts=opts.ItemStyleOpts(color="#FFA07A")),  # Salmon
    opts.GraphNode(name="Charlie", symbol_size=10, itemstyle_opts=opts.ItemStyleOpts(color="#7FFFD4")),  # Aqua
    opts.GraphNode(name="Company A", symbol_size=25, itemstyle_opts=opts.ItemStyleOpts(color="#DC143C")),  # Crimson
]

# 定义边列表
links = [
    opts.GraphLink(source="Alice", target="Company A"),
    opts.GraphLink(source="Bob", target="Company A"),
    opts.GraphLink(source="Charlie", target="Company A"),
]

# 创建图谱实例
graph = (
    Graph()
    # Add nodes and links to the graph, with a repulsion force set for layout aesthetics, and enable node dragging for interactivity
    .add("", nodes, links, repulsion=50, is_draggable=True)
    # Set global configuration options, such as the title of the chart
    .set_global_opts(title_opts=opts.TitleOpts(title="Knowledge Graph"))
    # Set series-specific configuration options, such as label display and line style
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    )
)

# 渲染图表
graph.render("knowledge_graph.html")