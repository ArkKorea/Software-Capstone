import flet as ft
from datetime import date
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar

SYMPTOM_CATEGORIES = ["피부", "복통", "호흡", "두통", "피로"]

def today_symptom_screen(page: ft.Page):
    # URL 쿼리에서 date 파라미터 읽기
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    try:
        selected_date = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        selected_date = date.today()

    username = "홍길동"

    # ✅ 뒤로가기: overlay 제거 후 선택한 날짜로 돌아감
    def go_back_to_calendar(e):
        page.overlay.clear()
        page.go(f"/dietmanagement?date={selected_date.isoformat()}")

    # 상태 변수
    ratings = {s: 0 for s in SYMPTOM_CATEGORIES}
    error_msgs = {s: ft.Text("", color=ft.Colors.RED, size=12) for s in SYMPTOM_CATEGORIES}
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
        result_text.value = "" if not has_error else ""
        if not has_error:
            result_text.value = "증상이 저장되었습니다."
        page.update()

    def build_star_row(symptom):
        def make_star(idx):
            return ft.GestureDetector(
                on_tap=lambda e: update_rating(symptom, idx + 1),
                content=ft.Icon(
                    name=ft.Icons.STAR,
                    color=ft.Colors.GREEN if idx < ratings[symptom] else ft.Colors.GREY_300,
                    size=24,
                )
            )
        return ft.Column(
            controls=[
                ft.Text(symptom, size=16),
                ft.Row(controls=[make_star(i) for i in range(5)], spacing=2, alignment=ft.MainAxisAlignment.START),
                error_msgs[symptom]
            ],
            spacing=2
        )

    symptom_ui_list = []
    for symptom in SYMPTOM_CATEGORIES:
        rating_containers[symptom] = ft.Column(controls=build_star_row(symptom).controls)
        symptom_ui_list.append(rating_containers[symptom])

    return ft.View(
        route=f"/todaysymptom?date={selected_date.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text("오 늘 의   증 상", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back_to_calendar)
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Text(f"{selected_date.strftime('%Y-%m-%d')} {username}님 오늘의 증상",
                                        size=20, weight=ft.FontWeight.BOLD),
                                *symptom_ui_list,
                                ft.Text("기타 증상", size=16, weight=ft.FontWeight.BOLD),
                                others_input,
                                ft.ElevatedButton("저장 하기", on_click=on_submit,
                                                  bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=400),
                                result_text
                            ]
                        )
                    )
                ]
            ),
            nav_bar(page, current_route="/todaysymptom")
        ]
    )
