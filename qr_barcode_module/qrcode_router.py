#qr코드 처리 모듈
import json
from qr_barcode_module.error_messages import no_food_error_message, server_error_message

def get_product_by_qrcode(input_json_data, user_email):
    try:
        data = json.loads(input_json_data)
    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)