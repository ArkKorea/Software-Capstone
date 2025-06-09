import flet as ft
from nav_bar import nav_bar
import app_state
import app_state

def home_screen(page: ft.Page):
    search_filter = ft.Ref[str]()
    search_filter.current = "제품명"

    sound_on = ft.Ref[bool]()
    sound_on.current = True

    notification_icon = ft.IconButton(
        icon="notifications_none_outlined",
        on_click=lambda e: toggle_sound(e)
    )

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

    def toggle_sound(e):
        sound_on.current = not sound_on.current
        notification_icon.icon = (
            "notifications_none_outlined" if sound_on.current else "notifications_off_outlined"
        )
        page.update()

    def change_filter(e):
        selected = e.control.text
        search_filter.current = selected
        selected_filter_label.value = selected
        page.update()

    def home_search(e):
        keyword = search_field.value.strip()
        if keyword == "":
            return
        app_state.search_keyword = keyword
        app_state.search_category = search_filter.current
        page.go("/searchview")
            
    selected_filter_label = ft.Text(search_filter.current, size=14)
    search_field.on_submit = home_search

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

    return ft.View(
        "/home",
        controls=[
            ft.Column(
                controls=[
                    # 헤더
                    ft.Container(
                        content=ft.Row([
                            ft.Image(
                                src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                                width=200
                            ),
                            ft.Row(
                                controls=[notification_icon],
                                spacing=10
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.Padding(10, 10, 10, 10)
                    ),

                    # 유저 정보
                    ft.Container(
                        content=ft.Row([
                            ft.CircleAvatar(
                                foreground_image_src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_avatar.png",
                                radius=40
                            ),
                            ft.Container(width=10),
                            ft.Column([
                                ft.Text("안녕하세요", size=20),
                                ft.Text((page.client_storage.get("display_name") or "홍길동") + "님", size=25)


                            ])
                        ]),
                        padding=ft.Padding(10, 5, 10, 5)
                    ),


                    ft.Container(height=10),

                    # 통합 검색창
                    ft.Container(
                        padding=ft.Padding(10, 20, 10, 20),
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
                                        #content=ft.TextField(
                                        #    hint_text="Search",
                                        #    border=None,
                                        #    filled=False,
                                        #    height=40,
                                        #    bgcolor=None,
                                        #    text_size=16,
                                        #    cursor_color=ft.Colors.BLACK,
                                        #    content_padding=ft.Padding(0, 0, 0, 0),
                                        #    border_color=ft.Colors.TRANSPARENT,
                                        #    border_radius=0
                                        #)
                                    ),
                                    filter_row
                                ]
                            )
                        )
                    ),

                    # 광고 배너
                    ft.Container(
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_adbanner.png",
                            width=page.width * 0.9,
                            border_radius=10
                        ),
                        alignment=ft.Alignment(0, 0)
                    ),

                    ft.Container(height=10),

                    # 카테고리 제목
                    ft.Container(
                        padding=ft.Padding(10, 0, 10, 0),
                        content=ft.Text("카테고리", size=18, weight=ft.FontWeight.BOLD)
                    ),

                    ft.Container(height=10),

                    # 카테고리 버튼
                    ft.Container(
                        height=110,
                        padding=ft.Padding(10, 0, 10, 0),
                        content=ft.Row(
                            controls=[
                                category_button("QR 코드", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_qr.png"),
                                category_button("OCR 인식", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_ocr.png","/ocr"),
                                category_button("내 상품 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myitems.png", "/productmanagement"),
                                category_button("내 식단 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_mydiet.png", "/dietmanagement"),
                                category_button("즐겨찾기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_favorites.png", "/favorites"),
                                category_button("내 알레르기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myallergy.png", "/myallergy"),
                            ],
                            spacing=10,
                            scroll=ft.ScrollMode.HIDDEN,  # ✅ 스크롤바 감추기
                            alignment=ft.MainAxisAlignment.START
                        )
                    ),

                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),
            nav_bar(page, current_route="/home")
        ]
    )

def category_button(label, image_url, route="/home"):
    return ft.GestureDetector(
        on_tap=lambda e: e.page.go(route),
        content=ft.Container(
            width=90,
            height=90,
            bgcolor=ft.Colors.GREEN_400,
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                [
                    ft.Image(src=image_url, width=36, height=36),
                    ft.Text(label, size=12, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            )
        )
    )
