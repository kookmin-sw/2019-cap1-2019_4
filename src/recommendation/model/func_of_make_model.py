# 모델 생성 후 예측값까지 반환하는 함수

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import metrics, model_selection


'''
train_x : 모델 생성을 위한 trian데이터
train_y : 모델 생성을 위한 train데이터의 binary 분류 값
text_x : 모델 생성 후 예측을 위한 test 데이터

*parameter
objective : reg,binary,multi 등으로 정의 가능, 이 코드에서는 binary분류를 할 것
eval_metric : 모델의 평가 함수 정의
eta : learning rate, 단계별 가중치를 줄여서 강한 모델을 제작 일반적으로 0.01~0.2
subsample : 각 트리마다의 관측 데이터 샘플링 비율. 일반적으로 0.5~1.0
min_child_weight : overfitting을 컨트롤, child의최소 가중치의 합
colsampe_bytree : feature 샘플링 비율, 일반적으로 0.5~1.0
max_depth : 트리의 최대 깊이를 정의, 일반적으로는 3~10
silent : 동작 메세지를 출력하려면 0, 출력을 원하지 않으면 1
seed : 난수 생성 seed
'''
def make_XGB(train_X, train_y, test_X, test_y=None, feature_names=None, seed_val=0):

        # xgboost 모델을 만들기 위한 param 집합 > 직접 지정!
        params = {}
        params["objective"] = "binary:logistic"
        params['eval_metric'] = 
        params["eta"] = 
        params["subsample"] =
        params["min_child_weight"] = 
        params["colsample_bytree"] = 
        params["max_depth"] = 
        params["silent"] = 
        params["seed"] = 

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
                
                #### EC2에서는 환경 설정이 필요함 ####
                xgb.plot_tree(model)
                fig = pyplot.gcf()
                fig.set_size_inches(30, 30)
                fig.savefig('tree.png')
                
                pyplot.show()

        else:
                xgtest = xgb.DMatrix(test_X)
                model = xgb.train(plst, xgtrain, num_rounds)

        # 모델 생성 후 예측값 찾아내기!
        pred = model.predict(xgtest)
        return pred
