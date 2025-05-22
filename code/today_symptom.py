import flet as ft
from datetime import date
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar

SYMPTOM_CATEGORIES = ["피부", "복통", "호흡", "두통", "피로"]

def today_symptom_screen(page: ft.Page):
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    try:
        selected_date = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        selected_date = date.today()

    username = "홍길동"

    ratings = {s: 0 for s in SYMPTOM_CATEGORIES}
    error_msgs = {s: "" for s in SYMPTOM_CATEGORIES}
    result_text = ft.Text("")
    others_input = ft.TextField(hint_text="Tell us everything.", multiline=True, width=400)

    # 상위 컨테이너 안에 전체 증상 평가 영역이 들어감
    symptom_column = ft.Column(spacing=20)

    def go_back_to_day_diet(e):
        page.overlay.clear()
        page.go(f"/daydiet?date={selected_date.isoformat()}")

    def update_rating(symptom, rating):
        ratings[symptom] = rating
        error_msgs[symptom] = ""
        refresh_symptom_ui()

    def refresh_symptom_ui():
        symptom_column.controls = build_symptom_ui()
        page.update()

    def on_submit(e):
        has_error = False
        for s in SYMPTOM_CATEGORIES:
            if ratings[s] == 0:
                error_msgs[s] = "필수 체크 항목입니다."
                has_error = True
            else:
                error_msgs[s] = ""
        result_text.value = "" if has_error else "증상이 저장되었습니다."
        refresh_symptom_ui()

    def build_symptom_ui():
        ui_list = [
            ft.Text(f"{selected_date.strftime('%Y-%m-%d')} {username}님 오늘의 증상", size=20, weight=ft.FontWeight.BOLD)
        ]
        for symptom in SYMPTOM_CATEGORIES:
            ui_list.append(
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(symptom, size=16),
                        ft.Row(
                            spacing=2,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.GestureDetector(
                                    on_tap=lambda e, s=symptom, i=i: update_rating(s, i + 1),
                                    content=ft.Icon(
                                        name=ft.Icons.STAR,
                                        color=ft.Colors.GREEN if i < ratings[symptom] else ft.Colors.GREY_300,
                                        size=24
                                    )
                                )
                                for i in range(5)
                            ]
                        ),
                        ft.Text(error_msgs[symptom], size=12, color=ft.Colors.RED) if error_msgs[symptom] else ft.Container()
                    ]
                )
            )
        ui_list.extend([
            ft.Text("기타 증상", size=16, weight=ft.FontWeight.BOLD),
            others_input,
            ft.ElevatedButton("저장 하기", on_click=on_submit, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=400),
            result_text
        ])
        return ui_list

    # 처음 UI 세팅
    symptom_column.controls = build_symptom_ui()

    return ft.View(
        route=f"/todaysymptom?date={selected_date.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text("오 늘 의   증 상", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back_to_day_diet)
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    ft.Container(
                        padding=20,
                        content=symptom_column
                    )
                ]
            ),
            nav_bar(page, current_route="/todaysymptom")
        ]
    )
