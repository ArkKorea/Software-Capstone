import flet as ft
from datetime import date
from nav_bar import nav_bar  # 네비게이션 바 임포트
import functools

SYMPTOM_CATEGORIES = ["피부", "복통", "호흡", "두통", "피로"]

selected_date = None
username = None

def today_symptom_screen(page: ft.Page):
    global selected_date, username

    if selected_date is None:
        selected_date = date.today()

    ratings = {symptom: 0 for symptom in SYMPTOM_CATEGORIES}
    error_msgs = {symptom: ft.Text("", color=ft.Colors.RED, size=12) for symptom in SYMPTOM_CATEGORIES}
    rating_containers = {}

    others_input = ft.TextField(hint_text="Tell us everything.", multiline=True, width=400)
    result_text = ft.Text("")

    def update_rating(symptom, rating):
        ratings[symptom] = rating
        error_msgs[symptom].value = ""
        rating_containers[symptom].controls = build_star_row(symptom).controls
        page.update()

    def on_submit(e):
        has_error = False
        for symptom in SYMPTOM_CATEGORIES:
            if ratings[symptom] == 0:
                error_msgs[symptom].value = "필수 체크 항목입니다."
                has_error = True
        result_text.value = "" if has_error else "증상이 저장되었습니다."
        page.update()

    def build_star_row(symptom):
        def make_star(index):
            return ft.GestureDetector(
                on_tap=lambda e: update_rating(symptom, index + 1),
                content=ft.Icon(
                    name=ft.Icons.STAR,
                    color=ft.Colors.GREEN if index < ratings[symptom] else ft.Colors.GREY_300,
                    size=24,
                )
            )

        return ft.Column(
            controls=[
                ft.Text(symptom, size=16),
                ft.Row(
                    controls=[make_star(i) for i in range(5)],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.START
                ),
                error_msgs[symptom]
            ],
            spacing=2
        )

    symptom_ui_list = []
    for symptom in SYMPTOM_CATEGORIES:
        rating_containers[symptom] = ft.Column(controls=build_star_row(symptom).controls)
        symptom_ui_list.append(rating_containers[symptom])

    return ft.View(
        "/todaysymptom",
        controls=[
            ft.AppBar(
                title=ft.Text("오 늘 의   증 상", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home")
                )
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.Text(f"{selected_date.strftime('%Y-%m-%d')} {username}님 오늘의 증상",
                                    size=20, weight=ft.FontWeight.BOLD),
                            *symptom_ui_list,
                            ft.Text("기타 증상", size=16, weight=ft.FontWeight.BOLD),
                            others_input,
                            ft.ElevatedButton(
                                "저장 하기",
                                on_click=on_submit,
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                width=400
                            ),
                            result_text
                        ],
                        spacing=20)
                    )
                ]
            ),
            nav_bar(page, current_route="/todaysymptom")
        ]
    )


def route_change(page: ft.Page, route: str):
    global selected_date, username
    if route == "/todaysymptom":
        selected_date = date.today()
        username = "홍길동"
        page.views.append(today_symptom_screen(page))
        page.update()
