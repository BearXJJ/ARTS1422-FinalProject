from flask import Flask, jsonify
import os
import json
from flask_cors import CORS  # 导入 CORS 扩展

app = Flask(__name__)
port = 3000

# 启用 CORS，允许所有来源的请求
CORS(app)

# 获取当前文件所在目录的路径
base_dir = os.path.dirname(os.path.abspath(__file__))

# API 路由：获取 JSON 文件内容
@app.route('/api/getOrganizationData')
def get_organization_data():
    # 拼接文件路径
    file_path = os.path.join(base_dir, 'assets', 'data', 'organization_time_to_time+1.json')
    
    # 打印路径以调试
    print('文件路径:', file_path)
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取文件并返回 JSON 内容
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        print('文件未找到:', file_path)
        return jsonify({"error": "文件未找到"}), 404

# 启动服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
