# 유저가 최근에 구매한 상품이 몇번 재구매 됐고, 구매 됐었는지, 그리고 지금 재구매가 된 것인지


def latest_order():
    orders_df = pd.read_csv("orders.csv", usecols=["order_id","user_id","order_number"])
    prior_df = pd.read_csv("order_products__prior.csv")
    
    # merge
    prior_df = pd.merge(prior_df, orders_df, how="inner", on="order_id")
    
    # 최근 구매한 기록 - 제일 큰 order_id 찾고, 최근 구매한 상품 목록 찾기
    prior_grouped_df = prior_df.groupby("user_id")["order_number"].aggregate("max").reset_index()
    prior_df_latest = pd.merge(prior_df, prior_grouped_df, how="inner", on=["user_id", "order_number"])
    
    # 칼럼 이름 변경 reordered >> reordered_latest
    prior_df_latest = prior_df_latest[["user_id", "product_id", "reordered"]]
    prior_df_latest.columns = ["user_id", "product_id", "reordered_latest"]
    
    # 유저가 구매한 상품들이 몇번 구매됐고 재구매는 몇번 되었는지 
    prior_df = prior_df.groupby(["user_id","product_id"])["reordered"].aggregate(["count", "sum"]).reset_index()

    # 칼럼명 바꾸기!
    prior_df.columns = ["user_id", "product_id", "reordered_count", "reordered_sum"]
    
    # merge prior_df & latest df 
    latest_order = pd.merge(prior_df, prior_df_latest, how="left", on=["user_id","product_id"])
    
    # 유저 아이디로 나중에 머지 할 것임!!
    return latest_order
