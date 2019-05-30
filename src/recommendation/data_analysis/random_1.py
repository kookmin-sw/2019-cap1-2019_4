# 데모를 위한 것
import numpy as np
import pandas as pd
import random
import csv


def random_table(df, n):
    return df.ix[random.sample(df.index, n)]

# 오픈 할 파일은 최종 결과를 담은 것
df = pd.read_csv("")

#`select random 100
result = random_table(df, 100)

result.to_csv("random.csv", index=False)
