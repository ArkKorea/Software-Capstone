import flet as ft
from datetime import date

def day_diet_screen(page: ft.Page, selected_date: date) -> ft.View:
    sample_data = {
        "2025-04-05": [
            {"time": "11:35", "meals": ["치즈불닭볶음면", "참치마요 삼각김밥", "쿨피스 복숭아맛"]},
            {"time": "13:15", "meals": ["아몬드 초콜릿"]},
            {"time": "15:10", "meals": ["토마토 파스타", "고르곤졸라 피자", "청포도 에이드"]}
        ]
    }

    date_str = selected_date.strftime("%Y-%m-%d")
    meals = sample_data.get(date_str, [])

    # 상단 날짜 및 버튼 표시
    date_display = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                controls=[
                    ft.Text(selected_date.strftime("%d"), size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(selected_date.strftime("%A").upper(), size=16, color=ft.Colors.GREY),
                    ft.Text(selected_date.strftime("%B %Y"), size=16, color=ft.Colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(  # ✅ 외부 패딩으로 감쌈
                padding=ft.Padding(0, 0, 20, 0),
                content=ft.TextButton(
                    text="오늘의 증상",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_100,
                        color=ft.Colors.GREEN,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: page.go(f"/todaysymptom?date={selected_date.isoformat()}")
                )
            )
        ]
    )

    # 식단 목록
    meal_list_controls = []
    if meals:
        for entry in meals:
            meal_list_controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=16,
                    controls=[
                        ft.Text(entry["time"], size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            expand=True,
                            padding=ft.Padding(10, 0, 0, 0),
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=10,
                            content=ft.Column(
                                controls=[ft.Text(m, size=16) for m in entry["meals"]]
                            )
                        ),
                        ft.IconButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color=ft.Colors.GREY_600,
                            on_click=lambda e: print("옵션 클릭")
                        )
                    ]
                )
            )
    else:
        meal_list_controls.append(
            ft.Text("등록된 식단이 없습니다.", size=16, color=ft.Colors.GREY_600, italic=True)
        )

    return ft.View(
        route=f"/daydiet?date={selected_date.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text(""),
                bgcolor=ft.Colors.WHITE,
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/dietmanagement")
                )
            ),
            ft.Container(
                padding=ft.Padding(20, 0, 0, 0),
                content=ft.Column(
                    controls=[
                        date_display,
                        ft.Container(height=10),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=40,
                                    controls=[
                                        ft.Text("Time", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                        ft.Text("식단 기록", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                    ]
                                ),
                                ft.Container(  # ✅ 외부 패딩으로 감쌈
                                    padding=ft.Padding(0, 0, 20, 0),
                                    content=ft.TextButton(
                                        text="추가하기",
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.GREEN_100,
                                            color=ft.Colors.GREEN,
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=lambda e: page.go(f"/adddiet?from=daydiet&date={selected_date.isoformat()}")
                                    )
                                )
                            ]
                        ),
                        ft.Divider(),
                        *meal_list_controls,
                        ft.Container(height=20)
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
