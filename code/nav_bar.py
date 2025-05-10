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

    # FilePicker 생성
    file_picker = ft.FilePicker(
        on_result=lambda e: print("Selected:", e.files[0].name) if e.files else print("Cancelled")
    )
    page.overlay.append(file_picker)

    def open_camera(e):
        file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
            dialog_title="카메라 또는 이미지 선택"
        )

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
                        on_click=open_camera
                    ),
                    margin=ft.Margin(0, -10, 0, 0)  # ✅ 수정된 부분
                ),

                nav_icon(ft.Icons.HISTORY, "History", "/history"),
                nav_icon(ft.Icons.PERSON_OUTLINE, "Profile", "/profileview")
            ]
        ),
        border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0),
        height=65
    )
