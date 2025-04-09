# email_verification_sent.py
import flet as ft

def email_verification_sent_screen(page: ft.Page, email: str):
    def go_back(e):
        page.go("/signup")

    return ft.View(
        "/email_verification_sent",
        controls=[
            ft.AppBar(
                title=ft.Text("회원가입"),
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.WHITE
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
                            width=page.width * 0.95,  # 가로 길이를 넓게 설정 (95%)
                            padding=15,
                            bgcolor=ft.colors.GREEN_50,
                            border_radius=8,
                            border=ft.border.all(1, ft.colors.GREEN),
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
                                ft.Icon(name=ft.icons.HELP_OUTLINE, size=14),
                                ft.Text("인증이 잘 안되시나요?", size=12),
                                ft.TextButton(
                                    "인증 메일 재전송",
                                    on_click=lambda e: None,
                                    style=ft.ButtonStyle(color=ft.colors.GREEN),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )
        ]
    )
