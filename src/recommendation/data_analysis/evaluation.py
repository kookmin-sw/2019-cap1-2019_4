import numpy as np 
import pandas as pd 
import csv

# read data
orders = pd.read_csv("../capstone_data/orders.csv")
train = pd.read_csv("../capstone_data/order_products__train.csv")
# sample submission file named 'submission"
submission = pd.read_csv("../capstone_data/sample_submission.csv")
# select orders included in train set
train_orders = orders.loc[orders['eval_set'] == 'train']


print("the number of train_orders : "  + str(train_orders.shape[0]))
#print(train.head())
#print(train.order_id.unique())
# show format of submission using a sample
print (submission.head())


### workflow
# input : read_csv 
# 1. train에 있는 order갯수만큼 반복문을 돌려야하고 (131209개)
# 2. 그 order에 해당하는 제품을 train에서 set으로 뽑아내야겠지-> 정답 set
# 3. 그 order에 해당하는 제품을 submission에서도 뽑아내야함
# 4. 몇개 맞았는지 저장할 list도 필요하겠다(order_id별로 f1-score계산 용)
# 5. 추천을 아예 못한 order 에 대해서는 0을 추가하고, 아니면 precision이랑 recall 구하기 


"""evaluate
compute f1_score
@input params : submission file using read_csv
@output       : mean f1-score
"""
def evaluate(submission):
    question_order_id = train.order_id.unique() # uniuqe order_id in train
    f1_scores = [] # keep f1_score per order_id
    for order in question_order_id:
        answer  = set(train.loc[train['order_id'] == order]['product_id'].tolist()) # the answer products in given order_id
        if(order in submission.order_id.unique()):
            predict = submission.loc[submission['order_id'] == order]['products']
            predict = set(map(int, predict.values[0].split(' '))) # the predicted products in given orders
            tp = float(len(answer.intersection(predict))) #true positive
            precision = tp / len(predict)
            recall    = tp / len(answer)
            f1_score  = 2 * (precision * recall / (precision + recall))
            f1_scores.append(f1_score)
        else:
            f1_scores.append(0)
            
    return sum(f1_scores)/len(f1_scores)
    
        
        
"""the simplest evaluate function 
@input params : answer list, predict list
@tn, fp, fn, tp : true negative, false positive, false negative, true positive
"""
def simple_evaluate(answer, predict):
    tn, fp, fn, tp = confusion_matrix(answer, predict).ravel()
    print(tp)
    print(fp)
    print(float(tp)/(tp + fp))
