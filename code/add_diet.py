import flet as ft
from datetime import datetime, date
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar
from config import BASE_URL
import httpx
import app_state

def add_diet_screen(page: ft.Page):
    # --- [1] URL에서 날짜 파라미터 파싱 ---
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    try:
        selected_date = ft.Ref[date]()
        selected_date.current = date.fromisoformat(date_str) if date_str else datetime.now().date()
    except ValueError:
        selected_date.current = datetime.now().date()

    selected_time = ft.Ref[datetime.time]()
    selected_time.current = datetime.now().time()

    # --- [2] 입력 및 UI 구성 요소 ---
    food_input = ft.TextField(
        hint_text="음식명",
        expand=True,
        bgcolor=ft.Colors.GREY_100,
        border_radius=8
    )
    added_foods = []
    food_list_view = ft.Column()

    date_text = ft.Text(
        strftime_safe(selected_date.current, "%b %d, %Y"),
        size=16,
        color=ft.Colors.GREEN
    )
    time_text = ft.Text(
        strftime_safe(selected_time.current, "%I:%M %p"),
        size=16,
        color=ft.Colors.GREEN
    )

    # --- [3] 날짜/시간 선택기 및 핸들러 ---
    def on_date_change(e):
        if date_picker.value:
            selected_date.current = date_picker.value
            date_text.value = strftime_safe(selected_date.current, "%b %d, %Y")
            page.update()

    date_picker = ft.DatePicker(
        first_date=date(2020, 1, 1),
        last_date=date(2030, 12, 31),
        on_change=on_date_change
    )

    def open_date_picker():
        date_picker.open = True
        page.dialog = date_picker
        page.update()

    def on_time_change(e):
        if time_picker.value:
            selected_time.current = time_picker.value
            time_text.value = strftime_safe(selected_time.current, "%I:%M %p")
            page.update()

    time_picker = ft.TimePicker(on_change=on_time_change)

    def open_time_picker():
        time_picker.open = True
        page.dialog = time_picker
        page.update()

    page.overlay.extend([date_picker, time_picker])

    # --- [4] 추가 & 저장 버튼 핸들러 ---
    def add_food(e):
        if food_input.value.strip():
            added_foods.append(food_input.value.strip())
            food_list_view.controls.append(ft.Text(food_input.value.strip(), size=14))
            food_input.value = ""
            page.update()

    def save_diet(e):
        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/user/meals/create",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={
                    "date": f"{selected_date.current.isoformat()}T{strftime_safe(selected_time.current, '%H:%M:%S')}",
                    "food_name": added_foods[0], # 이건 변수가 리스트가 아니게 되면 될 것 같아요요
                    "quantity": 1, # 양을 저장할 변수 및 ui 필요요
                    "memo": None # 메모 ui가 필요
                }
            )
            if response.status_code == 200:
                print("식단이 성공적으로 저장되었습니다.")
        print(f"[저장됨] 날짜: {selected_date.current}, 시간: {strftime_safe(selected_time.current, '%H:%M')}, 식단: {added_foods}")
        page.go(f"/dietmanagement?date={selected_date.current.isoformat()}")

    # --- [5] 뒤로가기 버튼 핸들러 ---
    def go_back_with_overlay(e):
        origin = qs.get("from", ["management"])[0]
        page.overlay.clear()
        if origin == "daydiet":
            page.go(f"/daydiet?date={selected_date.current.isoformat()}")
        else:
            page.go("/dietmanagement")

    # --- [6] 최종 View 리턴 ---
    return ft.View(
        route=f"/adddiet?date={selected_date.current.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text("내   식 단 관 리", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back_with_overlay
                )
            ),
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("날짜", size=16),
                                ft.GestureDetector(content=date_text, on_tap=lambda _: open_date_picker())
                            ]
                        ),
                        ft.Divider(height=16),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("섭취 시간", size=16),
                                ft.GestureDetector(content=time_text, on_tap=lambda _: open_time_picker())
                            ]
                        ),
                        ft.Divider(height=16),
                        ft.Text("식단 입력", size=16),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                food_input,
                                ft.TextButton(
                                    text="추가하기",
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN_100,
                                        color=ft.Colors.GREEN,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=ft.Padding(12, 6, 12, 6)
                                    ),
                                    on_click=add_food
                                )
                            ]
                        ),
                        ft.Column([food_list_view], spacing=4),
                        ft.Container(expand=True),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Text("✔ 저장하기", size=18, weight=ft.FontWeight.BOLD),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN,
                                        color=ft.Colors.WHITE,
                                        padding=ft.Padding(24, 14, 24, 14),
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=save_diet
                                )
                            ]
                        )
                    ],
                    expand=True
                )
            ),
            nav_bar(page, current_route="/adddiet")
        ],
        bgcolor=ft.Colors.WHITE
    )

# ✨ strftime을 Ref 안전하게 감싸는 함수
def strftime_safe(dt, fmt):
    try:
        return dt.strftime(fmt)
    except Exception:
        return ""
