import flet as ft
from nav_bar import nav_bar  # 네비게이션 바 불러오기

def product_management_screen(page: ft.Page):
    return ft.View(
        "/productmanagement",
        controls=[
            ft.Column(
                controls=[
                    # 상단 텍스트
                    ft.Container(
                        padding=ft.Padding(top=50, left=20, right=20, bottom=10),
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            "내    상 품 관 리",
                            size=24,
                            weight=ft.FontWeight.NORMAL,
                            text_align=ft.TextAlign.CENTER
                        )
                    ),

                    # 이미지 1개 (간격 없음)
                    ft.Container(
                        padding=ft.Padding(top=0, left=20, right=20, bottom=0),
                        content=ft.Row(
                            controls=[
                                ft.Image(
                                    src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/productmanagement/home_productmanagement_image.png",
                                    width=page.width * 0.9
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=0
                        )
                    ),

                    # 연두색 박스
                    ft.Container(
                        bgcolor=ft.Colors.LIGHT_GREEN_100,
                        border_radius=20,
                        padding=ft.Padding(0, 0, 0, 0),
                        margin=ft.margin.only(left=0, right=0, top=-80),  # 더 위로 올림
                        content=ft.Container(
                            padding=ft.Padding(top=20, left=20, right=20, bottom=60),  # 하단 여백 추가
                            content=ft.Column(
                                controls=[
                                    # 상품 등록 텍스트
                                    ft.Text("상품 등록", size=25, weight=ft.FontWeight.BOLD),

                                    product_card(
                                        "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/productmanagement/home_productmanagement_add.png",
                                        "상품 등록하기",
                                        width_ratio=0.95,
                                        height_multiplier=1.2,
                                        on_click=lambda e: page.go("/productregister")
                                    ),

                                    ft.Container(height=10),

                                    # 상품 관리 텍스트
                                    ft.Text("상품 관리", size=25, weight=ft.FontWeight.BOLD),

                                    ft.Row(
                                        controls=[
                                            product_card(
                                                "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/productmanagement/home_productmanagement_list.png",
                                                "내 상품 목록",
                                                width_ratio=0.45,
                                                height_multiplier=1.2,
                                                on_click=lambda e: page.go("/myproductlist")
                                            ),
                                            product_card(
                                                "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/productmanagement/home_productmanagement_group.png",
                                                "내 상품 그룹",
                                                width_ratio=0.45,
                                                height_multiplier=1.2
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    )
                                ],
                                spacing=20
                            )
                        )
                    ),

                    ft.Container(height=70)  # 네비게이션 바 높이 확보용 여백
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),

            # 하단 네비게이션 바 추가
            nav_bar(page, current_route="/productmanagement")
        ]
    )


def product_card(image_link, text, width_ratio=1.0, height_multiplier=1.0, on_click=None):
    card_height = 100 * height_multiplier
    card_width = 360 * width_ratio if width_ratio < 1.0 else None
    return ft.Container(
        width=card_width or 340,
        height=card_height,
        bgcolor=ft.Colors.GREEN,
        border_radius=15,
        padding=ft.Padding(20, 10, 20, 10),
        on_click=on_click,
        content=ft.Column(
            controls=[
                ft.Image(src=image_link, width=50, height=50),
                ft.Text(
                    text,
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.LEFT
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
    )
