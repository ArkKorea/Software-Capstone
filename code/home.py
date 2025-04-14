import flet as ft

def home_screen(page: ft.Page):
    return ft.View(
        "/home",
        controls=[
            ft.Column(
                controls=[
                    # 상단 여백 + 로고 & 아이콘들 (알림 + 전체메뉴)
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

                    # 프로필 & 환영 문구
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

                    # 검색창
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

                    # 광고 이미지
                    ft.Container(
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_adbanner.png",
                            width=page.width * 0.9,
                            border_radius=10
                        ),
                        alignment=ft.alignment.center
                    ),

                    ft.Container(height=20),

                    # 카테고리 제목
                    ft.Container(
                        padding=ft.Padding(top=0, left=10, right=10, bottom=0),
                        content=ft.Text("카테고리", size=16, weight=ft.FontWeight.BOLD)
                    ),

                    ft.Container(height=10),

                    # 가로 스크롤 가능한 카테고리 버튼들
                    ft.Container(
                        height=110,
                        padding=ft.Padding(left=10, right=10, top=0, bottom=0),
                        content=ft.Row(
                            controls=[
                                category_button("QR 코드", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_qr.png"),
                                category_button("OCR 인식", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_ocr.png"),
                                category_button("내 상품 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myitems.png"),
                                category_button("내 식단 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_mydiet.png"),
                                category_button("즐겨찾기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_favorites.png"),
                                category_button("내 알레르기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myallergy.png"),
                            ],
                            spacing=10,
                            scroll=ft.ScrollMode.ALWAYS,
                            alignment=ft.MainAxisAlignment.START
                        )
                    ),

                    ft.Container(height=70)  # 바텀 네비게이션 공간 확보용
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),

            # 하단 바텀 네비게이션 바
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=ft.Padding(top=8, bottom=8, left=8, right=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        nav_icon(ft.Icons.HOME, "Home", selected=True),
                        nav_icon(ft.Icons.SEARCH, "Search"),

                        # 가운데 QR 버튼 (조금 위로 이동)
                        ft.Container(
                            content=ft.FloatingActionButton(
                                icon=ft.Icons.QR_CODE_SCANNER,
                                bgcolor=ft.Colors.GREEN,
                                mini=True,
                                height=40,
                                width=40
                            ),
                            margin=ft.margin.only(top=-10)
                        ),

                        nav_icon(ft.Icons.HISTORY, "History"),
                        nav_icon(ft.Icons.PERSON_OUTLINE, "Profile")
                    ]
                ),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                height=65
            )
        ]
    )

# 카테고리 버튼
def category_button(label, image_url):
    return ft.Container(
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

# 하단 아이콘 + 텍스트 조합
def nav_icon(icon, label, selected=False):
    color = ft.Colors.GREEN if selected else ft.Colors.BLUE_GREY
    return ft.Column(
        [
            ft.Icon(icon, color=color, size=20),
            ft.Text(label, size=11, color=color)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
