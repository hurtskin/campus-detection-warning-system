from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict
import logging
 
# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors=CORS(app, origins=["http://localhost:8081"])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    try:
        if not request.is_json:
            file = request.files['file']
            file.save(r'./txt/testdata.txt')
            text = None
            senti = predict.SentimentAnalyzer()
            sentiment_code = senti.sentiment_predict(text)
            return jsonify(sentiment_code), 200
        else:
            # 获取请求中的文本数据
            data = request.json
            text = data.get('text')
            # 调用predict.py中的predict_sentiment函数
            senti = predict.SentimentAnalyzer()
            sentiment_code = senti.sentiment_predict(text)
            # 返回JSON结果
            if type(sentiment_code) == str:
                return jsonify({
                    "text": text,
                    "sentiment_code": sentiment_code
                }), 200
            else:
                return jsonify(sentiment_code), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)




# curl -X POST -H "Content-Type: application/json" -d '{"text": "我今天很开心"}' http://localhost:5000/predict 
# 终端中请求示例（实际应用中应该改为在VUE框架下使用类axios的第三方库来发送HTTP请求






