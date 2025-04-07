#qr 혹은 바코드 처리 진입점
import json
from qr_barcode_module.barcode_router import get_product_by_barcode
from qr_barcode_module.qrcode_router import get_product_by_qrcode

no_food_error_message = {"error": "해당 코드는 등록된 상품이 없습니다", "code" : "PRODUCT_NOT_FOUND"}
type_error_message = {"error": "유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.", "code" : "INVALID_CODE_TYPE"}
server_error_message = {"error": "서버 오류입니다. 잠시 후 다시 시도해주세요.", "code" : "INTERNAL_SERVER_ERROR"}

def get_product_by_code(input_json_data, user_email):
    try:
        data = json.loads(input_json_data)
        data_type = data.get('type')
        
        if data_type == 'barcode':
            return get_product_by_barcode(data, user_email)
        elif data_type == 'qrcode':
            return get_product_by_qrcode(data, user_email)
        else:
            return json.dumps(type_error_message, ensure_ascii=False)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return json.dumps(server_error_message, ensure_ascii=False)