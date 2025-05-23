import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler

def get_label_of_people():
    # 读取表格
    file_path = r'label_of_people\学生心理健康风险等级预测 .xlsx'
    df = pd.read_excel(file_path, sheet_name='Sheet1',header=1)
    df = df.drop(index=0)
    df = df.reset_index(drop=True)

    # 处理列名的空格问题
    df.columns = df.columns.str.strip()

    # 确认列名正确后，去除“岁”字并转为整数
    df['年龄（17岁-25岁，最后最值归一化为0-1）'] = df['年龄（17岁-25岁，最后最值归一化为0-1）'].apply(lambda x: x.replace('岁', '') if isinstance(x, str) else x)

    # 转换为整数类型
    df['年龄（17岁-25岁，最后最值归一化为0-1）'] = df['年龄（17岁-25岁，最后最值归一化为0-1）'].astype(int)

    # 归一化
    scaler = MinMaxScaler()
    df['年龄（17岁-25岁，最后最值归一化为0-1）'] = scaler.fit_transform(df[['年龄（17岁-25岁，最后最值归一化为0-1）']])


    # 选择需要修改的列（第2、3、4、9、11列），这些列在Python中是0索引的，所以我们选择的是1, 2, 3, 8, 10列
    cols_to_modify = [1, 2, 3, 8, 10]

    # 将"否"改为0，其他改为1
    for col in cols_to_modify:
        df.iloc[:, col] = df.iloc[:, col].apply(lambda x: 0 if x == '否' else 1)


    # 使用 iloc 获取第5列（列索引为4）
    df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: 0.25 if x == '学习状态极差，学习压力令人窒息' else
                                        0.50 if x == '学习状态较差、压力较大' else
                                        0.75 if x == '学习状态一般、有学习压力' else
                                        1.00 if x == '学习状态较好、无压力' else x)


    # 使用 iloc 获取第6列（列索引为5）
    df.iloc[:, 5] = df.iloc[:, 5].apply(lambda x: 0.20 if x == '没有' else
                                        0.40 if x == '轻度' else
                                        0.60 if x == '中度' else
                                        0.80 if x == '重度' else
                                        1.00 if x == '极重' else x)


    # 使用 iloc 获取第7列（列索引为6）
    df.iloc[:, 6] = df.iloc[:, 6].apply(lambda x: 0.25 if x == '一直平稳' else
                                        0.50 if x == '偶尔波动，但是本人能够控制' else
                                        0.75 if x == '波动较大，本人无法控制' else
                                        1.00 if x == '情绪崩溃' else x)


    # 使用 iloc 获取第8列（列索引为7）
    df.iloc[:, 7] = df.iloc[:, 7].apply(lambda x: 0.20 if x == '几乎没有' else
                                        0.40 if x == '较少' else
                                        0.60 if x == '一般' else
                                        0.80 if x == '比较多' else
                                        1.00 if x == '非常多' else x)


    # 将第10列（列索引为9）和第12列（列索引为11）的所有值设为0
    df.iloc[:, 9] = 0  
    df.iloc[:, 11] = 0  


    # 使用 iloc 获取第13列（列索引为12）并用 switch 语句处理
    df.iloc[:, 12] = df.iloc[:, 12].apply(lambda x: 0 if x == '无需帮助' else
                                        1.00 if x == '偶尔需要帮助' else x)


    # 使用 iloc 获取第14列（列索引为13）并进行替换
    df.iloc[:, 13] = df.iloc[:, 13].apply(lambda x: 0 if pd.isna(x) or x in ['无', '否'] else 1.00)
    df.rename(columns={
        '近六个月以来，您的及家人身体健康状况是否有异常（1有，0没有）': '近六个月以来，您的及家人身体健康状况1否有异常（1有，0没有）'
    }, inplace=True)

    df['过去一月学习顺利程度（取值0-1，精确到小数点2位，值越大越顺利）'] = scaler.fit_transform(df[['过去一月学习顺利程度（取值0-1，精确到小数点2位，值越大越顺利）']])
    df['目前有没有考试、就业、升学压力（取值0-1，精确到小数点2位，值越大压力程度越高）'] = scaler.fit_transform(df[['目前有没有考试、就业、升学压力（取值0-1，精确到小数点2位，值越大压力程度越高）']])
    df['过去一月情绪波动次数（取值最后最值归一化为0-1）'] = scaler.fit_transform(df[['过去一月情绪波动次数（取值最后最值归一化为0-1）']])
    df['从家人、朋友、老师得到的帮助和支持程度（取值0-1，精确到小数点2位，值越大支持程度越高）'] = scaler.fit_transform(df[['从家人、朋友、老师得到的帮助和支持程度（取值0-1，精确到小数点2位，值越大支持程度越高）']])
    df['认为自己需要心理帮助的程度（取值0-1，精确到小数点2位）'] = scaler.fit_transform(df[['认为自己需要心理帮助的程度（取值0-1，精确到小数点2位）']])
    df['本人在日常的生活、学习，人际交往方面上是否存在困难（取值0-1，精确到小数点2位，值越大越困难）'] = scaler.fit_transform(df[['本人在日常的生活、学习，人际交往方面上是否存在困难（取值0-1，精确到小数点2位，值越大越困难）']])

    # 选择前14列作为特征
    X = df.iloc[:, :14]  
    X = X.drop(columns=["针对18题，受影响程度"])

    # 转换所有非数值列为数值型数据，确保能适应机器学习模型
    X = X.apply(pd.to_numeric, errors='coerce')  

    # 处理NaN值：你可以选择填充NaN值或删除包含NaN的行
    X = X.fillna(0) 

    model = joblib.load(r'label_of_people\学生心理健康风险等级预测.pkl')


    # 将预测结果写回数据框的第15列
    df['预测标签'] = model.predict(X)  
    df = df.astype(float).round(2)

    label_dict = {
        '学习程度': [],
        '考试压力': [],
        '情绪波动': [],
        '帮助支持': [],
        '心理帮助': [],
        '日常困难': [],
        '预测标签': []
    }

    # 将每行数据添加到相应的列表中
    for i in range(len(df)):
        label_dict['学习程度'].append(df['过去一月学习顺利程度（取值0-1，精确到小数点2位，值越大越顺利）'][i])
        label_dict['考试压力'].append(df['目前有没有考试、就业、升学压力（取值0-1，精确到小数点2位，值越大压力程度越高）'][i])
        label_dict['情绪波动'].append(df['过去一月情绪波动次数（取值最后最值归一化为0-1）'][i])
        label_dict['帮助支持'].append(df['从家人、朋友、老师得到的帮助和支持程度（取值0-1，精确到小数点2位，值越大支持程度越高）'][i])
        label_dict['心理帮助'].append(df['认为自己需要心理帮助的程度（取值0-1，精确到小数点2位）'][i])
        label_dict['日常困难'].append(df['本人在日常的生活、学习，人际交往方面上是否存在困难（取值0-1，精确到小数点2位，值越大越困难）'][i])
        label_dict['预测标签'].append(df['预测标签'][i])


    return label_dict

def get_len():
    file_path = r'label_of_people\学生心理健康风险等级预测.xlsx'
    df = pd.read_excel(file_path, sheet_name='Sheet1',header=1)
    return len(df)