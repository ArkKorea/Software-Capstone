import flet as ft
import httpx
import base64
import app_state
from config import BASE_URL

def get_auth_headers():
    return {"Authorization": f"Bearer " + app_state.access_token}

def fetch_my_products():
    try:
        with httpx.Client() as client:
            res = client.post(f"{BASE_URL}/api/product/list", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json()
    except Exception as e:
        print("상품 불러오기 실패:", e)
    return []

def group_register_screen(page: ft.Page):
    picked_file = None
    product_data = []
    filtered_products = []
    selected_product_ids = set()
    checkbox_refs = []

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    picked_file_text = ft.Text("", size=12)
    image_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)
    group_name_field = ft.TextField(
        hint_text="제품명",
        border_color=ft.Colors.TRANSPARENT,
        border_radius=10,
        filled=True,
        fill_color=ft.Colors.GREY_100
    )
    group_name_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)
    product_error_text = ft.Text("필수 체크 항목입니다.", color=ft.Colors.RED, size=14, visible=False)

    product_list_container = ft.Ref[ft.Container]()
    search_field = ft.Ref[ft.TextField]()

    def on_file_picked(e: ft.FilePickerResultEvent):
        nonlocal picked_file
        if e.files:
            picked_file = e.files[0]
            picked_file_text.value = f"선택한 파일: {picked_file.name}"
            image_error_text.visible = False
        else:
            picked_file = None
            picked_file_text.value = "파일이 선택되지 않았습니다."
        page.update()

    file_picker.on_result = on_file_picked

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False)

    def on_checkbox_change(e, pid):
        if e.control.value:
            selected_product_ids.add(pid)
        else:
            selected_product_ids.discard(pid)

    def render_product_list():
        checkbox_refs.clear()

        # 상단 고정: 선택된 항목 + 검색에 포함된 것만
        selected_controls = []
        unselected_controls = []

        for p in filtered_products:
            cb = ft.Checkbox(
                value=p["product_id"] in selected_product_ids,
                on_change=lambda e, pid=p["product_id"]: on_checkbox_change(e, pid)
            )
            checkbox_refs.append(cb)
            tile = ft.ListTile(
                leading=ft.CircleAvatar(content=ft.Text(p["name"][0]), bgcolor=ft.Colors.GREEN),
                title=ft.Text(p["name"]),
                trailing=cb
            )
            if p["product_id"] in selected_product_ids:
                selected_controls.append(tile)
            else:
                unselected_controls.append(tile)

        product_list_container.current.content = ft.Column(
            controls=selected_controls + unselected_controls,
            scroll=ft.ScrollMode.ALWAYS
        )
        page.update()

    def apply_search_filter(e=None):
        nonlocal filtered_products
        keyword = search_field.current.value.strip().lower()
        filtered_products = [
            p for p in product_data if keyword in p["name"].lower()
        ]
        render_product_list()

    def save_clicked(e):
        has_error = False

        group_name = group_name_field.value.strip()
        if not group_name:
            group_name_error_text.visible = True
            has_error = True
        else:
            group_name_error_text.visible = False

        if not selected_product_ids:
            product_error_text.visible = True
            has_error = True
        else:
            product_error_text.visible = False

        if not picked_file:
            image_error_text.visible = True
            has_error = True
        else:
            image_error_text.visible = False

        page.update()
        if has_error:
            print("❌ 유효성 검사 실패")
            return

        try:
            with open(picked_file.path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
        except Exception as err:
            image_error_text.value = f"이미지 처리 실패: {err}"
            image_error_text.visible = True
            page.update()
            return

        payload = {
            "name": group_name,
            "image_base64": image_base64,
            "product_ids": list(selected_product_ids)
        }

        print("📤 전송 데이터:", payload)

        try:
            with httpx.Client() as client:
                res = client.post(f"{BASE_URL}/api/bundles/create", json=payload, headers=get_auth_headers())
                if res.status_code == 200:
                    print("✅ 그룹 생성 성공")
                    page.go("/groupregistersuccess")
                else:
                    print("❌ 그룹 생성 실패:", res.status_code, res.text)
        except Exception as err:
            print("❌ 서버 요청 에러:", err)

    def go_back(e):
        page.go("/myproductgroup")

    def load_products():
        nonlocal product_data
        product_data = fetch_my_products()
        apply_search_filter()  # 필터링 및 초기 렌더링 포함

    search_field_box = ft.TextField(
        ref=search_field,
        hint_text="상품명 검색",
        prefix_icon=ft.Icons.SEARCH,
        on_change=apply_search_filter,
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(10, 10, 10, 10),
    )

    view = ft.View(
        "/groupregister",
        controls=[
            ft.AppBar(
                title=ft.Text("그 룹   추 가", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back),
                actions=[
                    ft.Container(
                        margin=ft.Margin(0, 0, 10, 0),
                        content=ft.TextButton(
                            "저장",
                            on_click=save_clicked,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
                        )
                    )
                ]
            ),
            ft.Container(
                expand=True,
                padding=ft.Padding(left=20, right=20, top=10, bottom=20),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("STEP 1", size=19, color=ft.Colors.GREEN),
                                ft.Text("  그룹명 입력", size=19, color=ft.Colors.BLACK)
                            ]
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.GREY_100,
                            border_radius=10,
                            padding=ft.Padding(10, 14, 10, 14),
                            margin=ft.Margin(0, 5, 0, 5),
                            content=group_name_field
                        ),
                        group_name_error_text,

                        ft.Row(
                            controls=[
                                ft.Text("STEP 2", size=19, color=ft.Colors.GREEN),
                                ft.Text("  상품 선택", size=19, color=ft.Colors.BLACK)
                            ]
                        ),
                        ft.Container(
                            margin=ft.Margin(0, 5, 0, 0),
                            padding=ft.Padding(10, 10, 10, 10),
                            border=ft.Border(
                                top=ft.BorderSide(2, ft.Colors.GREEN),
                                right=ft.BorderSide(2, ft.Colors.GREEN),
                                bottom=ft.BorderSide(2, ft.Colors.GREEN),
                                left=ft.BorderSide(2, ft.Colors.GREEN)
                            ),
                            border_radius=10,
                            content=ft.Column(
                                controls=[
                                    search_field_box,
                                    ft.Container(ref=product_list_container, height=250)
                                ]
                            )
                        ),
                        product_error_text,

                        ft.Container(
                            margin=ft.Margin(0, 20, 0, 10),
                            content=ft.Row(
                                controls=[
                                    ft.Text("STEP 3", size=19, color=ft.Colors.GREEN),
                                    ft.Text("  대표 이미지 업로드", size=19, color=ft.Colors.BLACK)
                                ]
                            )
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.ElevatedButton(
                                    "파일 선택",
                                    icon=ft.Icons.UPLOAD_FILE,
                                    on_click=pick_file
                                ),
                                picked_file_text
                            ]
                        ),
                        image_error_text
                    ],
                    scroll=ft.ScrollMode.HIDDEN
                )
            )
        ]
    )

    load_products()
    return view
