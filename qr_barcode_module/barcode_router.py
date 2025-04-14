import json
import pymysql, pymysql.cursors
from qr_barcode_module.db import get_db_connection
from qr_barcode_module.food_utils import get_food_detail_by_id
from qr_barcode_module.error_messages import no_food_error_message, server_error_message

def get_product_by_barcode(data, user_email):
    try:
        data_code = data.get('value')
        db_connect = get_db_connection()
        # DictCursor로 결과의 값을 key(column)로 가져옴 -> 인덱스보다 명확히 알 수 있음음
        cursor = db_connect.cursor(pymysql.cursors.DictCursor)

        # 바코드의 값으로 맞는 food_id가 존재하는지 확인
        cursor.execute("SELECT food_id FROM barcodes WHERE code = %s", (data_code,))
        result = cursor.fetchone()
        if not result:
            return json.dumps(no_food_error_message, ensure_ascii=False)
        
        # 쿼리로 얻은 food_id로 food 정보를 가져옴
        food_id = result['food_id']
        product_data = get_food_detail_by_id(cursor, food_id, user_email)

        # json으로 반환환
        return json.dumps({"products" : [product_data]}, ensure_ascii=False)

    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)