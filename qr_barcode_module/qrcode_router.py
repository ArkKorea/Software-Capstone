#qr코드 처리 모듈
import json

no_food_error_message = {"error": "해당 코드는 등록된 상품이 없습니다", "code" : "PRODUCT_NOT_FOUND"}
server_error_message = {"error": "서버 오류입니다. 잠시 후 다시 시도해주세요.", "code" : "INTERNAL_SERVER_ERROR"}

def get_product_by_qrcode(input_json_data, user_email):
    try:
        data = json.loads(input_json_data)
    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)