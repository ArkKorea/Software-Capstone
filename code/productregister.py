import flet as ft
from nav_bar import nav_bar

def product_register_screen(page: ft.Page):
    allergy_items = [
        ("새우", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_shrimp.png"),
        ("게", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_crab.png"),
        ("오징어", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_squid.png"),
        ("조개류", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_abalone.png"),
        ("소고기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_beef.png"),
        ("돼지고기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_pork.png"),
        ("닭고기", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_chicken.png"),
        ("고등어", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_fish.png"),
        ("땅콩", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_cashew.png"),
        ("호두", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_walnut.png"),
        ("대두", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_soybean.png"),
        ("잣", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_sesame.png"),
        ("밀", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_wheat.png"),
        ("메밀", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_nuts.png"),
        ("복숭아", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_peach.png"),
        ("토마토", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_tomato.png"),
        ("난류", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_egg.png"),
        ("우유", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_milk.png"),
        ("아황산류", "https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/home_myallergy_sulfurousacid.png"),
    ]

    allergy_rows = []
    row = []

    for i, (label, img) in enumerate(allergy_items, 1):
        row.append(allergy_chip(label, img))
        if i % 4 == 0 or i == len(allergy_items):
            allergy_rows.append(ft.Row(row, spacing=10))
            row = []

    return ft.View(
        "/productregister",
        controls=[
            ft.AppBar(
                title=ft.Text("상  품    등  록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                actions=[
                    ft.Container(
                        margin=ft.margin.only(right=10),
                        content=ft.TextButton(
                            "저장",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                        )
                    )
                ]
            ),
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, top=10, bottom=20),
                        expand=True,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            spacing=15,
                            controls=[
                                step_text("STEP 1", "제품명 입력"),
                                ft.TextField(label="제품명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True),

                                step_text("STEP 2", "공급자명 입력"),
                                ft.TextField(label="공급자명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True),

                                step_text("STEP 3", "알레르기 항목 선택"),
                                *allergy_rows,

                                step_text("STEP 4", "전체 성분 입력"),
                                ft.TextField(label="전체 성분", multiline=True, min_lines=3, border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True),

                                step_text("STEP 5", "대표 이미지 업로드"),
                                ft.ElevatedButton("파일 선택", icon=ft.icons.UPLOAD_FILE),
                            ]
                        )
                    ),
                    nav_bar(page, current_route="/productregister")
                ]
            )
        ]
    )

def allergy_chip(label, img_src):
    return ft.Container(
        width=80,
        bgcolor=ft.Colors.LIGHT_GREEN_100,
        border_radius=12,
        padding=ft.padding.symmetric(vertical=6, horizontal=6),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Image(src=img_src, width=24, height=24),
                ft.Text(label, size=12, text_align=ft.TextAlign.CENTER)
            ]
        )
    )

def step_text(step, desc):
    return ft.Row(
        controls=[
            ft.Text(step, size=16, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
            ft.Text(f" {desc}", size=16, color=ft.Colors.BLACK)
        ]
    )
