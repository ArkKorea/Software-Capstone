import flet as ft
from nav_bar import nav_bar

def search_view_screen(page: ft.Page):
    search_filter = ft.Ref[str]()
    search_filter.current = "제품명"
    sound_on = ft.Ref[bool]()
    sound_on.current = True
    recent_searches = []

    dummy_db = {
        "매장명": ["쉐프공방", "헬씨키친", "비건레스토랑"],
        "제품명": ["알러지프리쿠키", "무유제품빵", "콩단백스낵"]
    }

    search_result = ft.Column(
        controls=[
            ft.Icon(name="search_off", size=80, color=ft.Colors.GREY_400),
            ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    recent_search_column = ft.Column()

    notification_icon = ft.IconButton(
        icon="notifications_none_outlined"
    )

    def toggle_sound(e):
        sound_on.current = not sound_on.current
        notification_icon.icon = (
            "notifications_none_outlined" if sound_on.current else "notifications_off_outlined"
        )
        page.update()

    notification_icon.on_click = toggle_sound

    def change_filter(e):
        selected = e.control.text
        search_filter.current = selected
        selected_filter_label.value = selected
        page.update()

    selected_filter_label = ft.Text(search_filter.current, size=14)

    filter_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="제품명", on_click=change_filter),
            ft.PopupMenuItem(text="매장명", on_click=change_filter)
        ]
    )

    filter_row = ft.Row(
        controls=[selected_filter_label, filter_menu],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    def clear_search_history(e):
        recent_searches.clear()
        update_recent_searches()
        page.update()

    def update_recent_searches():
        recent_search_column.controls = [
            ft.Text(item, size=14) for item in recent_searches
        ]

    search_field = ft.TextField(
        hint_text="Search",
        border=None,
        filled=False,
        height=40,
        bgcolor=None,
        text_size=16,
        cursor_color=ft.Colors.BLACK,
        content_padding=ft.Padding(0, 0, 0, 0),
        border_color=ft.Colors.TRANSPARENT,
        border_radius=0
    )

    def search_enter(e):
        keyword = search_field.value.strip()
        if keyword == "":
            return

        if keyword not in recent_searches:
            recent_searches.insert(0, keyword)

        if len(recent_searches) > 10:
            recent_searches.pop()

        update_recent_searches()

        category = search_filter.current
        matched = [item for item in dummy_db[category] if keyword in item]

        if matched:
            search_result.controls = [ft.Text(item, size=16) for item in matched]
        else:
            search_result.controls = [
                ft.Icon(name="search_off", size=80, color=ft.Colors.GREY_400),
                ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600)
            ]

        page.update()

    search_field.on_submit = search_enter

    return ft.View(
        route="/searchview",
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Image(
                                    src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                                    width=200
                                ),
                                ft.Row(controls=[notification_icon], spacing=10)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.Padding(10, 40, 10, 10)
                    ),

                    ft.Container(
                        padding=ft.Padding(10, 20, 5, 20),
                        content=ft.Container(
                            border_radius=10,
                            height=50,
                            padding=ft.Padding(10, 0, 10, 0),
                            bgcolor=ft.Colors.GREY_100,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Icon(name="search", color=ft.Colors.GREY_600, size=22),
                                    ft.Container(
                                        width=page.width * 0.5,
                                        content=search_field
                                    ),
                                    filter_row  # ✅ 변경된 필터 UI
                                ]
                            )
                        )
                    ),

                    ft.Container(height=20),

                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 0),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("최근 검색", size=16, weight=ft.FontWeight.BOLD),
                                ft.TextButton("전체 삭제", on_click=clear_search_history)
                            ]
                        )
                    ),

                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 0),
                        content=recent_search_column
                    ),

                    ft.Container(height=10),

                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 0),
                        content=search_result,
                        alignment=ft.Alignment(0, 0)
                    ),

                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
            nav_bar(page, current_route="/searchview")
        ]
    )
