import re
import flet as ft

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def check_consecutive_chars(pw):
    return any(pw[i] == pw[i+1] == pw[i+2] for i in range(len(pw) - 2)) or \
           any(ord(pw[i])+1 == ord(pw[i+1]) and ord(pw[i+1])+1 == ord(pw[i+2]) for i in range(len(pw) - 2))

def is_valid_password(password, email):
    if not 8 <= len(password) <= 12:
        return "8자리 이상 12자리 이하로 설정해주세요."
    if check_consecutive_chars(password):
        return "연속된 문자를 포함할 수 없습니다."
    if email and email.split("@")[0] in password:
        return "이메일과 동일한 비밀번호는 사용할 수 없습니다."
    count = sum(bool(re.search(p, password)) for p in [r"[A-Za-z]", r"\d", r"[!@#$%^&*(),.?\":{}|<>]"])
    if count < 2:
        return "비밀번호 조합이 맞지 않습니다."
    return ""

def is_valid_birth(birth):
    try:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", birth):
            return False
        year, month, day = map(int, birth.split("-"))
        return 1 <= month <= 12 and 1 <= day <= 31
    except:
        return False

def signup_screen(page: ft.Page):
    def update_register_button():
        is_ready = (
            is_valid_email(email.value) and
            is_valid_password(password.value, email.value) == "" and
            password.value == confirm_password.value and
            is_valid_birth(birth.value) and
            terms_1.value and terms_2.value and terms_3.value
        )
        register_button.bgcolor = ft.Colors.GREEN if is_ready else "#C3E8D3"
        register_button.disabled = not is_ready
        page.update()

    def back_to_login(e):
        page.go("/login")

    def close_dialog(e):
        dialog_modal.open = False
        page.update()

    def show_password_info(e):
        dialog_modal.title = ft.Text(
            "비밀번호",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        dialog_modal.content = ft.Text(
            spans=[
                ft.TextSpan(
                    text="비밀번호는 영문자, 숫자, 특수문자 중 최소 2가지 이상 조합하여 8~12자리로 설정 가능합니다.\n연속 혹은 반복된 문자 금지 / 이메일 중복 문자 금지"
                )
            ],
            text_align=ft.TextAlign.CENTER
        )
        dialog_modal.actions = [ft.TextButton("확인", on_click=close_dialog)]
        dialog_modal.open = True
        page.update()

    def validate_email(e=None):
        if email.value.strip() == "":
            email_warning.visible = False
        else:
            email_warning.visible = not is_valid_email(email.value)
        update_register_button()

    def validate_password(e=None):
        if password.value.strip() == "":
            password_warning.value = ""
            password_warning.visible = False
        else:
            result = is_valid_password(password.value, email.value)
            password_warning.value = result
            password_warning.visible = bool(result)
        update_register_button()

    def validate_password_match(e=None):
        if confirm_password.value.strip() == "":
            password_match_warning.visible = False
        else:
            password_match_warning.visible = confirm_password.value != password.value
        update_register_button()

    def validate_birth(e=None):
        if birth.value.strip() == "":
            birth_warning.visible = False
        else:
            birth_warning.visible = not is_valid_birth(birth.value)
        update_register_button()

    def go_to_verification(e):
        update_register_button()
        if not register_button.disabled:
            page.go(f"/email_verification_sent?email={email.value}")

    def terms_all_changed(e):
        terms_1.value = terms_all.value
        terms_2.value = terms_all.value
        terms_3.value = terms_all.value
        update_register_button()

    def update_terms_all_state(e):
        terms_all.value = terms_1.value and terms_2.value and terms_3.value
        update_register_button()

    dialog_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("알림"),
        content=ft.Text("내용 없음"),
        actions=[ft.TextButton("닫기", on_click=close_dialog)],
        actions_alignment=ft.MainAxisAlignment.END,
        open=False
    )

    email = ft.TextField(
        hint_text="이메일을 입력하세요.",
        on_change=validate_email,
        width=page.width * 0.9,
        height=50,
        border_radius=10
    )
    email_warning = ft.Text("이메일 형식이 올바르지 않습니다.", size=12, color=ft.Colors.RED, visible=False)

    password = ft.TextField(
        hint_text="비밀번호 입력",
        password=True,
        on_change=validate_password,
        width=page.width * 0.9,
        height=50,
        border_radius=10,
        suffix=ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.INFO_OUTLINE,
                on_click=show_password_info
            )
        )
    )

    password_warning = ft.Text("", size=12, color=ft.Colors.RED, visible=False)

    confirm_password = ft.TextField(
        hint_text="비밀번호 확인",
        password=True,
        on_change=validate_password_match,
        width=page.width * 0.9,
        height=50,
        border_radius=10
    )
    password_match_warning = ft.Text("비밀번호가 일치하지 않습니다.", size=12, color=ft.Colors.RED, visible=False)

    birth = ft.TextField(
        hint_text="YYYY-MM-DD",
        on_change=validate_birth,
        width=page.width * 0.9,
        height=50,
        border_radius=10
    )
    birth_warning = ft.Text("1997-03-12와 같은 형식으로 입력해주세요.", size=12, color=ft.Colors.RED, visible=False)

    gender_toggle = ft.SegmentedButton(
        segments=[
            ft.Segment(value="female", label=ft.Text("여성")),
            ft.Segment(value="male", label=ft.Text("남성"))
        ],
        selected=["female"],
        allow_multiple_selection=False,
        width=page.width * 0.9
    )

    terms_all = ft.Checkbox(label="필수약관 모두 동의", on_change=terms_all_changed)
    terms_1 = ft.Checkbox(label="(필수) 이용약관", on_change=update_terms_all_state)
    terms_2 = ft.Checkbox(label="(필수) 개인정보 수집 및 이용에 대한 동의", on_change=update_terms_all_state)
    terms_3 = ft.Checkbox(label="(필수) 알레르기 정보 제공 및 면책 조항", on_change=update_terms_all_state)

    terms_1_row = ft.Row([terms_1, ft.TextButton("보기", on_click=lambda e: page.go("/terms_1"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    terms_2_row = ft.Row([terms_2, ft.TextButton("보기", on_click=lambda e: page.go("/terms_2"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    terms_3_row = ft.Row([terms_3, ft.TextButton("보기", on_click=lambda e: page.go("/terms_3"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    register_button = ft.ElevatedButton(
        text="다 음",
        bgcolor="#C3E8D3",
        color=ft.Colors.WHITE,
        width=page.width * 0.9,
        height=50,
        disabled=True,
        on_click=go_to_verification
    )

    return ft.View(
        "/signup",
        controls=[
            dialog_modal,
            ft.AppBar(title=ft.Text("회원가입"), leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=back_to_login), bgcolor=ft.Colors.WHITE),
            ft.Column(
                [
                    email,
                    email_warning,
                    password,
                    password_warning,
                    confirm_password,
                    password_match_warning,
                    birth,
                    birth_warning,
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
