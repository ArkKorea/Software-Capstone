import flet as ft
import httpx
import base64
import app_state
from config import BASE_URL

def ocr_screen(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE
    page.overlay.clear()
    page.dialog = None

    input_name = ft.TextField(label="제품 이름", autofocus=False)
    result_column = ft.Column(scroll=True)
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def show_result_popup(product: dict):
        allergens = product.get("allergen_hit", [])
        safe_allergens = product.get("allergen_safe", [])

        popup = ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=20,
                width=350,
                height=580,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                    controls=[
                        ft.Text(product.get("name", "제품명 없음"), size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("알레르기 유발 성분", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(", ".join(allergens) if allergens else "없음", size=14, color=ft.Colors.RED_400),
                        ft.Text("안전 성분", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(", ".join(safe_allergens) if safe_allergens else "정보 없음", size=14, color=ft.Colors.GREEN_400),
                        ft.Text("전체 성분", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text("", size=13),  # 전체 성분 빈칸 출력
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    text="닫기",
                                    on_click=lambda e: (page.overlay.clear(), page.go("/home")),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN,
                                        color=ft.Colors.WHITE,
                                        padding=ft.Padding(40, 10, 40, 10),
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )
        page.overlay.clear()
        page.overlay.append(popup)
        page.update()

    def on_file_pick(e: ft.FilePickerResultEvent):
        if e.files and e.files[0].path:
            file_path = e.files[0].path
            product_name_input = input_name.value.strip() or "이름없음"

            try:
                with open(file_path, "rb") as f:
                    image_bytes = f.read()
                    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                payload = {
                    "product_name": product_name_input,
                    "image_base64": image_base64
                }

                with httpx.Client(timeout=20.0) as client:
                    response = client.post(
                        f"{BASE_URL}/api/product/from-ocr",
                        json=payload,
                        headers={"Authorization": f"Bearer {app_state.access_token}"}
                    )

                if response.status_code == 200:
                    show_result_popup(response.json())
                else:
                    result_column.controls = [ft.Text(f"서버 오류: {response.status_code}", color=ft.Colors.RED)]
            except Exception as ex:
                result_column.controls = [ft.Text(f"예외 발생: {str(ex)}", color=ft.Colors.RED)]
        else:
            result_column.controls = [ft.Text("파일이 유효하지 않습니다.", color=ft.Colors.RED)]

        page.update()

    file_picker.on_result = on_file_pick

    def close_dialog(e=None):
        popup_dialog.open = False
        page.update()

    def pick_from_gallery(e=None):
        close_dialog()
        file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
            dialog_title="앨범에서 이미지 선택"
        )

    def pick_from_camera(e=None):
        close_dialog()
        file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
            camera=True,
            dialog_title="카메라로 촬영"
        )

    def build_popup():
        return ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("어디서 사진을 가져올까요?", weight="bold", size=16),
                    ft.Divider(),
                    ft.TextButton("사진앨범", on_click=pick_from_gallery),
                    ft.TextButton("카메라", on_click=pick_from_camera),
                    ft.Container(height=10),
                    ft.TextButton("취소", on_click=close_dialog),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            shape=ft.RoundedRectangleBorder(radius=20),
            inset_padding=20
        )

    popup_dialog = build_popup()
    page.overlay.append(popup_dialog)

    def show_popup(e=None):
        page.dialog = popup_dialog
        popup_dialog.open = True
        page.update()

    def handle_back(e):
        if popup_dialog.open:
            popup_dialog.open = False
            page.dialog = None
        page.go("/home")

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=handle_back,
        icon_color=ft.Colors.GREEN,
        tooltip="뒤로가기"
    )

    return ft.View(
        "/ocr",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.AppBar(
                title=ft.Text("OCR 분석", color=ft.Colors.BLACK),
                leading=back_button,
                bgcolor=ft.Colors.WHITE
            ),
            ft.Column(
                [
                    input_name,
                    ft.ElevatedButton(
                        "사진 선택 및 업로드",
                        on_click=show_popup,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE
                        )
                    ),
                    result_column
                ],
                scroll=True,
                expand=True
            )
        ]
    )
