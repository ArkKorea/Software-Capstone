import flet as ft
from nav_bar import nav_bar
from config import BASE_URL
import app_state
import httpx

def search_view_screen(page: ft.Page):
    search_filter = ft.Ref[str]()
    search_filter.current = "제품명"
    recent_searches = []

    search_result = ft.Column(
        controls=[
            ft.Icon(name="search_off", size=80, color=ft.Colors.GREY_400),
            ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    recent_search_column = ft.Column()

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

        category = "product" if search_filter.current == "제품명" else "store"
        
        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/search",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={
                    "type": category,
                    "query": keyword
                }
            )
            if response.status_code == 200:
                if category == "product":
                    matched = response.json()
                    matched_products = matched["products"]
                    if matched_products:
                        search_result.controls = [ft.Text(item["name"], size=16) for item in matched_products]
                    matched_bundles = matched["bundles"]
                    if matched_bundles:
                        search_result.controls = search_result.controls + [ft.Text(item["name"], size=16) for item in matched_bundles]
                else:
                    matched = response.json()["stores"]
                    search_result.controls = [ft.Text(store["name"], size=16) for store in matched]
            else:
                search_result.controls = [
                ft.Icon(name="search_off", size=80, color=ft.Colors.GREY_400),
                ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600)
            ]
            """
            현재 검색기능이 완료되었습니다. 다만 검색 기능에 대한 출력이 위에 텍스트만 나오게 되어있어요.
            이를 다양한 정보가 더 나오도록 꾸며주시기를 요청드립니다.
            """
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
                                )
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
                                    filter_row
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
                scroll=ft.ScrollMode.HIDDEN
            ),
            nav_bar(page, current_route="/searchview")
        ]
    )
