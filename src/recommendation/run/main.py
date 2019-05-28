# coding: utf-8
'''
EC2 환경에서 실행하는 main
''' 
import random
import pymysql
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import xgboost as xgb
from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree

# 필요한 파일 import 
import feature
import dataset
import model


###################### DB connect
db = pymysql.connect(host="", port=3306, user="", passwd="",db="")


print("start")
train_x = dataset.train_result()
# train과 test 확인을 위해
print(train_x.columns)


## 여기 make_answer에 파라미터로 train_x 보내는 것을 바뀜
train_y = dataset.make_answer(train_x)
print("train_y 확인 \n")
print(train_y)


## test set
test = dataset.test_result()
# train과 test 확인을 위해
print(test.columns)


### submission form
out_df=test[["order_id", "product_id","user_id"]]


### 최종 data set --> array로 바꾸기
train_x = np.array(train_x.drop(["order_id", "user_id", "product_id","aisle_id","department_id"], axis=1))
test = test.drop(["order_id", "user_id", "product_id","aisle_id","department_id"], axis=1)
#test.to_csv("test.csv", index=False)
test = np.array(test)


# xgboost : 모델을 생성하기위한 데이터, 답, 모델 생성후 예측할 데이터 -> 20분 정도 걸림
pred = model.runXGB(train_x, train_y, test)
print("Prediction fin.")


#### 모델 예측값 따로 저장
temp = pred

## 모델 뎁스가 같더라도 cutoff에 따라 값이 바뀜
cutoff = temp.mean() - 0.02
temp[temp>=cutoff] = 1
temp[temp<cutoff] = 0

# 주문 번호랑 상품 번호에 맞춰서 칼럼 추가
out_df["Pred"] = temp
out_df.head()


# 재구매한다고 결과가 나온 것만 뽑아내기!
out_df = out_df.ix[out_df["Pred"].astype('int')==1]

# 중복 제거
out_df = out_df.drop_duplicates()

### 살 확률이 높은 상품만 선택
def merge_products(x):
    return " ".join(list(x.astype('str')))


############### 캐글 제출용
kaggle = out_df.groupby("order_id")["product_id"].aggregate(merge_products).reset_index()
kaggle.columns = ["order_id", "products"]


SQL = "SELECT order_id FROM submission"
sub_df = pd.read_sql(SQL, db)
sub_df = pd.merge(sub_df, kaggle, how="left", on="order_id")
sub_df["products"].fillna("None", inplace=True)
sub_df.to_csv("kaggle_n.csv", index=False)

del SQL

# 주문 번호 - 상품 한 개
product = list(map(lambda x: random.choice(x.split()) , sub_df['products']))

sub_df['products'] = product
sub_df.head()

# 저장
sub_df["products"].fillna("None", inplace=True)
sub_df.to_csv("kaggle_1.csv", index=False)
del sub_df

print("kaggle data finish")

############### user 기준 : 회원과 상품 여러개
result = out_df.groupby("user_id")["product_id"].aggregate(merge_products).reset_index()
result.to_csv("user_ncsv", index=False)

# 회원당 추천 상품 여러개 > 하나만 뽑는 과정
product = list(map(lambda x: random.choice(x.split()) , result['product_id']))
result['product_id'] = map(int, product)


# 테스트용으로 사람 30명만 선택
#user_list = random.sample(result["user_id"], 30)
#print("user list")
#print(user_list)


# 회원 - 상품 1개 저장
result["product_id"].fillna(0, inplace=True)
result.to_csv("user_1.csv", index=False)

#print("finish")
