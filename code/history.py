import flet as ft

# 최근 검색 기록 페이지
def history_screen(page: ft.Page):
    # 검색 기록은 나중에 DB에서 가져올 예정이므로 현재는 빈 리스트
    recent_searches = []

    # 뒤로 가기 버튼 클릭 이벤트
    def back_to_home(e):
        page.go("/home")

    return ft.View(
        "/history",
        controls=[
            ft.AppBar(
                title=ft.Text("기록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=back_to_home
                )
            ),
            ft.Column(
                controls=[
                    # 최근 검색 기록 제목
                    ft.Container(
                        content=ft.Text("최근 30개의 검색 기록", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.Padding(top=10, right=10, bottom=10, left=10)
                    ),
                    ft.Container(height=10),

                    # 검색 기록이 없을 때는 빈 화면 (추후 DB 연동 예정)
                    ft.Column(
                        controls=[],  # 현재는 표시할 기록 없음
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        scroll=ft.ScrollMode.AUTO
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
        ],
        bgcolor=ft.Colors.WHITE
    )
