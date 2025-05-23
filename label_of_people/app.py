from flask import Flask, request, jsonify
import label_of_people.get_label as get_label 
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:8081"])

@app.route('/get_label', methods=['POST'])
def get_label():
    # 从请求中获取数字
    data = request.get_json()
    number = data.get('number')
    
    if number is None:
        return jsonify({"error": "No number provided"}), 400
    
    try:
        # 将数字转换为整数（或浮点数，根据你的需求）
        number = int(number)
    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    
    # 调用算法函数，注意使用 two. 前缀
    result = get_label.get_label_of_people()
    for i in result:
        result[i] = result[i][number]
    
    
    # 返回结果
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)