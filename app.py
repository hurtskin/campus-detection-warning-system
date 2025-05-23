from flask import Flask, request, jsonify
import label_of_people.get_label as two
from opinionOnCampus.predict import predict
from flask_cors import CORS
import sys
sys.path.append(r"complex-network")
from networksmodel import global_visulization_echarts, node_embeddings_visualization_echarts, subgraph_visualization_echarts, centrality_visual_echarts, comdec_visualization_echarts
import logging
from neo4j import show_neo4j
import pandas as pd
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors=CORS(app, origins=["http://localhost:8081"])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/api/data', methods=['GET'])
def get_data():
    # 读取 Excel 数据
    df = pd.read_excel('data.xlsx')
    # 将数据转换为 JSON 格式
    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/get_label', methods=['POST'])
def get_label():
    """
    输入: 
    - 如果是JSON格式，输入:
    {
        "number": int  # 用于获取标签的数字索引
    }
    - 如果是上传文件，输入:
    {
        file: File  # 需要上传的文本文件
    }
    输出:
    {
        "label_name": "label_value"  # 标签对应的值
    }
    """
    try:
        if not request.is_json:
            file = request.files['file']
            file.save(r'label_of_people\学生心理健康风险等级预测.xlsx')
            return jsonify({'result': two.get_len()}),200
        else:
            data = request.get_json()
            number = data.get('number')

            try:
                number = int(number)
            except ValueError:
                return jsonify({"error": "Invalid number format"}), 400
        
            result = two.get_label_of_people()
            for i in result:
                result[i] = result[i][number]
            
            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# 允许跨域（前端在不同域名时需要）

@app.route('/get_label/redata', methods=['POST'])
def get_label_redata():
    try:
        if request.is_json:
            data = request.get_json()
            number = data.get('number')

            if number is not None:
                try:
                    number = int(number)
                    original_data = two.get_label_of_people()
                    
                    # 转换为标准化列表（修复点：确保格式化仅用于数值）
                    converted_data = [
                        {"分类": k, "数值": f"{v:.2f}"} 
                        for k, v in original_data.items()
                    ]
                    
                    if number < len(converted_data):
                        # 返回单个条目（注意：这里不需要额外格式化）
                        return jsonify([converted_data[number]])
                    else:
                        return jsonify({"error": "number 超出范围"}), 400
                except ValueError:
                    return jsonify({"error": "Invalid number format"}), 400
            else:
                original_data = two.get_label_of_people()
                converted_data = [
                    {"分类": k, "数值": f"{v:.2f}"} 
                    for k, v in original_data.items()
                ]
                # 直接返回列表，不格式化（修复点）
                return jsonify(converted_data)
        
        else:
            # 文件上传逻辑（保持不变）
            file = request.files['file']
            file.save(r'label_of_people\学生心理健康风险等级预测.xlsx')
            return jsonify({'result': two.get_len()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/random-sample', methods=['GET'])
def get_random_sample():
    file_path = "Campus_public_opinion_text_corpus.csv"  # 替换为你的CSV文件路径
    sample_size = 20
    
    try:
        # 使用pandas读取（推荐）
        df = pd.read_csv(file_path)
        total_rows = len(df)
        
        if total_rows < sample_size:
            return make_response(jsonify({
                "success": False,
                "message": f"数据不足{sample_size}条（当前{total_rows}条）",
                "data": []
            }), 400)
            
        sample_data = df.sample(n=sample_size).to_dict('records')
        return jsonify({
            "success": True,
            "message": f"成功获取{sample_size}条随机数据",
            "data": sample_data
        })
        
    except FileNotFoundError:
        return make_response(jsonify({
            "success": False,
            "message": "CSV文件未找到",
            "data": []
        }), 404)
    except Exception as e:
        return make_response(jsonify({
            "success": False,
            "message": f"处理错误：{str(e)}",
            "data": []
        }), 500)
@app.route('/predict', methods=['POST'])
def predict_sentiment():
    """
    输入:
    - 如果是JSON格式，输入:
    {
        "text": str  # 需要分析情感的文本
    }
    - 如果是上传文件，输入:
    {
        file: File  # 需要上传的文本文件
    }
    输出:
    {
        "text": str,  # 原始文本
        "sentiment_code": str  # 预测的情感类别
    }
    """
    try:
        if not request.is_json:
            file = request.files['file']
            file.save(r'./txt/testdata.txt')
            text = None
            senti = predict.SentimentAnalyzer()
            sentiment_code = senti.sentiment_predict(text)
            return jsonify(sentiment_code), 200
        else:
            data = request.json
            text = data.get('text')
            senti = predict.SentimentAnalyzer()
            sentiment_code = senti.sentiment_predict(text)
            if type(sentiment_code) == str:
                return jsonify({
                    "text": text,
                    "sentiment_code": sentiment_code
                }), 200
            else:
                return jsonify(sentiment_code), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upAttributes', methods=['POST'])
def upAttributes():
    """
    输入:
    {
        file: File  # 需要上传的属性文件
    }
    输出:
    {
        "上传成功": ""  # 上传成功响应
    }
    """
    try:
        file = request.files['file']
        file.save(r'complex-network\data\Sweden_gang_attributes.txt')
        return jsonify({"上传成功":''}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upEdgelist', methods=['POST'])
def upEdgelist():
    """
    输入:
    {
        file: File  # 需要上传的边列表文件
    }
    输出:
    {
        "上传成功": ""  # 上传成功响应
    }
    """
    try:
        file = request.files['file']
        file.save(r'complex-network\data\Sweden_gang_edgelist.txt')
        return jsonify({"上传成功":''}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/subGraphSeries', methods=['POST'])
def subGraphSeries():
    """
    输入: 无
    输出:
    {
        "subgraph_visualization_data": []  # 返回子图数据
    }
    """
    try:
        result = subgraph_visualization_echarts.subgraph()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nodeEmbeddingChartsSeries', methods=['POST'])
def nodeEmbeddingChartsSeries():
    """
    输入: 无
    输出:
    {
        "node_embedding_visualization_data": []  # 返回节点嵌入数据
    }
    """
    try:
        result = node_embeddings_visualization_echarts.node()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/minedCommunityGraphSeries', methods=['POST'])
def minedCommunityGraphSeries():
    """
    输入: 无
    输出:
    {
        "community_graph_data": []  # 返回挖掘的社区图数据
    }
    """
    try:
        result = comdec_visualization_echarts.comdec()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/globalGraphSeries', methods=['POST'])
def globalGraphSeries():
    """
    输入: 无
    输出:
    {
        "global_graph_data": []  # 返回全局图数据
    }
    """
    try:
        result = global_visulization_echarts.global_graph()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/centralityGraphsSeries1', methods=['POST'])
def centralityGraphsSeries1():
    """
    输入: 无
    输出:
    {
        "centrality_graph_data": []  # 返回中心性图数据
    }
    """
    try:
        result = centrality_visual_echarts.centrality()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_neo4j', methods=['POST'])
def get_neo4j():
    """
    输入:
    {
        "text": str  # 查询Neo4j图数据库的文本
    }
    输出:
    {
        "neo4j_graph_data": []  # 返回Neo4j图数据
    }
    """
    data = request.get_json()
    text = data.get('text')
    result = show_neo4j.get_neo4j_graph(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
