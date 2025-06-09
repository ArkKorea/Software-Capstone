import flet as ft
import app_state
import httpx
from datetime import datetime
from config import BASE_URL
from nav_bar import nav_bar
from card_renderer import create_product_card, create_store_card
from popup_manager import product_detail_popup, store_detail_popup

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

def render_history_item(item, page: ft.Page):
    item_type = item.get("type")
    viewed_at = item.get("viewed_at")
    data = item.get("data", {})

    viewed_text = ft.Text(f"열람 시각: {format_time(viewed_at)}", size=12, color=ft.Colors.GREY)

    if item_type == "food" or item_type == "bundle":
        card = create_product_card(data)
        card.on_click = lambda e: product_detail_popup(page, data)

    elif item_type == "supplier":
        # 👉 추가적으로 products를 받아와야 함
        def on_click(e):
            products = []
            try:
                with httpx.Client(base_url=BASE_URL) as client:
                    res = client.post(
                        "/api/store/products",
                        json={"store_id": data["store_id"]},
                        headers=get_auth_headers()
                    )
                    if res.status_code == 200:
                        products = res.json().get("products", [])
            except Exception as e:
                print("매장 제품 조회 실패:", e)

            store_detail_popup(page, data, products)

        card = create_store_card(data)
        card.on_click = on_click

    else:
        card = ft.Text("알 수 없는 항목", color=ft.Colors.RED)

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
                    render_history_item(item, page) for item in history_items
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
