import flet as ft

def email_verification_sent_screen(page: ft.Page, email: str):
    def go_back(e):
        page.go("/signup")

    def go_login(e):
        page.go("/login")

    return ft.View(
        "/emailverificationsent",
        controls=[
            ft.AppBar(
                title=ft.Text("인 증 메 일 발 송", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back
                )
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("링크를 보냈습니다.", size=16, weight="bold"),
                        ft.Text(
                            f"{email}으로\n인증메일이 발송되었습니다.",
                            size=18,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(
                            width=page.width * 0.95,
                            padding=15,
                            bgcolor=ft.Colors.GREEN_50,
                            border_radius=8,
                            border=ft.Border(
                                top=ft.BorderSide(1, ft.Colors.GREEN),
                                right=ft.BorderSide(1, ft.Colors.GREEN),
                                bottom=ft.BorderSide(1, ft.Colors.GREEN),
                                left=ft.BorderSide(1, ft.Colors.GREEN)
                            ),
                            margin=10,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "메일에 있는 ‘인증하기’버튼 혹은\n링크를 클릭하세요.",
                                        text_align=ft.TextAlign.CENTER
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ),
                        ft.Text(
                            "메일을 받지 못하셨다면 스팸 메일함을 확인해주세요.",
                            size=12,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Icon(name=ft.Icons.HELP_OUTLINE, size=14),
                                ft.Text("인증이 잘 안되시나요?", size=12),
                                ft.TextButton(
                                    "인증 메일 재전송",
                                    on_click=lambda e: None,
                                    style=ft.ButtonStyle(color=ft.Colors.GREEN),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                        ft.ElevatedButton(
                            text="로그인 화면으로 돌아가기",
                            on_click=go_login,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.Padding(10, 15, 10, 15),
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        ]
    )
