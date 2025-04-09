import flet as ft

def splash_content(page: ft.Page):
    logo = ft.Image(
        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/main/flet_code/login_image.png",
        width=300,
        height=300
    )

    desc = ft.Text(
        "당신의 알러지를 등록하고\n지금부터 관리해보세요!!",
        size=16,
        text_align=ft.TextAlign.CENTER
    )

    return ft.Column(
        [logo, ft.Container(height=10), desc],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

def login_screen(page: ft.Page):
    logo = ft.Image(
        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/main/flet_code/login_image.png",
        width=300,
        height=300
    )

    email_input = ft.TextField(label="이메일 주소", width=page.width * 0.8)
    password_input = ft.TextField(label="비밀번호", password=True, width=page.width * 0.8)

    login_button = ft.ElevatedButton(
        text="로그인",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=page.width * 0.8
    )

    forgot_password = ft.TextButton(
        "비밀번호가 생각나지 않으신가요?",
        on_click=lambda e: page.go("/find-password")
    )

    signup_link = ft.TextButton(
        "회원가입",
        style=ft.ButtonStyle(color=ft.Colors.GREEN),
        on_click=lambda e: page.go("/signup")
    )

    signup_row = ft.Row(
        [ft.Text("Allert Sign이 처음이신가요?"), signup_link],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.View(
        "/login",
        controls=[
            ft.Column(
                [
                    logo,
                    email_input,
                    password_input,
                    login_button,
                    forgot_password,
                    ft.Container(height=30),
                    signup_row
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
