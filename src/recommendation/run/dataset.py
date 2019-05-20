# coding: utf-8

import pymysql
import numpy as np
import pandas as pd 
import csv
import xgboost as xgb
from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree

# 필요한 다른 python 파일
import feature


###################### DB connect
db = pymysql.connect(host="", port=3306, user="", passwd="",db="")


### train_set - 뼈대
def make_train_set():
    SQL = "SELECT order_id, user_id, order_dow, order_hour_of_day FROM orders"
    orders_df = pd.read_sql(SQL, db)

    SQL = "SELECT order_id FROM order_products__train"
    train_df = pd.read_sql(SQL, db)

    print("make train set - basic start")
    # ------------------ train id에 맞는 유저를 찾은 뒤 그 유저가 최근에 샀던 상품 확인

    # order_id 중복 제거 >> 갯수 세는 것 같지만 중복 제거
    train_df= train_df.groupby("order_id").aggregate("count").reset_index()

    # order_id에 맞는 user_id를 찾아서 merge
    train_df = pd.merge(train_df, orders_df, how="inner", on="order_id")

    # prior과 merge
    # 유저와 order_id 에 맞는 상품 목록
    train_df = pd.merge(train_df, feature.latest_order(), how="inner", on="user_id")

    # product table에서 id, 소분류, 대분류만 가져와서 merge
    # products_df = pd.read_csv( "products.csv", usecols=["product_id", "aisle_id", "department_id"])
    SQL = "SELECT product_id, aisle_id, department_id FROM products"
    products_df = pd.read_sql(SQL, db)

    train_df = pd.merge(train_df, products_df, how="inner", on="product_id")

    del products_df, orders_df, SQL

    print("make train set - basic finish")
    return train_df


'''
새로 만든 feature를 붙이는 부분
만들어진 것은 많지만 제일 정확성이 높은 것만 활용
'''

def train_result():
    train_x = make_train_set()
    train_x = pd.merge(train_x, feature.order_ratio_bychance(), how="left", on = ["user_id, product_id"])
    
    return train_x


### train answer : train_y
def make_answer(train_x):

    SQL = "SELECT order_id, user_id FROM orders"
    orders_df = pd.read_sql(SQL, db)

    SQL = "SELECT order_id, product_id, reordered FROM order_products__train"
    train_df = pd.read_sql(SQL, db)

    print ("train_y start")

    answer = pd.merge(train_df, orders_df, how="inner", on="order_id")
    del orders_df, train_df

    #order_id 제거
    answer = answer[["user_id", "product_id", "reordered"]]

    # train과 그 외 정보를  merge >>>> train_result() 를 train_x로 파라미터 받아올까?
    train_df = pd.merge(train_x, answer, how="left", on=["user_id", "product_id"])

    del answer

    # reordered 값이 nan 인것들은 0으로 변경
    train_df["reordered"].fillna(0, inplace=True)

    train_y = train_df.reordered.values
    print("train_y finish")
    return train_y





### TEST BASIC - test 뼈대
def make_test_set():

    SQL = "SELECT order_id FROM submission"
    test_df = pd.read_sql(SQL, db)

    SQL = "SELECT order_id, user_id, order_dow, order_hour_of_day FROM orders"
    orders_df = pd.read_sql(SQL, db)

    test_df = pd.merge(test_df, orders_df, how="inner", on="order_id")

    del orders_df, SQL

    print("test basic start")

    # prior과 merge
    # 유저와 order_id 에 맞는 상품 목록
    test_df = pd.merge(test_df, feature.latest_order(), how="inner", on="user_id")

    #products_df = pd.read_csv("products.csv", usecols = ["product_id", "aisle_id","department_id"])
    SQL = "SELECT product_id, aisle_id, department_id FROM products"
    products_df = pd.read_sql(SQL, db)

    test_df = pd.merge(test_df, products_df, how="inner", on="product_id")

    del products_df, SQL

    print("test basic finish")
    return test_df


'''
TEST feature merge
train과 같은 갯수의 feature를 가질 수 있도록 맞춰준다.
'''
def test_result():
    test_x = make_test_set()
    test_x = pd.merge(test_x, feature.order_ratio_bychance(), how="left", on = ["user_id, product_id"])
  
    # 확인 print("test fin---")
    return test_x
