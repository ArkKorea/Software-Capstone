import json

server_error_message = {"error": "서버 오류입니다. 잠시 후 다시 시도해주세요.", "code": "INTERNAL_SERVER_ERROR"}

def get_food_detail_by_id(cursor, food_id, user_email):
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        user_id = user['id']

        cursor.execute("SELECT * FROM foods WHERE food_id = %s", (food_id,))
        food = cursor.fetchone()
    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)