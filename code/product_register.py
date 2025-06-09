import flet as ft
import app_state
import httpx
import base64
from config import BASE_URL
from nav_bar import nav_bar

def get_auth_headers():
    return {"Authorization": f"Bearer {app_state.access_token}"}

def step_text(step, desc):
    return ft.Row(
        controls=[
            ft.Text(step, size=16, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
            ft.Text(f" {desc}", size=16, color=ft.Colors.BLACK)
        ]
    )

def product_register_screen(page: ft.Page, mode="create", product_data=None):
    is_edit = mode == "edit"

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

    selected_allergies = set(product_data.get("allergen_hit", [])) if is_edit and product_data else set()
    file_path = ft.Text("현재 이미지 유지됩니다" if is_edit else "")
    uploaded_file = None

    def build_allergy_chip(label, img_src):
        selected = label in selected_allergies
        container = ft.Container(
            bgcolor=ft.Colors.GREEN_300 if selected else ft.Colors.LIGHT_GREEN_100,
            border_radius=12,
            padding=6,
            height=80,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
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

    allergy_grid = ft.GridView(
        max_extent=100,
        child_aspect_ratio=1.2,
        spacing=10,
        run_spacing=10,
        controls=[build_allergy_chip(label, img) for label, img in allergy_items],
        expand=False
    )

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def handle_file_result(e: ft.FilePickerResultEvent):
        nonlocal uploaded_file
        if e.files:
            uploaded_file = e.files[0]
            file_path.value = uploaded_file.name
        else:
            uploaded_file = None
            file_path.value = ""
        file_path.update()

    file_picker.on_result = handle_file_result

    name_field = ft.TextField(value=product_data.get("name", "") if is_edit else "", label="제품명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)
    supplier_field = ft.TextField(value=product_data.get("supplier_name", "") if is_edit else "", label="공급자명", border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)
    ingredient_field = ft.TextField(value=product_data.get("ingredient", "") if is_edit else "", label="전체 성분", multiline=True, min_lines=3, border_radius=10, filled=True, fill_color=ft.Colors.GREY_100, dense=True)

    name_error = ft.Text("", color=ft.Colors.RED)
    supplier_error = ft.Text("", color=ft.Colors.RED)
    allergy_error = ft.Text("", color=ft.Colors.RED)
    ingredient_error = ft.Text("", color=ft.Colors.RED)
    file_error = ft.Text("", color=ft.Colors.RED)

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

        image_base64 = None
        if uploaded_file:
            try:
                with open(uploaded_file.path, "rb") as f:
                    raw_bytes = f.read()
                    image_base64 = base64.b64encode(raw_bytes).decode("utf-8")
            except Exception as err:
                file_error.value = f"이미지 인코딩 실패: {err}"
                file_error.update()
                return
        elif not is_edit:
            file_error.value = "필수 체크 항목입니다."
            file_error.update()
            return

        for msg in [name_error, supplier_error, allergy_error, ingredient_error, file_error]:
            msg.update()

        if not valid:
            return

        payload = {
            "name": name_field.value,
            "ingredient": ingredient_field.value,
            "allergies": list(selected_allergies)
        }
        if image_base64:
            payload["image_base64"] = image_base64
        if is_edit:
            payload["product_id"] = product_data["product_id"]

        url = f"{BASE_URL}/api/product/update" if is_edit else f"{BASE_URL}/api/product/create"

        try:
            with httpx.Client() as client:
                res = client.post(url, json=payload, headers=get_auth_headers())
                if res.status_code == 200:
                    product_id = res.json().get("product_id")
                    page.go("/productmanagement") if is_edit else page.go(f"/productregistersuccess?id={product_id}")
                else:
                    file_error.value = f"등록 실패: {res.json()}"
                    file_error.update()
        except Exception as err:
            file_error.value = f"요청 실패: {err}"
            file_error.update()

    return ft.View(
        "/productregister",
        controls=[
            ft.AppBar(
                title=ft.Text("상 품 수 정" if is_edit else "상 품 등 록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/productmanagement")),
                actions=[
                    ft.Container(
                        margin=ft.Margin(left=0, top=0, right=10, bottom=0),
                        content=ft.TextButton("저장", style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE), on_click=validate_and_save)
                    )
                ]
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    ft.Container(
                        padding=ft.Padding(left=20, top=20, right=20, bottom=30),
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                step_text("STEP 1", "제품명 입력"),
                                name_field,
                                name_error,
                                step_text("STEP 2", "공급자명 입력"),
                                supplier_field,
                                supplier_error,
                                step_text("STEP 3", "알레르기 항목 선택"),
                                allergy_grid,
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
