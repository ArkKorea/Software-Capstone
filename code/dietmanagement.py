import flet as ft
from datetime import date, timedelta
from nav_bar import nav_bar
import calendar


def generate_full_calendar(month: int, year: int):
    first_day_of_month = date(year, month, 1)
    first_weekday = (first_day_of_month.weekday() + 1) % 7  # Sunday=0
    days_in_month = calendar.monthrange(year, month)[1]

    # 시작 날짜: 전달의 마지막 날짜 포함
    start_date = first_day_of_month - timedelta(days=first_weekday)

    # 마지막 날짜: 다음달 초 포함 (6줄 * 7칸)
    total_cells = 6 * 7
    calendar_days = [start_date + timedelta(days=i) for i in range(total_cells)]
    return calendar_days


def diet_management_screen(page: ft.Page):
    today = date.today()
    current_year = today.year
    current_month = today.month

    calendar_days = generate_full_calendar(current_month, current_year)

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    weekday_colors = [ft.colors.RED] + [ft.colors.GREY] * 5 + [ft.colors.BLUE]

    # 요일 라벨
    weekday_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        controls=[
            ft.Container(
                content=ft.Text(day, size=14, color=color),
                width=48,
                height=50,
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=10)
            )
            for day, color in zip(weekday_labels, weekday_colors)
        ]
    )

    # 달력 날짜 그리드
    calendar_grid = []
    for week_index in range(6):
        row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[]
        )
        for day_index in range(7):
            date_obj = calendar_days[week_index * 7 + day_index]
            is_current_month = (date_obj.month == current_month)
            is_today = (date_obj == today)

            # 요일 색상 설정
            if day_index == 0:
                number_color = ft.colors.RED
            elif day_index == 6:
                number_color = ft.colors.BLUE
            else:
                number_color = ft.colors.BLACK

            # 마지막 주의 다음달 날짜는 비워두기
            if not is_current_month and week_index == 5:
                day_container = ft.Container(width=48, height=60)
            else:
                # 날짜 텍스트 또는 오늘 표시
                if is_today:
                    content = ft.Container(
                        width=38,  # 가로 길이 살짝 줄임
                        height=28,
                        bgcolor=ft.colors.GREEN,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            str(date_obj.day),
                            size=13,
                            color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER
                        )
                    )
                else:
                    content = ft.Text(
                        str(date_obj.day),
                        size=13,
                        color=number_color if is_current_month else ft.colors.GREY,
                        text_align=ft.TextAlign.CENTER
                    )

                # 날짜 컨테이너
                day_container = ft.Container(
                    width=48,
                    height=60,
                    alignment=ft.alignment.center,
                    content=content
                )

            row.controls.append(day_container)
        calendar_grid.append(row)

    return ft.View(
        "/dietmanagement",
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("내   식 단 관 리", size=24),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=50, bottom=10)
                    ),
                    ft.Text(
                        calendar.month_name[current_month],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(
                        content=weekday_row,
                        padding=ft.padding.only(top=20, bottom=15)
                    ),
                    ft.Column(
                        controls=calendar_grid,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="+ 식단 추가하기",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=30),
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE,
                                padding=ft.Padding(20, 10, 20, 10)
                            ),
                            on_click=lambda e: print("식단 추가 클릭됨!")
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=60)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            nav_bar(page, current_route="/dietmanagement")
        ],
        bgcolor=ft.colors.WHITE
    )
