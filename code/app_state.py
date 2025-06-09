# app_state.py
pending_camera_invoke = False

# 로그인 이후 저장값
access_token: str = ""
user: dict = {} # 로그인 이후 user정보를 딕셔너리로 저장

search_keyword = ""
search_category = "제품명"

editing_product = None