# day_diet.py

import flet as ft
from datetime import date

def day_diet_screen(page: ft.Page, selected_date: date):
    # 예시 식단 데이터
    sample_data = {
        "2025-04-05": [
            {"time": "11:35", "meals": ["치즈불닭볶음면", "참치마요 삼각김밥", "쿨피스 복숭아맛"]},
            {"time": "13:15", "meals": ["아몬드 초콜릿"]},
            {"time": "15:10", "meals": ["토마토 파스타", "고르곤졸라 피자", "청포도 에이드"]}
        ]
    }

    date_str = selected_date.strftime("%Y-%m-%d")
    meals = sample_data.get(date_str, [])

    # 날짜 표시
    date_display = ft.Column([
        ft.Text(selected_date.strftime("%d"), size=32, weight=ft.FontWeight.BOLD),
        ft.Text(selected_date.strftime("%A").upper(), size=14, color=ft.Colors.GREY),
        ft.Text(selected_date.strftime("%B %Y"), size=14, color=ft.Colors.GREY),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # 오늘의 증상으로 이동
    def on_today_symptom(e):
        # 1) 기존 BottomSheet 닫기
        page.overlay.clear()
        # 2) 선택 날짜를 쿼리로 넘겨서 내비게이트
        page.go(f"/todaysymptom?date={selected_date.isoformat()}")

    # 식단 리스트 또는 “없음” 메시지
    meal_list_controls = (
        [
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                cross_axis_alignment=ft.CrossAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(entry["time"], size=14, weight=ft.FontWeight.BOLD),
                    ft.Expanded(
                        ft.Container(
                            padding=10,
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=10,
                            content=ft.Column(
                                controls=[ft.Text(m, size=14) for m in entry["meals"]]
                            )
                        )
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MORE_VERT,
                        icon_color=ft.Colors.GREY_600,
                        on_click=lambda e: print("옵션 클릭")
                    )
                ]
            )
            for entry in meals
        ]
        if meals else
        [ft.Text("등록된 식단이 없습니다.", size=14, color=ft.Colors.GREY_600, italic=True)]
    )

    return ft.BottomSheet(
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            content=ft.Column(
                controls=[
                    # 날짜 + 오늘의 증상 버튼
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            date_display,
                            ft.TextButton(
                                text="오늘의 증상",
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_100,
                                    color=ft.Colors.GREEN,
                                    padding=ft.Padding(12, 6, 12, 6),
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=on_today_symptom
                            )
                        ]
                    ),
                    ft.Divider(height=20, thickness=1),
                    # 헤더
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=40,
                                controls=[
                                    ft.Text("Time", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                    ft.Text("식단 기록", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                ]
                            ),
                            ft.TextButton(
                                text="추가하기",
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN_100,
                                    color=ft.Colors.GREEN,
                                    padding=ft.Padding(16, 8, 16, 8),
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=lambda e: page.go("/adddiet")
                            )
                        ]
                    ),
                    ft.Divider(),
                    # 식단 항목
                    *meal_list_controls,
                    ft.Container(height=20),
                ],
                scroll=ft.ScrollMode.AUTO
            )
        ),
        show_drag_handle=True,
        open=True
    )
