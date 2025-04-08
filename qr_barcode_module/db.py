#qr과 바코드 처리를 위한 DB 설정
import pymysql

# .env에 맞게 수정할 것
def get_db_connection():
    return pymysql.connect(
        host='allertsign-data.c9eywawiwtlh.ap-northeast-2.rds.amazonaws.com',
        user='root',
        password='Capstone2025!',
        database='test',
        charset='utf8',        
        )


## 아래는 env용
##import os
##from dotenv import load_dotenv
##
##load_dotenv()
##
##def get_db_connection():
##    return pymysql.connect(
##        host=os.getenv('DB_HOST'),
##        user=os.getenv('DB_USER'),
##        password=os.getenv('DB_PASSWORD'),
##        database=os.getenv('DB_NAME'),
##        charset='utf8',
##    )