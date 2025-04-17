# home.py
import flet as ft
from nav_bar import nav_bar

def home_screen(page: ft.Page):
    return ft.View(
        "/home",
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Image(
                                src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                                width=200
                            ),
                            ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.NOTIFICATIONS_NONE_OUTLINED),
                                    ft.Icon(name=ft.Icons.MENU)
                                ],
                                spacing=10
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.Padding(top=40, left=10, right=10, bottom=10)
                    ),

                    ft.Container(
                        content=ft.Row([
                            ft.CircleAvatar(
                                foreground_image_src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_avatar.png",
                                radius=40
                            ),
                            ft.Container(width=10),
                            ft.Column([
                                ft.Text("안녕하세요", size=20),
                                ft.Text("홍길동님", size=25, weight=ft.FontWeight.BOLD)
                            ])
                        ]),
                        padding=ft.Padding(top=5, left=10, right=10, bottom=5)
                    ),

                    ft.Container(height=10),

                    ft.Container(
                        padding=ft.Padding(top=5, left=10, right=10, bottom=5),
                        content=ft.TextField(
                            hint_text="Search",
                            prefix_icon=ft.Icons.SEARCH,
                            suffix_icon=ft.Icons.MIC,
                            border_radius=8,
                            filled=True,
                            fill_color=ft.Colors.GREY_200
                        )
                    ),

                    ft.Container(height=10),

                    ft.Container(
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_adbanner.png",
                            width=page.width * 0.9,
                            border_radius=10
                        ),
                        alignment=ft.alignment.center
                    ),

                    ft.Container(height=20),

                    ft.Container(
                        padding=ft.Padding(top=0, left=10, right=10, bottom=0),
                        content=ft.Text("카테고리", size=16, weight=ft.FontWeight.BOLD)
                    ),

                    ft.Container(height=10),

                    ft.Container(
                        height=110,
                        padding=ft.Padding(left=10, right=10, top=0, bottom=0),
                        content=ft.Row(
                            controls=[
                                category_button("QR 코드", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_qr.png"),
                                category_button("OCR 인식", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_ocr.png"),
                                category_button("내 상품 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myitems.png", "/productmanagement"),
                                category_button("내 식단 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_mydiet.png", "/dietmanagement"),
                                category_button("즐겨찾기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_favorites.png", "/favorites"),
                                category_button("내 알레르기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myallergy.png", "/myallergy"),
                            ],
                            spacing=10,
                            scroll=ft.ScrollMode.ALWAYS,
                            alignment=ft.MainAxisAlignment.START
                        )
                    ),

                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
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
            alignment=ft.alignment.center,
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
