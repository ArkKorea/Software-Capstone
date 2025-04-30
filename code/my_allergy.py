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

    selected_allergies = set()
    allergy_count_text = ft.Text(f"알  레  르  기   :   {len(selected_allergies)}  개", size=18, text_align=ft.TextAlign.CENTER)

    def update_allergy_count():
        allergy_count_text.value = f"알  레  르  기   :   {len(selected_allergies)}  개"
        allergy_count_text.update()

    def create_allergy_button(image_id, label):
        selected = False

        container = ft.Container(
            width=86,
            bgcolor=ft.Colors.LIGHT_GREEN_100,
            border_radius=12,
            padding=ft.padding.symmetric(vertical=8, horizontal=8),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(
                        src=f"https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/{image_id}.png",
                        width=29,
                        height=29
                    ),
                    ft.Text(label, size=14, text_align=ft.TextAlign.CENTER)
                ]
            )
        )

        def toggle_selection(e):
            nonlocal selected
            selected = not selected

            if selected:
                selected_allergies.add(label)
                container.bgcolor = ft.Colors.GREEN_300
            else:
                selected_allergies.discard(label)
                container.bgcolor = ft.Colors.LIGHT_GREEN_100

            container.update()
            update_allergy_count()

        return ft.GestureDetector(
            on_tap=toggle_selection,
            content=container
        )

    allergy_grid = []
    row = []
    row_width = (86 * 4) + (12 * 3)

    for i, (img_id, label) in enumerate(allergy_items, 1):
        row.append(create_allergy_button(img_id, label))
        if i % 4 == 0 or i == len(allergy_items):
            is_last_row = i == len(allergy_items)
            alignment = ft.MainAxisAlignment.START if is_last_row else ft.MainAxisAlignment.CENTER
            allergy_grid.append(
                ft.Container(
                    width=row_width,
                    content=ft.Row(
                        row,
                        spacing=12,
                        alignment=alignment
                    )
                )
            )
            row = []

    return ft.View(
        "/myallergy",
        controls=[
            ft.AppBar(
                title=ft.Text("내   알 레 르 기", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home")
                ),
                actions=[
                    ft.Container(
                        margin=ft.margin.only(right=10),
                        content=ft.TextButton(
                            "저장",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                            on_click=lambda _: print("선택된 알레르기 항목:", selected_allergies)
                        )
                    )
                ]
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=20),

                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("홍  길  동  님", size=18, text_align=ft.TextAlign.CENTER),
                                allergy_count_text,
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
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),

                    ft.Container(height=30),
                ]
            ),
            nav_bar(page, current_route="/myallergy")
        ]
    )
