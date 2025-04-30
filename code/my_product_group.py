import flet as ft
from nav_bar import nav_bar

def my_product_group_screen(page: ft.Page):
    selected_sort_option = ft.Text("정렬", size=14, color=ft.colors.GREEN)

    def on_sort_change(e):
        selected_sort_option.value = e.control.text
        page.update()

    return ft.View(
        "/myproductgroup",
        controls=[
            # AppBar 스타일 적용 (중앙 정렬 제목 + 뒤로가기)
            ft.AppBar(
                title=ft.Text("그 룹   관 리", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/productmanagement")
                )
            ),

            ft.Column(
                controls=[
                    # 검색창
                    ft.Container(
                        padding=ft.Padding(top=0, left=20, right=20, bottom=10),
                        content=ft.TextField(
                            hint_text="검색",
                            prefix_icon=ft.Icons.SEARCH,
                            filled=True,
                            fill_color=ft.Colors.GREY_100,
                            border_radius=15,
                            border_color=ft.Colors.TRANSPARENT
                        )
                    ),

                    # 정렬 & 추가하기 버튼
                    ft.Container(
                        padding=ft.Padding(top=0, left=20, right=20, bottom=10),
                        content=ft.Row(
                            controls=[
                                # 정렬 버튼
                                ft.Container(
                                    width=105,
                                    height=40,
                                    border=ft.border.all(width=1, color=ft.colors.GREEN),
                                    border_radius=ft.border_radius.all(12),
                                    bgcolor=ft.colors.WHITE,
                                    alignment=ft.alignment.center,
                                    content=ft.PopupMenuButton(
                                        items=[
                                            ft.PopupMenuItem(text="이름순", on_click=on_sort_change),
                                            ft.PopupMenuItem(text="생성순", on_click=on_sort_change)
                                        ],
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=4,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Icon(name=ft.icons.UNFOLD_MORE, size=18, color=ft.colors.GREEN),
                                                selected_sort_option,
                                                ft.Icon(name=ft.icons.KEYBOARD_ARROW_DOWN, size=18, color=ft.colors.GREY_400),
                                            ]
                                        )
                                    )
                                ),

                                ft.Container(expand=True),

                                # 추가하기 버튼
                                ft.ElevatedButton(
                                    text="추가하기",
                                    icon=ft.Icons.ADD,
                                    on_click=lambda _: page.go("/groupregister"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.GREEN,
                                        bgcolor=ft.Colors.WHITE,
                                        side=ft.BorderSide(1, ft.Colors.GREEN),
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.Padding(10, 5, 10, 5)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START
                        )
                    ),

                    # 그룹 없음 표시
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.Padding(top=20, left=20, right=20, bottom=20),
                        content=ft.Text("그룹이 없습니다.", size=18, color=ft.Colors.GREY)
                    ),

                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
            nav_bar(page, current_route="/myproductgroup")
        ]
    )
