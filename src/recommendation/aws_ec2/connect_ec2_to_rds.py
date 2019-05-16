import MySQLdb
import pandas as pd

db = MySQLdb.connect(host="[RDS endpoint]",# host
                     user="[master user]",         # username
                     passwd="[master user passwd]",  # password
                     db="[RDS name]")   # RDS database name     

# cur = db.cursor()
# cur.execute("SELECT * FROM aisles")

# 데이터 접근 가능한지 확인해보는 방법
print("print all records to check DB is connected") 
data = pd.read_sql('select * from aisles', con=db)
print(data)
