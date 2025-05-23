import sys
sys.path.append('complex-network\model')
from flask import Flask, request, jsonify
from flask_cors import CORS
import global_visulization_echarts, node_embeddings_visualization_echarts, subgraph_visualization_echarts, centrality_visual_echarts, comdec_visualization_echarts
import logging
 
# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors=CORS(app, origins=["http://localhost:8081"])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upAttributes', methods=['POST'])
def upAttributes():
    try:
            file = request.files['file']
            file.save(r'complex-network\data\Sweden_gang_attributes.txt')
            return jsonify({"上传成功":''}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upEdgelist', methods=['POST'])
def upEdgelist():
    try:
            file = request.files['file']
            file.save(r'complex-network\data\Sweden_gang_edgelist.txt')
            return jsonify({"上传成功":''}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/subGraphSeries', methods=['POST'])
def subGraphSeries():
    try:
        result = subgraph_visualization_echarts.subgraph()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nodeEmbeddingChartsSeries', methods=['POST'])
def nodeEmbeddingChartsSeries():
    try:
        result = node_embeddings_visualization_echarts.node()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/minedCommunityGraphSeries', methods=['POST'])
def minedCommunityGraphSeries():
    try:
        result = comdec_visualization_echarts.comdec()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/globalGraphSeries', methods=['POST'])
def globalGraphSeries():
    try:
        result = global_visulization_echarts.global_graph()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/centralityGraphsSeries1', methods=['POST'])
def centralityGraphsSeries1():
    try:
        result = centrality_visual_echarts.centrality()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)