# 검색 기능의 진입점
import qr_barcode_module.error_messages as error
import json

# qr 혹은 바코드처럼 반환에 즐겨찾기 여부가 없어서 이메일은 제외
def get_result_by_query(input_json_data):
    try:
        search_type = input_json_data.get('type')
        if search_type is None:
            return json.dumps(error.missing_serarch_type_message, ensure_ascii=False)
        if search_type not in ['product', 'store']:
            return json.dumps(error.invalid_search_type_message, ensure_ascii=False)
        keyword = input_json_data.get('query')
        if search_type == 'product':
            return
        elif search_type == 'store':
            return

    except Exception as e:
        return json.dumps(error.server_error_message, ensure_ascii=False)