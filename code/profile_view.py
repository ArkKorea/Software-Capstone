import flet as ft
from nav_bar import nav_bar

def profile_view_screen(page: ft.Page):
    profile_avatar = ft.Ref[ft.Image]()
    file_picker = ft.FilePicker()

    name_text = ft.Ref[ft.Text]()
    name_input = ft.Ref[ft.TextField]()
    name_dialog = ft.AlertDialog()
    
    # 초기 이름 저장 및 로딩
    default_name = page.client_storage.get("display_name") or "홍길동님"

    # 이름 수정 팝업 함수
    def open_name_dialog(e):
        name_input.current.value = name_text.current.value
        name_dialog.open = True
        page.dialog = name_dialog
        page.update()

    def save_name(e):
        new_name = name_input.current.value.strip()
        if new_name:
            name_text.current.value = new_name
            page.client_storage.set("display_name", new_name)
        name_dialog.open = False
        page.update()

    def cancel_dialog(e):
        name_dialog.open = False
        page.update()

    # 팝업 정의
    name_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("이름 수정"),
        content=ft.TextField(ref=name_input, autofocus=True),
        actions=[
            ft.TextButton("취소", on_click=cancel_dialog),
            ft.TextButton("저장", on_click=save_name)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    file_picker.on_result = lambda e: (
        setattr(profile_avatar.current, "src", e.files[0].path),
        page.update()
    ) if e.files else None
    page.overlay.extend([file_picker, name_dialog])

    def handle_logout(e): page.go("/login")
    def go_to_myallergy(e): page.go("/myallergy")
    def go_to_notice(e): page.go("/notice")
    def go_to_terms(e): page.go("/terms")

    return ft.View(
        "/profileview",
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    # 상단 로고
                    ft.Container(
                        alignment=ft.Alignment(0, 0),
                        padding=ft.Padding(top=40, bottom=10, left=0, right=0),
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                            width=180,
                            fit=ft.ImageFit.CONTAIN
                        )
                    ),
                    # 프로필
                    ft.Container(
                        alignment=ft.Alignment(0, 0),
                        padding=ft.Padding(10, 10, 10, 10),
                        content=ft.Column(
                            [
                                ft.GestureDetector(
                                    on_tap=lambda e: file_picker.pick_files(
                                        allow_multiple=False,
                                        allowed_extensions=["png", "jpg", "jpeg"]
                                    ),
                                    content=ft.Container(
                                        width=80,
                                        height=80,
                                        border_radius=40,
                                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                        content=ft.Image(
                                            ref=profile_avatar,
                                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/profile/home_profile_avatar.png",
                                            fit=ft.ImageFit.COVER
                                        )
                                    )
                                ),
                                ft.GestureDetector(
                                    on_tap=open_name_dialog,
                                    content=ft.Text(default_name, ref=name_text, size=20, weight=ft.FontWeight.BOLD)
                                ),
                                ft.Text("@username", size=14, color=ft.Colors.GREY)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        )
                    ),
                    # 메뉴
                    ft.Divider(height=1, thickness=1),
                    *[menu_item(label, handle_logout, go_to_myallergy, go_to_notice, go_to_terms) for label in [
                        "공지사항", "이용 약관", "내 알레르기", "알림 설정",
                        "고객센터", "언어", "회원 탈퇴", "로그아웃"
                    ]],
                    ft.Divider(height=1, thickness=1)
                ]
            ),
            nav_bar(page, current_route="/profileview")
        ]
    )

def menu_item(label, logout_handler=None, myallergy_handler=None, notice_handler=None, terms_handler=None):
    tile = ft.ListTile(
        title=ft.Text(label),
        trailing=ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT),
        dense=True
    )

    handlers = {
        "로그아웃": logout_handler,
        "내 알레르기": myallergy_handler,
        "공지사항": notice_handler,
        "이용 약관": terms_handler
    }

    return ft.GestureDetector(
        on_tap=handlers.get(label, lambda e: None),
        content=ft.Container(content=tile, padding=ft.Padding(10, 0, 10, 0))
    )
