# email_verified.py
import flet as ft

def email_verified_screen(page: ft.Page, email: str):
    def go_login(e):
        page.go("/login")

    def go_back(e):
        page.go("/signup")

    return ft.View(
        "/email_verified",
        controls=[
            ft.AppBar(
                title=ft.Text("회원가입"),
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.WHITE
            ),
            ft.Column(
                [
                    ft.Text(f"{email}으로\n인증이 완료되었습니다.", size=18, weight="bold"),
                    ft.TextButton("로그인하러가기", on_click=go_login, style=ft.ButtonStyle(color=ft.colors.GREEN))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ]
    )
