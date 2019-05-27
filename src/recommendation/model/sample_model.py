# 모델이 잘 만들어 지는지 확인하기 위한 테스트 코드

from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
import csv
import pandas as pd
#------------------------------------------이거 다시 수정하기!!!ㅠㅠtest 부분
# data
db = pymysql.connect(host="", port= , user="",passwd ="", db="")

SQL = "SELECT * FROM orders"
orders_df = pd.read_sql(SQL, db)
del SQL

SQL = "SELECT * FROM order_products__train"
train = pd.read_sql(SQL, db)
del SQL

SQL "SELECT * FROM sample_submission"
test = pd.read_sql(SQL, db)
del SQL


# 필요한 데이터 merge, 샘플 코드이므로 500개 데이터만 사용
# feature 추가 또는 가공된 데이터 없이 기존 데이터를 그대로 사용(sample code)
DATA = pd.merge(train, orders_df, how='inner', on=['user_id'])
DATA_answer = pd.DataFrame(DATA['reordered'])[:500]
DATA_data = DATA.drop(['reordered','product_name','eval_set','add_to_cart_order'], axis=1, errors="ignore")[:500]


#### 모델 생성 ####
model = XGBClassifier()
model.fit(DATA_data, DATA_answer)


#### boosting 트리 확인 ####
plot_tree(model)

fig = pyplot.gcf()
fig.set_size_inches(20,20)
pyplot.show()


#### 어떤 feature가 중요한지 확인 ####
plot_importance(model)
pyplot.show()


#### 예측할 test 데이터 ####
test_ = pd.merge(test, orders_df, how='inner', on=['order_id'])
test_answer = pd.DataFrame(test_['reordered'])[:500]
test_data = test_.drop(['reordered','product_name','eval_set','add_to_cart_order'], axis=1, errors="ignore")[:500]


#### 예측한 값이랑 정답이랑 정확성 확인 ####
pred = model.predict(train_data)
predictions =[ round(value) for value in pred]
accuracy = accuracy_score(train_answer, pred)
print("%.2f%%" %(accuracy*100.0))
