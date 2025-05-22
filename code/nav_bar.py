import flet as ft

def nav_bar(page: ft.Page, current_route: str):
    def is_selected(route):
        return current_route == route

    def nav_icon(icon, label, route):
        selected = is_selected(route)
        color = ft.Colors.GREEN if selected else ft.Colors.BLUE_GREY
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route),
            content=ft.Column(
                [
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(label, size=11, color=color)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    # ✅ 파일 선택기 등록
    file_picker = ft.FilePicker()
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)
    if file_picker not in page.controls:
        page.controls.append(file_picker)

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            print("✅ 선택된 파일:", e.files[0].name)
        else:
            print("❌ 파일 선택 취소됨")
    file_picker.on_result = on_file_result

    # ✅ 카메라 호출용 Dummy Control
    camera_invoker = ft.Container(visible=False)
    page.controls.append(camera_invoker)

    def open_camera():
        print("📸 카메라 호출 시도")
        page.invoke_method("flet/camera", "openCamera")

    # ✅ 팝업 핸들러 정의
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
        open_camera()

    # ✅ 팝업 다이얼로그 UI 정의
    def build_popup():
        return ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("어디서 사진을 가져올까", weight="bold", size=16),
                    ft.Text("골라줘", size=12, color=ft.Colors.GREY),
                    ft.Divider(),
                    ft.TextButton("사진앨범", on_click=pick_from_gallery, style=ft.ButtonStyle(color=ft.Colors.BLUE)),
                    ft.TextButton("카메라", on_click=pick_from_camera, style=ft.ButtonStyle(color=ft.Colors.BLUE)),
                    ft.Container(height=10),
                    ft.TextButton("취소", on_click=close_dialog, style=ft.ButtonStyle(color=ft.Colors.BLUE)),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            shape=ft.RoundedRectangleBorder(radius=20),
            inset_padding=20
        )

    popup_dialog = build_popup()
    if popup_dialog not in page.overlay:
        page.overlay.append(popup_dialog)
    if popup_dialog not in page.controls:
        page.controls.append(popup_dialog)

    def open_camera_album_popup(e=None):
        popup_dialog.open = True
        page.dialog = popup_dialog
        page.update()

    # ✅ 하단 네비게이션 바 반환
    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=ft.Padding(8, 8, 8, 8),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nav_icon(ft.Icons.HOME, "Home", "/home"),
                nav_icon(ft.Icons.SEARCH, "Search", "/searchview"),
                ft.Container(
                    content=ft.FloatingActionButton(
                        icon=ft.Icons.QR_CODE_SCANNER,
                        bgcolor=ft.Colors.GREEN,
                        mini=True,
                        height=40,
                        width=40,
                        on_click=open_camera_album_popup
                    ),
                    margin=ft.Margin(0, -10, 0, 0)
                ),
                nav_icon(ft.Icons.HISTORY, "History", "/history"),
                nav_icon(ft.Icons.PERSON_OUTLINE, "Profile", "/profileview")
            ]
        ),
        border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0),
        height=65
    )
