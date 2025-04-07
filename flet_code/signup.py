import flet as ft

def signup_screen(page: ft.Page):
    def back_to_login(e):
        page.go("/login")

    email = ft.TextField(hint_text="이메일을 입력하세요.", width=page.width * 0.9, border_radius=10)
    password = ft.TextField(hint_text="비밀번호 입력", password=True, width=page.width * 0.9, border_radius=10)
    confirm_password = ft.TextField(hint_text="비밀번호 확인", password=True, width=page.width * 0.9, border_radius=10)
    birth = ft.TextField(hint_text="YYYY-MM-DD", width=page.width * 0.9, border_radius=10)

    gender_toggle = ft.SegmentedButton(
    segments=[
        ft.Segment(value="female", label=ft.Text("여성")),
        ft.Segment(value="male", label=ft.Text("남성"))
    ],
    selected=["female"],
    allow_multiple_selection=False,
    width=page.width * 0.9
)



    terms_all = ft.Checkbox(label="필수약관 모두 동의")
    terms_1 = ft.Checkbox(label="(필수) Allert Sign 이용약관")
    terms_2 = ft.Checkbox(label="(필수) Allert Sign 개인정보 수집 및 이용에 대한 동의")
    terms_3 = ft.Checkbox(label="(필수) Allert Sign 위치기반 서비스 이용 동의")

    register_button = ft.ElevatedButton(
        text="다 음",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=page.width * 0.9,
        height=50
    )

    return ft.View(
        "/signup",
        controls=[
            ft.AppBar(
                title=ft.Text("회원가입"),
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_to_login),
                bgcolor=ft.Colors.WHITE
            ),
            ft.Column(
                [
                    email,
                    password,
                    confirm_password,
                    birth,
                    gender_toggle,
                    ft.Text("ALLERT SIGN", size=14, weight="bold", color=ft.Colors.GREEN),
                    ft.Text("약관동의가 필요해요.", size=16, weight="bold"),
                    terms_all,
                    ft.Container(content=terms_1, padding=ft.padding.only(left=20)),
                    ft.Container(content=terms_2, padding=ft.padding.only(left=20)),
                    ft.Container(content=terms_3, padding=ft.padding.only(left=20)),
                    ft.Container(height=30),
                    register_button
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )
