import flet as ft
from nav_bar import nav_bar  # 네비게이션 바 임포트

# 공지사항 페이지
def notice_screen(page: ft.Page):
    def back_to_home(e):
        page.go("/profileview")

    return ft.View(
        "/notice",
        controls=[
            # 상단 AppBar
            ft.AppBar(
                title=ft.Text("공  지  사  항", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=back_to_home
                )
            ),

            # 본문 컨텐츠
            ft.Column(
                controls=[
                    # 공지사항 영역 (추후 DB 연동 등 추가 예정)
                    ft.Container(
                        padding=ft.Padding(16, 16, 16, 16),
                        content=ft.Text("공지사항이 없습니다.", size=16, color=ft.Colors.GREY)
                    ),
                    ft.Container(height=70)  # 하단 네비게이션 공간 확보
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),

            # 하단 네비게이션 바
            nav_bar(page, current_route="/notice")
        ],
        bgcolor=ft.Colors.WHITE
    )
