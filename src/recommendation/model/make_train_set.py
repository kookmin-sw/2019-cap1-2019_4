## 데이터 불러오는 부분 후에 수정
## main에서 배열로 변경하는 작업

## 생성한 feature를 추가하기 전 기본 train_set

'''
make_train_set 
@ orders_df, train_df, product_df 에서 필요한 것들만 뽑아 merge
@ 중간에 필요없는 것들은 삭제
'''

def make_train_set():
    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id","order_dow","order_hour_of_day"])
    train_df = pd.read_csv("order_products__train.csv", usecols=["order_id"])
    
    # ------------------ train id에 맞는 유저를 찾은 뒤 그 유저가 최근에 샀던 상품 확인 
    
    # order_id 중복 제거 >> 갯수 세는 것 같지만 중복 제거였음
    train_df= train_df.groupby("order_id").aggregate("count").reset_index()
    
    # order_id에 맞는 user_id를 찾아서 merge
    train_df = pd.merge(train_df, orders_df, how="inner", on="order_id")
    
    # prior과 merge
    # 유저와 order_id 에 맞는 상품 목록
    train_df = pd.merge(train_df, latest_order(), how="inner", on="user_id")
    
    # product table에서 id, 소분류, 대분류만 가져와서 merge
    products_df = pd.read_csv( "products.csv", usecols=["product_id", "aisle_id", "department_id"])
    train_df = pd.merge(train_df, products_df, how="inner", on="product_id")
    
    del products_df, orders_df
    
    return train_df

# 만든 feature merge 하기 >>> 후에 함수 앞에 import 파일명 붙여서 수정해주기,필요한 만큼 피처 merge
# train 과 test의 모양은 같아야 함

def train_result():
    train_x = make_train_set()
    ## train_x = pd.merge(train_x, feature function, how="left", on=["column name"])
    ## ex : train_x = pd.merge(train_x, dep_prob(), how="left", on=["user_id","department_id"])
    
    return train_x

## 배열로 만드는 작업은 main에서
