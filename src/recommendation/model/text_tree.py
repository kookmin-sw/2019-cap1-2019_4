import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import csv
import pickle
import xgboost as xgb
from numpy import loadtxt
from xgboost import XGBClassifier
from xgboost import plot_importance
from xgboost import plot_tree
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
import csv
import pandas as pd

# 학습 데이터와 그의 분류값은 지정해줘야함 
model = XGBClassifier()
model.fit(train_x, train_y)

# display text tree 
model.get_booster().dump_model('xgb_model.txt', with_stats=True)
# read the contents of the file
with open('xgb_model.txt', 'r') as f:
    txt_model = f.read()
print(txt_model)
