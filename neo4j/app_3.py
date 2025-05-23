from flask import Flask, request, jsonify
import show_neo4j
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:8081"])

@app.route('/get_neo4j', methods=['POST'])
def get_neo4j():
    print(1)
    # 从请求中获取数字
    data = request.get_json()
    text = data.get('text')
    
    
    # 调用算法函数，注意使用 two. 前缀
    result = show_neo4j.get_neo4j_graph(text)
    
    # 返回结果
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)