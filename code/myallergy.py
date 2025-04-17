import flet as ft
from nav_bar import nav_bar

def my_allergy_screen(page: ft.Page):
    allergy_items = [
        ("home_myallergy_crab", "게"), ("home_myallergy_shrimp", "새우"), ("home_myallergy_fish", "고등어"),
        ("home_myallergy_beef", "소고기"), ("home_myallergy_pork", "돼지고기"), ("home_myallergy_chicken", "닭고기"),
        ("home_myallergy_abalone", "조개류"), ("home_myallergy_cashew", "땅콩"), ("home_myallergy_walnut", "호두"),
        ("home_myallergy_peach", "복숭아"), ("home_myallergy_tomato", "토마토"), ("home_myallergy_nuts", "메밀"),
        ("home_myallergy_wheat", "밀"), ("home_myallergy_sesame", "잣"), ("home_myallergy_sulfurousacid", "아황산류"),
        ("home_myallergy_egg", "난류"), ("home_myallergy_squid", "오징어"), ("home_myallergy_milk", "우유"),
        ("home_myallergy_soybean", "대두")
    ]

    def create_allergy_button(image_id, label):
        return ft.Container(
            bgcolor=ft.colors.GREEN_100,
            border_radius=6,
            padding=ft.padding.only(left=4, right=10),
            width=125,
            height=40,
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src=f"https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/{image_id}.png",
                            width=42,  # 이미지 크기 크게!
                            height=42,
                            fit=ft.ImageFit.FILL
                        ),
                        alignment=ft.alignment.center_left
                    ),
                    ft.Container(
                        content=ft.Text(label, size=17, text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2  # 간격 더 줄임!
            )
        )

    allergy_grid = []
    for i in range(0, len(allergy_items), 3):
        row_items = allergy_items[i:i+3]
        row = ft.Row(
            controls=[create_allergy_button(*item) for item in row_items],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY if len(row_items) == 3 else ft.MainAxisAlignment.START
        )
        allergy_grid.append(row)

    return ft.View(
        "/myallergy",
        controls=[
            ft.Column(
                controls=[
                    ft.Container(height=40),

                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("내   알 레 르 기", size=20, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text("홍  길  동  님", size=18, text_align=ft.TextAlign.CENTER),
                                ft.Text("알  레  르  기   :   N  개", size=18, text_align=ft.TextAlign.CENTER),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        ),
                        alignment=ft.alignment.center
                    ),

                    ft.Container(height=20),

                    ft.Column(
                        controls=allergy_grid,
                        spacing=20
                    ),

                    ft.Container(height=30),

                    ft.Container(
                        content=ft.ElevatedButton(
                            "저  장",
                            bgcolor=ft.colors.GREEN,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(20, 8, 20, 8),  # 높이 줄임
                                shape=ft.RoundedRectangleBorder(radius=6),
                                text_style=ft.TextStyle(size=18)
                            ),
                            width=130
                        ),
                        alignment=ft.alignment.center
                    ),

                    ft.Container(height=70)
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            nav_bar(page, current_route="/myallergy")
        ]
    )
