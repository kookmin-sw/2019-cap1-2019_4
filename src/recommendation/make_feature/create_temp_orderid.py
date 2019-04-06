## order_id와 user_id dataframe 생성

#order_id와 user_id가 매칭되는 column 2개짜리 table을 생성하는 것 : 예측을 위함
#prior가 기준, order_id 공통으로 orders_df와 merge
#위에서 merge된 table이 기준, product_id 공통으로 product와 merge

import time
import numpy as np
import pandas as pd

orders_df = pd.read_csv("orders.csv")

'''
model에 넣고 추천 상품을 예측하기 위한 임시 order_id를 만드는 함수
output : 임시 order_id와 user_id가 짝지어진 table
'''

def make_tmp_orderid():
    # user_id만 중복없이 뽑아내기
    user = orders_df['user_id'].unique()
    user = map(str, user)
    #len(user)

    # order_id를 위해 현재 시간 구하기
    now = time.strftime('%y%m%d', time.localtime(time.time()))
    #now

    # table을 채우기 위해 user수만큼 시간 개수도 늘리기 and user_id 붙이기
    order_id = ([now]*len(user))
    id_ = list(map(lambda x, y : x+y, order_id, user))

    tmp_orderid = pd.DataFrame({"order_id": id_, "user_id": user})
    return tmp_orderid

    del user, id_, now

make_tmp_orderid()
