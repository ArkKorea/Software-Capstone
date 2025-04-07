import json
import pymysql
from qr_barcode_module.db import get_db_connection
from qr_barcode_module.food_utils import get_food_detail_by_id

no_food_error_message = {"error": "해당 코드는 등록된 상품이 없습니다", "code": "PRODUCT_NOT_FOUND"}
server_error_message = {"error": "서버 오류입니다. 잠시 후 다시 시도해주세요.", "code": "INTERNAL_SERVER_ERROR"}

def get_product_by_barcode(data, user_email):
    try:
        data_code = data.get('value')
        db_connect = get_db_connection()
        cursor = db_connect.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT food_id FROM barcodes WHERE code = %s", (data_code,))
        result = cursor.fetchone()
        if not result:
            return json.dumps(no_food_error_message, ensure_ascii=False)
        
        food_id = result['food_id']
        product_data = get_food_detail_by_id(cursor, food_id, user_email)

        return json.dumps({"products" : [product_data]}, ensure_ascii=False)

    except Exception as e:
        print(f"Error occurred: {e}")
        return json.dumps(server_error_message, ensure_ascii=False)