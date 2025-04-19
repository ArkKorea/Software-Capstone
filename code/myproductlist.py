import flet as ft
from nav_bar import nav_bar  # 네비게이션 바

def my_product_list_screen(page: ft.Page):
    return ft.View(
        "/myproductlist",
        controls=[
            ft.Column(
                controls=[
                    # 상단 타이틀
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=50, bottom=10),
                        content=ft.Text(
                            "상  품   목  록",
                            size=24,
                            weight=ft.FontWeight.NORMAL,  # 굵게 효과 없앰
                            text_align=ft.TextAlign.CENTER
                        )
                    ),

                    # 가로 라인
                    ft.Divider(thickness=1, height=1, color=ft.colors.GREY_300),  # 색상 수정

                    # 상품 목록 리스트 (스크롤 가능)
                    ft.Container(
                        expand=True,
                        content=ft.ListView(
                            controls=[
                                # DB 연동 후 동적으로 추가될 항목들
                                # product_list_item("아이스 아메리카노", "https://via.placeholder.com/100"),
                                # product_list_item("바닐라 라떼", "https://via.placeholder.com/100"),
                                # product_list_item("카라멜 마끼아또", "https://via.placeholder.com/100"),
                                # product_list_item("딸기 스무디", "https://via.placeholder.com/100")
                            ],
                            spacing=15,
                            padding=ft.Padding(20, 20, 20, 80),
                            auto_scroll=False
                        )
                    )
                ],
                expand=True
            ),

            # 하단 네비게이션 바
            nav_bar(page, current_route="/myproductlist")
        ]
    )

def product_list_item(name, image_url):
    return ft.Container(
        height=90,
        border_radius=10,
        bgcolor=ft.colors.GREY_100,  # 색상 수정
        padding=10,
        content=ft.Row(
            controls=[
                ft.Image(src=image_url, width=70, height=70),
                ft.Container(width=20),
                ft.Text(name, size=18, weight=ft.FontWeight.NORMAL)  # 굵게 효과 없앰
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )
