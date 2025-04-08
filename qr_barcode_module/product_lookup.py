#qr 혹은 바코드 처리 진입점
import json
from qr_barcode_module.barcode_router import get_product_by_barcode
from qr_barcode_module.qrcode_router import get_product_by_qrcode
from qr_barcode_module.error_messages import type_error_message, server_error_message


def get_product_by_code(input_json_data, user_email):
    try:
        # JSON 데이터 파싱해 입력 코드의 종류 판별
        data = json.loads(input_json_data)
        data_type = data.get('type')
        
        # 각 코드에 맞는 함수 실행
        if data_type == 'barcode':
            return get_product_by_barcode(data, user_email)
        elif data_type == 'qrcode':
            return get_product_by_qrcode(data, user_email)
        else:
            return json.dumps(type_error_message, ensure_ascii=False)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return json.dumps(server_error_message, ensure_ascii=False)