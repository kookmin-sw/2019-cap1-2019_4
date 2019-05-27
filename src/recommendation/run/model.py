# coding: utf-8

import pymysql
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import csv
import xgboost as xgb
from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree


## CREATE MODEL
def runXGB(train_X, train_y, test_X, test_y=None, feature_names=None, seed_val=0):

        # xgboost 모델을 만들기 위한 param 집합
        params = {}
        params["objective"] = "binary:logistic"
        params['eval_metric'] = 'logloss'
        params["eta"] = 0.05
        params["subsample"] = 0.7
        params["min_child_weight"] = 10
        params["colsample_bytree"] = 0.7
        ## 제일 정확성이 높은 feature 조합과 트리 깊이가 5일 때 더 정확한 값이 나오는 것을 알았음
        params["max_depth"] = 5
        params["silent"] = 1
        params["seed"] = seed_val
        params["nthread"] = 16

        # round 값 설정
        num_rounds = 100

        plst = list(params.items())
        xgtrain = xgb.DMatrix(train_X, label=train_y)

        # test에대한 답이 존재할 때 label설정
        if test_y is not None:
                xgtest = xgb.DMatrix(test_X, label=test_y)
                watchlist = [ (xgtrain,'train'), (xgtest, 'test') ]
                model = xgb.train(plst, xgtrain, num_rounds, watchlist, early_stopping_rounds=50, verbose_eval=10)

        else:
                xgtest = xgb.DMatrix(test_X)
                model = xgb.train(plst, xgtrain, num_rounds)

        # 모델 생성 후 예측값 찾아내기!
        pred_test_y = model.predict(xgtest)
        return pred_test_y
