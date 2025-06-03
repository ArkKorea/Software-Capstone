import flet as ft
from datetime import datetime, date
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar
from config import BASE_URL
import httpx
import app_state

def add_diet_screen(page: ft.Page):
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    try:
        selected_date = ft.Ref[date]()
        selected_date.current = date.fromisoformat(date_str) if date_str else datetime.now().date()
    except ValueError:
        selected_date.current = datetime.now().date()

    selected_time = ft.Ref[datetime.time]()
    selected_time.current = datetime.now().time()

    food_input = ft.TextField(hint_text="음식명", expand=True, bgcolor=ft.Colors.GREY_100, border_radius=8)
    food_error_text = ft.Text("", size=12, color=ft.Colors.RED)
    quantity_value = ft.Text("1", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)

    def on_quantity_change(e):
        quantity_value.value = str(int(quantity_slider.value))
        page.update()

    quantity_slider = ft.Slider(min=1, max=5, divisions=4, value=1, width=300, label="{value}", on_change=on_quantity_change)

    memo_input = ft.TextField(hint_text="메모 (선택 사항)", multiline=True, max_lines=3,
                              bgcolor=ft.Colors.GREY_100, border_radius=8, expand=True)

    date_text = ft.Text(strftime_safe(selected_date.current, "%b %d, %Y"), size=16, color=ft.Colors.GREEN)
    time_text = ft.Text(strftime_safe(selected_time.current, "%I:%M %p"), size=16, color=ft.Colors.GREEN)

    def on_date_change(e):
        if date_picker.value:
            selected_date.current = date_picker.value
            date_text.value = strftime_safe(selected_date.current, "%b %d, %Y")
            page.update()

    date_picker = ft.DatePicker(first_date=date(2020, 1, 1), last_date=date(2030, 12, 31), on_change=on_date_change)

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

    def show_success_popup():
        popup = ft.Container(
            alignment=ft.alignment.center,
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=20,
                width=350,
                height=230,
                content=ft.Column([
                    ft.Container(
                        width=90,
                        height=90,
                        border_radius=45,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home//dietmanagement/adddiet/save_success.png",
                            fit=ft.ImageFit.COVER
                        )
                    ),
                    ft.Text("저장을 완료하였습니다.", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        content=ft.Text("이전으로", size=18),
                        on_click=lambda e: close_and_go_back(),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            padding=ft.Padding(60, 10, 60, 10),
                            shape=ft.RoundedRectangleBorder(radius=12)
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
            ),
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK)
        )
        page.dialog = None
        page.overlay.append(popup)
        page.update()

    def close_and_go_back():
        origin = qs.get("from", ["management"])[0]
        page.overlay.clear()
        if origin == "daydiet":
            page.go(f"/daydiet?date={selected_date.current.isoformat()}")
        else:
            page.go("/dietmanagement")

    def show_product_popup(suggested_products, record_id):
        match_product_id = ft.Ref[int]()
        match_product_id.current = 0

        warning_text = ft.Text("", size=12, color=ft.Colors.RED)

        radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Image(src=p.get("image_url"), width=40, height=40),
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Text(str(p["product_id"]), size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(p["name"], size=14)
                                ],
                                spacing=2,
                                alignment=ft.alignment.top_left
                            )
                        ),
                        ft.Radio(value=str(p["product_id"]))
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
                for p in suggested_products
            ]),
            on_change=lambda e: match_product_id.__setattr__("current", int(e.control.value))
        )

        def on_confirm(e):
            if match_product_id.current == 0:
                warning_text.value = "연동 상품을 선택하여야 합니다."
                page.update()
                return

            page.overlay.clear()
            with httpx.Client(base_url=BASE_URL) as client:
                client.post(
                    "/api/user/meals/select-product",
                    headers={"Authorization": f"Bearer {app_state.access_token}"},
                    json={"record_id": record_id, "matched_product_id": match_product_id.current}
                )
            show_success_popup()

        def on_skip(e):
            page.overlay.clear()
            show_success_popup()

        popup = ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=20,
                width=300,
                height=420,
                content=ft.Column([
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            "찾으시는 상품이 맞습니까?",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        )
                    ),
                    ft.Divider(height=12),
                    radio_group,
                    warning_text,
                    ft.Column([
                        ft.ElevatedButton(
                            text="연동하기",
                            on_click=on_confirm,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                padding=ft.Padding(16, 10, 16, 10),
                                shape=ft.RoundedRectangleBorder(radius=12)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Skip",
                            on_click=on_skip,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.WHITE,
                                color=ft.Colors.GREEN,
                                padding=ft.Padding(16, 10, 16, 10),
                                shape=ft.RoundedRectangleBorder(radius=12)
                            )
                        )
                    ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
                ], spacing=16)
            )
        )
        page.dialog = None
        page.overlay.append(popup)
        page.update()

    def save_diet(e):
        food_name = food_input.value.strip()
        quantity = int(quantity_slider.value)
        memo = memo_input.value.strip() or ""

        if not food_name:
            food_error_text.value = "필수 캔프 항목입니다."
            page.update()
            return
        else:
            food_error_text.value = ""

        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/user/meals/create",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={
                    "datetime": f"{selected_date.current.isoformat()}T{strftime_safe(selected_time.current, '%H:%M:%S')}",
                    "food_name": food_name,
                    "quantity": quantity,
                    "memo": memo
                }
            )
            if response.status_code == 200:
                data = response.json()
                record_id = data["record_id"]
                suggested_products = data["suggested_products"]
                if suggested_products:
                    show_product_popup(suggested_products, record_id)
                else:
                    show_success_popup()

    def go_back_with_overlay(e):
        origin = qs.get("from", ["management"])[0]
        page.overlay.clear()
        if origin == "daydiet":
            page.go(f"/daydiet?date={selected_date.current.isoformat()}")
        else:
            page.go("/dietmanagement")

    return ft.View(
        route=f"/adddiet?date={selected_date.current.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text("내   식   단   관   리", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back_with_overlay)
            ),
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column([
                    ft.Row([
                        ft.Text("날짜", size=16),
                        ft.GestureDetector(content=date_text, on_tap=lambda _: open_date_picker())
                    ]),
                    ft.Divider(height=16),
                    ft.Row([
                        ft.Text("설치 시간", size=16),
                        ft.GestureDetector(content=time_text, on_tap=lambda _: open_time_picker())
                    ]),
                    ft.Divider(height=16),
                    ft.Text("식단명", size=16),
                    food_input,
                    food_error_text,
                    ft.Divider(height=16),
                    ft.Text("식사량 (1~5)", size=16),
                    ft.Row([quantity_slider, quantity_value]),
                    ft.Divider(height=16),
                    ft.Text("메모 (선택)", size=16),
                    memo_input,
                    ft.Container(expand=True),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Text("\u2714 \uc800장하기", size=18, weight=ft.FontWeight.BOLD),
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
                ], expand=True)
            ),
            nav_bar(page, current_route="/adddiet")
        ],
        bgcolor=ft.Colors.WHITE
    )

def strftime_safe(dt, fmt):
    try:
        return dt.strftime(fmt)
    except Exception:
        return ""
