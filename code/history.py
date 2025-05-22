import flet as ft
from nav_bar import nav_bar  # 네비게이션 바 임포트

# 최근 검색 기록 페이지
def history_screen(page: ft.Page):
    recent_searches = []  # 나중에 DB 연동 예정

    return ft.View(
        "/history",
        controls=[
            # 상단 AppBar (뒤로가기 버튼 제거됨)
            ft.AppBar(
                title=ft.Text("기  록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE
            ),

            # 본문 컨텐츠
            ft.Column(
                controls=[
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text("최근 30개의 검색 기록", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.Padding(top=10, right=10, bottom=10, left=10)
                    ),
                    ft.Column(
                        controls=[],  # 검색 기록은 추후 DB 연동 시 표시 예정
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.HIDDEN
                    ),
                    ft.Container(height=70)  # 네비게이션 바 영역 확보용
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),

            # 하단 네비게이션 바
            nav_bar(page, current_route="/history")
        ],
        bgcolor=ft.Colors.WHITE
    )
