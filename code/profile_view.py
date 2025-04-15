import flet as ft

def profile_screen(page: ft.Page):
    return ft.View(
        "/profile",
        controls=[
            ft.Column(
                expand=True,
                controls=[
                    # 상단 로고 이미지
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.Padding(left=0, top=40, right=0, bottom=10),
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                            width=180,
                            fit=ft.ImageFit.CONTAIN
                        )
                    ),

                    # 프로필 아바타 + 닉네임 + 유저네임
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.Padding(left=10, top=10, right=10, bottom=10),
                        content=ft.Column(
                            [
                                ft.CircleAvatar(
                                    radius=40,
                                    content=ft.Image(
                                        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/profile/home_profile_avatar.png",
                                        fit=ft.ImageFit.COVER
                                    )
                                ),
                                ft.Text("홍길동님", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("@username", size=14, color=ft.Colors.GREY)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        )
                    ),

                    # 메뉴 리스트
                    ft.Divider(height=1, thickness=1),
                    *[menu_item(label) for label in [
                        "공지사항", "이용 약관", "내 알레르기", "알림 설정",
                        "고객센터", "언어", "회원 탈퇴", "로그아웃"
                    ]],
                    ft.Divider(height=1, thickness=1),
                ],
                scroll=ft.ScrollMode.AUTO
            ),

            # 하단 네비게이션 바
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=ft.Padding(left=8, top=8, right=8, bottom=8),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        nav_icon(ft.Icons.HOME, "Home", page, "/home"),
                        nav_icon(ft.Icons.SEARCH, "Search", page, "/search"),
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
                        nav_icon(ft.Icons.HISTORY, "History", page, "/history"),
                        nav_icon(ft.Icons.PERSON_OUTLINE, "Profile", page, "/profile", selected=True),
                    ]
                ),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                height=65
            )
        ]
    )

# 메뉴 항목 생성 함수
def menu_item(label):
    return ft.Container(
        content=ft.ListTile(
            title=ft.Text(label),
            trailing=ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT),
            dense=True
        ),
        padding=ft.Padding(left=10, top=0, right=10, bottom=0),
    )

# 네비게이션 아이콘
def nav_icon(icon, label, page, route, selected=False):
    color = ft.Colors.GREEN if selected else ft.Colors.BLUE_GREY
    return ft.GestureDetector(
        on_tap=lambda e: page.go(route),
        content=ft.Column(
            [
                ft.Icon(icon, color=color, size=20),
                ft.Text(label, size=11, color=color)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
