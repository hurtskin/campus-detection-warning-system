import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib


# 读取表格
file_path = r'label_of_people/学生心理健康风险等级预测_合成数据_4000条.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

weight = np.array([0.027, 0.001, 0.356,0.013,0.013,0.372,0.369,0.006,0.380,0.212,0.337,0.376,0.013])

# 提取特征（前13列）和标签（第14列）
features = df.iloc[:, :13].values
labels = df.iloc[:, 13].values

# 定义结构化数据类型
feature_names = df.columns[:13].tolist()
dtype = [(name, 'f8') for name in feature_names] + [('label', 'i4')]

# 创建结构化 Numpy 数组，将特征和标签结合
structured_array = np.zeros(features.shape[0], dtype=dtype)
for i, name in enumerate(feature_names):
    structured_array[name] = features[:, i]
structured_array['label'] = labels

X = df.iloc[:, :13]
y = df.iloc[:, 13]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
sample_weight = np.dot(X_train, weight)

mp_model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)
svm_model = SVC()
nb_model = GaussianNB(var_smoothing=1e-9)
dt_model = DecisionTreeClassifier(max_features=0.1,random_state=42)
xgb_model = XGBClassifier(eval_metric='logloss', random_state=42, learning_rate=0.1, n_estimators=200)

mp_model.fit(X_train, y_train)
svm_model.fit(X_train, y_train,sample_weight=sample_weight)
nb_model.fit(X_train, y_train, sample_weight=sample_weight)
dt_model.fit(X_train, y_train, sample_weight=sample_weight)
xgb_model.fit(X_train, y_train, sample_weight=sample_weight)

# 创建投票分类器
voting_clf = VotingClassifier(
    estimators=[('svm', svm_model),('neural_network', mp_model),('naive_bayes', nb_model), ('decision_tree', dt_model), ('xgboost', xgb_model)],
    voting='hard',
    weights=[5,4,2,1,3]
)

# 训练投票分类器
voting_clf.fit(X_train, y_train)



# 预测并计算准确率
y_pred_ensemble = svm_model.predict(X_test)
svm_model_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

y_pred_ensemble = mp_model.predict(X_test)
mp_model_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

y_pred_ensemble = nb_model.predict(X_test)
nb_model_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

y_pred_ensemble = dt_model.predict(X_test)
dt_model_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

y_pred_ensemble = xgb_model.predict(X_test)
xgb_model_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

y_pred_ensemble = voting_clf.predict(X_test)
voting_ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)

# print("mp:", mp_model_ensemble_accuracy)
# print("svm:", svm_model_ensemble_accuracy)
# print("Naive Bayes Model Accuracy:", nb_model_ensemble_accuracy)
# print("Decision Tree Model Accuracy:", dt_model_ensemble_accuracy)
# print("XGBoost Model Accuracy:", xgb_model_ensemble_accuracy)
# print("Ensemble Model Accuracy:", voting_ensemble_accuracy)
# print(X_test.iloc[:5])

# # 进行预测
# predictions = voting_clf.predict(X)
# df = pd.Series(predictions, name='predictions')
# output_path = '更新后的文件路径.xlsx'
# df.to_excel(output_path, index=False)

# 保存模型
joblib.dump(voting_clf, r'label_of_people\学生心理健康风险等级预测.pkl')
