import json
from qr_barcode_module.error_messages import server_error_message

def get_food_detail_by_id(cursor, food_id, user_email):
    try:
        # user_email을 통해 user_id를 가져옴
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        user_id = user['id']

        # food_id를 통해 food 정보를 가져옴
        cursor.execute("SELECT * FROM foods WHERE food_id = %s", (food_id,))
        food = cursor.fetchone()
        
        # food의 supplier_name 가져오기기
        cursor.execute("SELECT name FROM suppliers WHERE id = %s", (food['supplier_id'],))
        supplier_name = cursor.fetchone()['name']

        # 사용자가 food를 즐겨찾기를 했는지
        cursor.execute("SELECT * FROM favorites WHERE user_id = %s AND food_id = %s", (user_id, food_id))
        is_favorite = True if cursor.fetchone() else False
        # user_id로 사용자의 알러지 정보 가져옴
        cursor.execute("SELECT allergen_id FROM user_allergens WHERE user_id = %s", (user_id,))
        user_allergies = [row["allergen_id"] for row in cursor.fetchall()]

        # food_id로 음식의 알러지 정보 가져옴
        cursor.execute("SELECT allergen_id FROM food_allergens WHERE food_id = %s", (food_id,))
        food_allergens = [row["allergen_id"] for row in cursor.fetchall()]

        # 사용자와 음식의 알러지 교집합 계산
        allergen_hit = []
        for user_allergy in user_allergies:
            if user_allergy in food_allergens:
                allergen_hit.append(user_allergy)
        
        # 음식의 알러지 중 안전한 것들
        allergen_safe = food_allergens - allergen_hit

        return {
            "product_id" : food_id,
            "name" : food['name'],
            "image_url" : food['image_url'],
            "allergen_hit" : allergen_hit,
            "allergen_safe" : allergen_safe,
            "ingredient" : food['ingredient'],
            "is_favorite" : is_favorite,
            "supplier_id" : food['supplier_id'],
            "supplier_name" : supplier_name,
        }
    except Exception as e:
        return json.dumps(server_error_message, ensure_ascii=False)