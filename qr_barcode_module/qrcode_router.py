#qr코드 처리 모듈
import json
import pymysql
from qr_barcode_module.db import get_db_connection
from qr_barcode_module.food_utils import get_food_detail_by_id
from qr_barcode_module.error_messages import no_food_error_message, server_error_message

def get_product_by_qrcode(input_json_data, user_email):
    try:
        data = json.loads(input_json_data)
        data_code = data.get('value')
        db_connect = get_db_connection()

        cursor = db_connect.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM qr_links WHERE code = %s", (data_code,))
        result = cursor.fetchone()

        if not result:
            return json.dumps(no_food_error_message, ensure_ascii=False)
        
        qr_type = result["type"]
        if qr_type == "food":
            food_id = result["food_id"]
            product_data = get_food_detail_by_id(cursor, food_id, user_email)
            return json.dumps({"products" : [product_data]}, ensure_ascii=False)
        elif qr_type == "bundle":
            """구성 상품만"""
            bundle_id = result["bundle_id"]
            cursor.execute("SELECT food_id FROM food_bundle_items WHERE bundle_id = %s", (bundle_id,))
            food_ids = cursor.fetchall()['food_id']
            products = []
            for food_id in food_ids:
                product_data = get_food_detail_by_id(cursor, food_id, user_email)
                products.append(product_data)
            return json.dumps({"products" : products}, ensure_ascii=False)
        else:
            #/supplier/{supplier_id}로 라우팅 할 수 있도록 하기기
            supplier_id = result["supplier_id"]
            return
    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)