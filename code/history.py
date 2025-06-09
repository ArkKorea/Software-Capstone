import flet as ft
import app_state
import httpx
from datetime import datetime
from config import BASE_URL
from nav_bar import nav_bar
from card_renderer import create_product_card, create_store_card

def get_auth_headers():
    return {"Authorization": f"Bearer {app_state.access_token}"}

def fetch_history():
    try:
        with httpx.Client() as client:
            res = client.get(f"{BASE_URL}/api/history", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json().get("history", [])
    except Exception as e:
        print("검색 기록 요청 실패:", e)
    return []

def format_time(dt):
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print("시간 포맷 에러:", e)
        return str(dt)

def render_history_item(item):
    item_type = item.get("type")
    viewed_at = item.get("viewed_at")
    data = item.get("data", {})

    # viewed_at 표시용 텍스트
    viewed_text = ft.Text(f"열람 시각: {format_time(viewed_at)}", size=12, color=ft.Colors.GREY)

    # 각각 타입에 맞는 카드 구성
    if item_type == "food" or item_type == "bundle":
        card = create_product_card(data)
    elif item_type == "supplier":
        card = create_store_card(data)
    else:
        card = ft.Text("알 수 없는 항목", color=ft.Colors.RED)

    # viewed_at 추가해서 감싸기
    return ft.Column(
        controls=[
            card,
            ft.Container(height=4),
            viewed_text,
            ft.Divider(height=1, color=ft.Colors.GREY_300)
        ]
    )

def history_screen(page: ft.Page):
    history_items = fetch_history()

    return ft.View(
        "/history",
        controls=[
            ft.AppBar(
                title=ft.Text("기  록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE
            ),

            ft.Column(
                controls=[
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text("최근 30개의 검색 기록", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.Padding(top=10, right=10, bottom=10, left=10)
                    ),
                    ft.Column(
                        controls=[
                            render_history_item(item) for item in history_items
                        ] if history_items else [
                            ft.Text("기록이 없습니다.", color=ft.Colors.GREY, size=14)
                        ],
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),

            nav_bar(page, current_route="/history")
        ],
        bgcolor=ft.Colors.WHITE
    )
