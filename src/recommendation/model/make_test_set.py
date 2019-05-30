## 테스트 셋 기본 

def make_test_set():
    test_df = pd.read_csv("sample_submission.csv", usecols=["order_id"])
    
    # order_id에 맞는 user_id를 찾아서 merge
    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id", "order_dow", "order_hour_of_day"])
    test_df = pd.merge(test_df, orders_df, how="inner", on="order_id")
    
    del orders_df
    
    # prior과 merge
    # 유저와 order_id 에 맞는 상품 목록
    test_df = pd.merge(test_df, latest_order(), how="inner", on="user_id")
    
    products_df = pd.read_csv("products.csv", usecols = ["product_id", "aisle_id","department_id"])
    test_df = pd.merge(test_df, products_df, how="inner", on="product_id")
    
    del products_df

    #### 밑부분 원래 제거!
    test_df = test_df.drop(["reordered_count","reordered_sum","reordered_latest"], axis = 1)
    return test_df
    
# 만든 feature merge 하기 >>> 후에 함수 앞에 import 파일명 붙여서 수정해주기,필요한 만큼 피처 merge
# train 과 test의 모양은 같아야 함

def test_result():
    test_x = make_train_set()
    ## test_x = pd.merge(test_x, feature function, how="left", on=["column name"])
    ## ex : test_x = pd.merge(test_x, dep_prob(), how="left", on=["user_id","department_id"])
    
    return test_x
