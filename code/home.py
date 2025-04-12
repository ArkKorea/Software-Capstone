import flet as ft

def home_screen(page: ft.Page):
    return ft.View(
        "/home",
        controls=[
            ft.Column(
                controls=[
                    # 상단 여백 + 로고 & 알림 아이콘
                    ft.Container(
                        content=ft.Row([
                            ft.Image(
                                src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                                width=120
                            ),
                            ft.Icon(name=ft.icons.NOTIFICATIONS_NONE_OUTLINED)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.Padding(top=40, left=10, right=10, bottom=10)
                    ),

                    # 프로필 & 환영 문구
                    ft.Container(
                        content=ft.Row([
                            ft.CircleAvatar(
                                foreground_image_src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_avatar.png",
                                radius=25
                            ),
                            ft.Container(width=10),
                            ft.Column([
                                ft.Text("안녕하세요", size=14),
                                ft.Text("홍길동님", size=18, weight=ft.FontWeight.BOLD)
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
                            prefix_icon=ft.icons.SEARCH,
                            suffix_icon=ft.icons.MIC,
                            border_radius=8,
                            filled=True,
                            fill_color=ft.colors.GREY_200
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

                    # 카테고리 버튼들 (Row 안에 Column들)
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                category_button("QR 코드", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_qr.png"),
                                category_button("OCR 인식", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_ocr.png"),
                                category_button("내 상품 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myitems.png"),
                                category_button("내 식단 관리", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_mydiet.png"),
                                category_button("즐겨찾기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_favorites.png"),
                                category_button("내 알레르기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_category_myallergy.png"),
                            ],
                            scroll=ft.ScrollMode.ALWAYS,
                            spacing=10
                        ),
                        padding=ft.Padding(top=0, left=10, right=10, bottom=0)
                    ),

                    ft.Container(height=70)  # 바텀 네비게이션 공간 확보용
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),

            # 하단 바텀 네비게이션 바
            # 🔹 네비게이션 바 가운데 정렬 수정
            ft.Container(
                bgcolor=ft.colors.WHITE,
                padding=ft.Padding(top=8, bottom=8, left=8, right=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,  # ← 가운데 정렬로 수정
                    controls=[
                        nav_icon(ft.icons.HOME, "Home", selected=True),
                        nav_icon(ft.icons.SEARCH, "Search"),
                        nav_icon(ft.icons.HISTORY, "History"),
                        nav_icon(ft.icons.PERSON_OUTLINE, "Profile")
                    ]
                ),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                height=65
            )
        ]
    )

# 🔹 카테고리 버튼 (초록 배경 컨테이너 + 이미지 + 텍스트)
# 🔹 카테고리 버튼 수정
def category_button(label, image_url):
    return ft.Container(
        width=90,
        height=90,
        bgcolor=ft.colors.GREEN_400,
        border_radius=10,
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Image(src=image_url, width=36, height=36),
                ft.Text(label, size=12, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )
    )


# 🔹 하단 아이콘 + 텍스트 조합
def nav_icon(icon, label, selected=False):
    color = ft.colors.GREEN if selected else ft.colors.BLUE_GREY
    return ft.Column([
        ft.Icon(icon, color=color),
        ft.Text(label, size=11, color=color)
    ], alignment=ft.MainAxisAlignment.CENTER)
