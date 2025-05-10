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

    selected_allergies = set()
    file_path = ft.Text("")

    name_field = ft.TextField(label="제품명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)
    supplier_field = ft.TextField(label="공급자명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)
    ingredient_field = ft.TextField(label="전체 성분", multiline=True, min_lines=3, border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)

    # 오류 메시지 텍스트
    name_error = ft.Text("", color=ft.Colors.RED)
    supplier_error = ft.Text("", color=ft.Colors.RED)
    allergy_error = ft.Text("", color=ft.Colors.RED)
    ingredient_error = ft.Text("", color=ft.Colors.RED)
    file_error = ft.Text("", color=ft.Colors.RED)

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def build_allergy_chip(label, img_src):
        selected = False

        container = ft.Container(
            width=80,
            bgcolor=ft.Colors.LIGHT_GREEN_100,
            border_radius=12,
            padding=ft.Padding(6, 6, 6, 6),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Image(src=img_src, width=24, height=24),
                    ft.Text(label, size=12, text_align=ft.TextAlign.CENTER)
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

        return ft.GestureDetector(on_tap=toggle_selection, content=container)

    allergy_rows = []
    row = []
    for i, (label, img) in enumerate(allergy_items, 1):
        row.append(build_allergy_chip(label, img))
        if i % 4 == 0 or i == len(allergy_items):
            allergy_rows.append(ft.Row(row, spacing=10))
            row = []

    def handle_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path.value = e.files[0].name
        else:
            file_path.value = ""
        file_path.update()

    file_picker.on_result = handle_file_result

    def validate_and_save(e):
        valid = True

        if not name_field.value:
            name_error.value = "필수 체크 항목입니다."
            valid = False
        else:
            name_error.value = ""

        if not supplier_field.value:
            supplier_error.value = "필수 체크 항목입니다."
            valid = False
        else:
            supplier_error.value = ""

        if not selected_allergies:
            allergy_error.value = "필수 체크 항목입니다."
            valid = False
        else:
            allergy_error.value = ""

        if not ingredient_field.value:
            ingredient_error.value = "필수 체크 항목입니다."
            valid = False
        else:
            ingredient_error.value = ""

        if not file_path.value:
            file_error.value = "필수 체크 항목입니다."
            valid = False
        else:
            file_error.value = ""

        name_error.update()
        supplier_error.update()
        allergy_error.update()
        ingredient_error.update()
        file_error.update()

        if valid:
            print("저장됨:")
            print("제품명:", name_field.value)
            print("공급자명:", supplier_field.value)
            print("알레르기:", selected_allergies)
            print("성분:", ingredient_field.value)
            print("파일:", file_path.value)

            page.go("/productregistersuccess")

    return ft.View(
        "/productregister",
        controls=[
            ft.AppBar(
                title=ft.Text("상 품   등 록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/productmanagement")
                ),
                actions=[
                    ft.Container(
                        margin=ft.Margin(top=0, bottom=0, left=0, right=10),
                        content=ft.TextButton(
                            "저장",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                            on_click=validate_and_save
                        )
                    )
                ]
            ),
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.Padding(left=20, right=20, top=10, bottom=20),
                        expand=True,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            spacing=15,
                            controls=[
                                step_text("STEP 1", "제품명 입력"),
                                name_field,
                                name_error,

                                step_text("STEP 2", "공급자명 입력"),
                                supplier_field,
                                supplier_error,

                                step_text("STEP 3", "알레르기 항목 선택"),
                                *allergy_rows,
                                allergy_error,

                                step_text("STEP 4", "전체 성분 입력"),
                                ingredient_field,
                                ingredient_error,

                                step_text("STEP 5", "대표 이미지 업로드"),
                                ft.ElevatedButton("파일 선택", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                                file_path,
                                file_error
                            ]
                        )
                    ),
                    nav_bar(page, current_route="/productregister")
                ]
            )
        ]
    )

def step_text(step, desc):
    return ft.Row(
        controls=[
            ft.Text(step, size=16, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
            ft.Text(f" {desc}", size=16, color=ft.Colors.BLACK)
        ]
    )
