# signup.py
import re
import flet as ft

def is_valid_password(password):
    if not 8 <= len(password) <= 12:
        return False
    count = 0
    if re.search(r'[A-Za-z]', password):
        count += 1
    if re.search(r'\d', password):
        count += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        count += 1
    return count >= 2

def signup_screen(page: ft.Page):
    def back_to_login(e):
        page.go("/login")

    def go_to_verification(e):
        check_password_validity()
        check_password_match()
        if (
            email.value and
            is_valid_password(password.value) and
            password.value == confirm_password.value and
            terms_1.value and terms_2.value and terms_3.value
        ):
            page.go(f"/email_verification_sent?email={email.value}")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("모든 필수 항목을 확인해주세요."))
            page.snack_bar.open = True
            page.update()

    email = ft.TextField(
        hint_text="이메일을 입력하세요.",
        width=page.width * 0.9,
        border_radius=10
    )

    password_warning = ft.Text(
        "영문자, 숫자, 특수문자 중 최소 2가지 이상 조합하여 8~12자리로 설정 가능합니다",
        size=12,
        color=ft.colors.RED,
        visible=False
    )

    password_match_warning = ft.Text(
        "비밀번호가 일치하지 않습니다.",
        size=12,
        color=ft.colors.RED,
        visible=False
    )

    def check_password_validity(e=None):
        password_warning.visible = not is_valid_password(password.value)
        page.update()

    def check_password_match(e=None):
        password_match_warning.visible = (
            confirm_password.value != "" and password.value != confirm_password.value
        )
        page.update()

    password = ft.TextField(
        hint_text="비밀번호 입력",
        password=True,
        width=page.width * 0.9,
        border_radius=10,
        on_blur=check_password_validity
    )

    confirm_password = ft.TextField(
        hint_text="비밀번호 확인",
        password=True,
        width=page.width * 0.9,
        border_radius=10,
        on_change=check_password_match
    )

    birth = ft.TextField(
        hint_text="YYYY-MM-DD",
        width=page.width * 0.9,
        border_radius=10
    )

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
    terms_1 = ft.Checkbox(label="(필수) 이용약관")
    terms_2 = ft.Checkbox(label="(필수) 개인정보 수집 및 이용에 대한 동의")
    terms_3 = ft.Checkbox(label="(필수) 알레르기 정보 제공 및 면책 조항")

    def terms_all_changed(e):
        terms_1.value = terms_all.value
        terms_2.value = terms_all.value
        terms_3.value = terms_all.value
        page.update()

    def update_terms_all_state(e):
        terms_all.value = terms_1.value and terms_2.value and terms_3.value
        page.update()

    terms_all.on_change = terms_all_changed
    terms_1.on_change = update_terms_all_state
    terms_2.on_change = update_terms_all_state
    terms_3.on_change = update_terms_all_state

    terms_1_row = ft.Row([terms_1, ft.TextButton("보기", on_click=lambda e: page.go("/terms_1"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    terms_2_row = ft.Row([terms_2, ft.TextButton("보기", on_click=lambda e: page.go("/terms_2"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    terms_3_row = ft.Row([terms_3, ft.TextButton("보기", on_click=lambda e: page.go("/terms_3"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    register_button = ft.ElevatedButton(
        text="다 음",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=page.width * 0.9,
        height=50,
        on_click=go_to_verification
    )

    return ft.View(
        "/signup",
        controls=[
            ft.AppBar(title=ft.Text("회원가입"), leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=back_to_login), bgcolor=ft.Colors.WHITE),
            ft.Column(
                [
                    email,
                    password,
                    password_warning,
                    confirm_password,
                    password_match_warning,
                    birth,
                    gender_toggle,
                    ft.Text("ALLERT SIGN", size=14, weight="bold", color=ft.Colors.GREEN),
                    ft.Text("약관동의가 필요해요.", size=16, weight="bold"),
                    terms_all,
                    ft.Container(content=terms_1_row, padding=ft.padding.only(left=20)),
                    ft.Container(content=terms_2_row, padding=ft.padding.only(left=20)),
                    ft.Container(content=terms_3_row, padding=ft.padding.only(left=20)),
                    ft.Container(height=30),
                    register_button
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )
