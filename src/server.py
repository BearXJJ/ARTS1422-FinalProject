from flask import Flask, request, jsonify
from flask_cors import CORS

import os
from openai import OpenAI
import json
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap.umap_ import UMAP


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

def Dimensionality_Reduction(data_filter):
    _organ = []
    _output = []
    df = pd.read_json("public/organization_time_to2020.json")
    for i, _ in df.iterrows():
        _dict = {'organization_name': _['organization_name']}
        __output = {'organization_name': _['organization_name']}
        _dt = _['data']
        if(data_filter['small_exclude']):
            mx = 0
            for l in range(len(_dt)):
                mx = max(mx, _dt[l]['detail']['total_patent_number'])
            if(mx < 100):
                continue
        for l in range(len(_dt)):
            if(_dt[l]['time'] == data_filter['start_year']):
                __output['total_patent_number'] = _dt[l]['detail']['total_patent_number']
                __output['A'] = int(_dt[l]['detail']['CPC_ratio']['A'] * 100)
                __output['B'] = int(_dt[l]['detail']['CPC_ratio']['B'] * 100)
                __output['E'] = int(_dt[l]['detail']['CPC_ratio']['E'] * 100)
                __output['F'] = int(_dt[l]['detail']['CPC_ratio']['F'] * 100)
                __output['G'] = int(_dt[l]['detail']['CPC_ratio']['G'] * 100)
                __output['H'] = int(_dt[l]['detail']['CPC_ratio']['H'] * 100)
                __output['Y'] = int(_dt[l]['detail']['CPC_ratio']['Y'] * 100)
                if(data_filter['gender_ratio'] == 1):
                    _dict['gender_ratio'] = _dt[l]['detail']['gender_ratio']
                if(data_filter['total_patent'] == 1):
                    _dict['total_patent_number'] = _dt[l]['detail']['total_patent_number']
                if(data_filter['cited_per_people'] == 1):
                    _dict['cited_per_people'] = _dt[l]['detail']['cited_per_people']
                if(data_filter['emerging'] == 1):
                    _dict['emerging'] = int(_dt[l]['detail']['emerging'][:4])
                if(data_filter['cpc_ratio'] == 1):
                    _dict['A'] = int(_dt[l]['detail']['CPC_ratio']['A'] * 100)
                    _dict['B'] = int(_dt[l]['detail']['CPC_ratio']['B'] * 100)
                    _dict['E'] = int(_dt[l]['detail']['CPC_ratio']['E'] * 100)
                    _dict['F'] = int(_dt[l]['detail']['CPC_ratio']['F'] * 100)
                    _dict['G'] = int(_dt[l]['detail']['CPC_ratio']['G'] * 100)
                    _dict['H'] = int(_dt[l]['detail']['CPC_ratio']['H'] * 100)
                    _dict['Y'] = int(_dt[l]['detail']['CPC_ratio']['Y'] * 100)
                if(data_filter['total_cited'] == 1):
                    _dict['total_cited_number'] = _dt[l]['detail']['total_cited_number']
                if(data_filter['cited_average'] == 1):
                    _dict['average_cited'] = _dt[l]['detail']['average_cited']
                if(data_filter['inventor_count'] == 1):
                    _dict['inventor_count'] = _dt[l]['detail']['inventor_count']
            else:
                continue
        _organ.append(_dict)
        _output.append(__output)
    res = pd.DataFrame(_organ)
    res = res.dropna().reset_index(drop = True)
    res_new = res.drop(columns = ['organization_name'])
    
    # for col in res_new.columns:
    #     minv = res_new [col].min()
    #     maxv = res_new [col].max()
    #     res_new[col] = (res_new [col] - minv) / (maxv - minv)
    
    if(data_filter['reduction_method'] =='t-SNE'):
        tsne = TSNE(n_components = 2)  
        res_x = tsne.fit_transform(res_new)
        
    if(data_filter['reduction_method'] == 'PCA'):    
        pca = PCA(n_components = 2)
        res_x = pca.fit_transform(res_new)

    if(data_filter['reduction_method'] == 'UMAP'):    
        umap_model = UMAP(n_components = 2)  
        res_x = umap_model.fit_transform(res_new)

    res_x = pd.DataFrame(res_x)
    res_x['organization_name'] = res['organization_name']
    res_x.rename(columns = {0: 'x', 1: 'y'}, inplace = True)
    res_x.to_csv("public/now.csv", index = False)
    # res_json = []
    
    # for i, _ in res_x.iterrows():
    #     cur_json = {"organization": _['organization_name'], "x": _[0], "y": _[1]}
    #     res_json.append(cur_json)
    
    return _output

def process_statement_text(statement):

    client = OpenAI(
        base_url='https://xiaoai.plus/v1',
        api_key='sk-FpEx54u6YVmMVuVm7QCXfVaqETEC5NZperrGUaC5FLtrX5FH'
    )

    df = pd.read_csv('public/update.csv')
    org = df['organization_name'].to_list() 

    Prompt_text = f'''
        You are an expert in advising some fresh people to find a job in a company and apply for a patent.
        Here I have a list containing all the companies that you can choose and can only choose from! {org}
        You can only choose companies in this list \[ very important!!! \]. 
        Remember not to change the name of any company. \[ very important!!! \].
        Remember to check whether you have recommended some companies outside of the list.
        
        And here is my requirements for my future job. {statement} 
        Please give me some advise.
        
        Remember to answer this question in the following format and you'better advise twenty companies instead of just one. Here is an example.
        1. salesforce.com, inc.
        Reason: The reason why I suggest you is that xx
        
        3. iRobot Corporation
        Reason: The reason why I suggest you is that xx
        
        5. Zynga Inc.
        Reason: The reason why I suggest you is that xx
        
        Please do NOT add anything also besides my format!
        You can only choose companies in the list \[ very important!!! \]. 
        Remember not to change the name of any company. \[ very important!!! \].
        Remember to check whether you have recommended some companies outside of the list. 
        Remember not to change the name of any company.
        Don't add some '*' marks in your answer.
    '''

    completion = client.chat.completions.create(
        model = "gpt-4-32k",
        messages = [{
            'role': 'user',
            'content': Prompt_text
        }]
    )

    res = completion.choices[0].message.content
    for txt in res:
        print(txt, end = '')
    res = res.split('\n')

    lst = []
    str_company = ""

    for x in range(20):
        if(x * 3 + 1 > len(res)):
            break
        if(res[x * 3][3:] in org):
            lst.append(res[x * 3][3:])
            str_company += res[x * 3][3:]
            str_company += res[x * 3 + 1][3:] + '\n'
    if(len(lst) == 0):
        lst.append('International Business Machines Corporation')
        str_company += 'International Business Machines Corporation'
        str_company += 'Reason: The reason why I suggest you is that it is big company that can give you more chance.'

    return str_company, lst

@app.route('/run-filter', methods=['GET', 'POST'])
def run_filter():
    data = request.json
    result = Dimensionality_Reduction(data)
    return jsonify({"success": True, "data": result})

@app.route('/process-statement', methods=['GET', 'POST'])
def process_statement():
    data = request.json
    statement_text = data.get('statementText')
    print(f"Received statementText via POST: {statement_text}")
    result, lst = process_statement_text(statement_text)
    return jsonify({"success": True, "processedText": result, "processList": lst})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
