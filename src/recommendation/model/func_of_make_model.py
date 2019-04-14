# 모델 생성 후 예측값까지 반환하는 함수

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import metrics, model_selection


'''
train_x : 모델 생성을 위한 trian데이터
train_y : 모델 생성을 위한 train데이터의 binary 분류 값
text_x : 모델 생성 후 예측을 위한 test 데이터
'''
def make_XGB(train_X, train_y, test_X, test_y=None, feature_names=None, seed_val=0):

        # xgboost 모델을 만들기 위한 param 집합 > 필요에따라 수정 가능
        params = {}
        params["objective"] = "binary:logistic"
        params['eval_metric'] = 'logloss'
        params["eta"] = 0.05
        params["subsample"] = 0.7
        params["min_child_weight"] = 10
        params["colsample_bytree"] = 0.7
        params["max_depth"] = 8
        params["silent"] = 1
        params["seed"] = seed_val

        # round 값 설정
        num_rounds = 100
        
        # train()의 파라미터로 넣기위한 데이터 변형
        plst = list(params.items())
        xgtrain = xgb.DMatrix(train_X, label=train_y)

        # test에대한 답이 존재할 때 label설정, 모델 생성
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
