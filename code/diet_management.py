import flet as ft
from datetime import date, timedelta
import calendar
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar
from day_diet import day_diet_screen

def generate_full_calendar(month: int, year: int):
    first_day_of_month = date(year, month, 1)
    first_weekday = (first_day_of_month.weekday() + 1) % 7  # Sunday = 0
    start_date = first_day_of_month - timedelta(days=first_weekday)
    total_cells = 6 * 7
    return [start_date + timedelta(days=i) for i in range(total_cells)]

def diet_management_screen(page: ft.Page):
    today = date.today()
    current_year = ft.Ref[int]()
    current_month = ft.Ref[int]()

    current_year.current = today.year
    current_month.current = today.month

    calendar_column = ft.Column()
    month_title = ft.Text("", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    weekday_labels = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    weekday_colors = [ft.colors.RED] + [ft.colors.GREY] * 5 + [ft.colors.BLUE]

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

    def on_day_clicked(selected: date):
        page.overlay.clear()  # ✅ BottomSheet 중복 방지
        page.overlay.append(day_diet_screen(page, selected))
        page.update()

    def update_calendar():
        calendar_days = generate_full_calendar(current_month.current, current_year.current)
        month_title.value = f"{calendar.month_name[current_month.current]} {current_year.current}"
        calendar_column.controls.clear()

        for week_index in range(6):
            week_days = calendar_days[week_index * 7:(week_index + 1) * 7]

            if week_index == 5 and not any(day.month == current_month.current for day in week_days):
                continue

            row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls=[])
            for day_index, date_obj in enumerate(week_days):
                is_current_month = (date_obj.month == current_month.current)
                is_today = (date_obj == today)

                number_color = (
                    ft.colors.RED if day_index == 0 else
                    ft.colors.BLUE if day_index == 6 else
                    ft.colors.BLACK
                )

                if is_today and is_current_month:
                    content = ft.Container(
                        width=38,
                        height=28,
                        bgcolor=ft.colors.GREEN,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        content=ft.Text(str(date_obj.day), size=13, color=ft.colors.WHITE)
                    )
                else:
                    content = ft.Text(
                        str(date_obj.day),
                        size=13,
                        color=number_color if is_current_month else ft.colors.GREY
                    )

                day_container = ft.Container(
                    width=48,
                    height=60,
                    alignment=ft.alignment.center,
                    content=content,
                    on_click=lambda e, d=date_obj: on_day_clicked(d)
                )

                row.controls.append(day_container)
            calendar_column.controls.append(row)

    def go_previous_month(e):
        if current_month.current == 1:
            current_month.current = 12
            current_year.current -= 1
        else:
            current_month.current -= 1
        update_calendar()
        page.update()

    def go_next_month(e):
        if current_month.current == 12:
            current_month.current = 1
            current_year.current += 1
        else:
            current_month.current += 1
        update_calendar()
        page.update()

    # ✅ URL에서 ?date=2025-xx-xx 쿼리 있으면 팝업 자동 띄우기
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    from_str = qs.get("from", [None])[0]

    if date_str and from_str != "symptom":
        try:
            selected_date = date.fromisoformat(date_str)
            page.overlay.clear()
            page.overlay.append(day_diet_screen(page, selected_date))
        except ValueError:
            pass


    update_calendar()

    return ft.View(
        "/dietmanagement",
        controls=[
            ft.AppBar(
                title=ft.Text("내   식 단 관 리", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home")
                )
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_LEFT, on_click=go_previous_month),
                            month_title,
                            ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_RIGHT, on_click=go_next_month),
                        ]
                    ),
                    ft.Container(content=weekday_row, padding=ft.padding.only(top=20, bottom=15)),
                    calendar_column,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="+ 식단 추가하기",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=30),
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE,
                                padding=ft.Padding(20, 10, 20, 10)
                            ),
                            on_click=lambda e: page.go(f"/adddiet?from=management&date={today.isoformat()}")
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
