import flet as ft
from nav_bar import nav_bar

def favorites_screen(page: ft.Page):
    tab_state = ft.Ref[int]()
    content_area = ft.Ref[ft.Container]()
    store_box = ft.Ref[ft.Container]()
    food_box = ft.Ref[ft.Container]()

    def update_content(index):
        tab_state.current = index

        # 스타일 업데이트
        if index == 0:
            store_box.current.bgcolor = ft.Colors.GREEN_400
            food_box.current.bgcolor = ft.Colors.GREY_300
        else:
            store_box.current.bgcolor = ft.Colors.GREY_300
            food_box.current.bgcolor = ft.Colors.GREEN_400

        # 내용 변경
        if index == 0:
            content_area.current.content = ft.Container(
                alignment=ft.alignment.center,
                height=page.height * 0.7,
                bgcolor=ft.Colors.GREY_100,
                content=ft.Text("매장 즐겨찾기 없음", size=16, color=ft.Colors.GREY),
            )
        else:
            content_area.current.content = ft.Container(
                alignment=ft.alignment.center,
                height=page.height * 0.7,
                bgcolor=ft.Colors.GREY_100,
                content=ft.Text("음식 즐겨찾기 없음", size=16, color=ft.Colors.GREY),
            )
        page.update()

    def on_load():
        update_content(0)

    # 페이지가 pop될 때 초기화
    page.on_view_pop = lambda _: update_content(0)

    # 뷰 정의
    view = ft.View(
        "/favorites",
        controls=[
            ft.Column(
                [
                    # 상단 제목 및 뒤로가기
                    ft.Container(
                        padding=ft.Padding(top=40, left=10, right=10, bottom=10),
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Text("즐 겨 찾 기", size=20),
                                    expand=True,
                                ),
                                ft.Container(
                                    alignment=ft.alignment.center_left,
                                    content=ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK,
                                        on_click=lambda _: page.go("/home")
                                    ),
                                )
                            ],
                            height=50
                        )
                    ),

                    # 탭 버튼 영역
                    ft.Container(
                        padding=ft.Padding(top=0, bottom=0, left=10, right=10),
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    ref=store_box,
                                    expand=1,
                                    height=40,
                                    bgcolor=ft.Colors.GREEN_400,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    content=ft.Text("매장", size=16, color=ft.Colors.WHITE),
                                    on_click=lambda _: update_content(0),
                                ),
                                ft.Container(
                                    ref=food_box,
                                    expand=1,
                                    height=40,
                                    bgcolor=ft.Colors.GREY_300,
                                    alignment=ft.alignment.center,
                                    border_radius=10,
                                    content=ft.Text("음식", size=16, color=ft.Colors.WHITE),
                                    on_click=lambda _: update_content(1),
                                ),
                            ],
                            spacing=10
                        )
                    ),

                    # 콘텐츠 영역
                    ft.Container(ref=content_area),

                    # 여백
                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),

            # 하단 네비게이션 바
            nav_bar(page, current_route="/favorites")
        ]
    )

    # 초기 콘텐츠 로딩
    on_load()

    return view
