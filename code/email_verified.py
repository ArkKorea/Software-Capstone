# email_verified.py
import flet as ft

def email_verified_screen(page: ft.Page, email: str):
    def go_login(e):
        page.go("/login")

    return ft.View(
        "/emailverified",
        controls=[
            ft.AppBar(
                title=ft.Text("인 증 완 료", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/login")
                )
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    [
                        ft.Text(
                            f"{email}으로\n인증이 완료되었습니다.",
                            size=25,
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.TextButton(
                            content=ft.Text("로그인하러가기", size=25),
                            on_click=go_login,
                            style=ft.ButtonStyle(
                                color=ft.colors.GREEN,
                                padding=10,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        ]
    )
