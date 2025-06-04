import flet as ft
import app_state
import httpx
from datetime import datetime
from config import BASE_URL
from nav_bar import nav_bar

def get_auth_headers():
    return {"Authorization": f"Bearer {app_state.access_token}"}

def fetch_history():
    try:
        with httpx.Client() as client:
            res = client.get(f"{BASE_URL}/api/history", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json().get("products", [])
    except Exception as e:
        print("검색 기록 요청 실패:", e)
    return []

def format_time(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return dt_str

def render_history_item(item):
    return ft.Container(
        padding=10,
        bgcolor=ft.Colors.WHITE,
        margin=ft.margin.only(bottom=10),
        border_radius=10,
        content=ft.Row(
            controls=[
                ft.Image(src=item.get("image_url", ""), width=60, height=60, fit=ft.ImageFit.COVER),
                ft.Container(width=10),
                ft.Column(
                    controls=[
                        ft.Text(item["name"], size=16, weight="bold"),
                        ft.Text(f"열람 시각: {format_time(item['viewed_at'])}", size=12, color=ft.Colors.GREY)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )
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
