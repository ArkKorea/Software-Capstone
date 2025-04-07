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