import flet as ft
import mysql.connector
import re  # 이메일 정규식 체크용

# 이메일 정규식 검증 함수
def validate_email_format(email):
    return re.match(r"[^@]+@[^@]+\.(com|net)$", email)

# MySQL 연결 함수
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # ✅ 본인의 사용자명으로 수정
        password="$tlscjfak9",   # ✅ 본인의 비밀번호로 수정
        database="login_db"
    )

# 로그인 체크 (DB 조회)
def check_credentials(email, password):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"DB 오류: {e}")
        return False

# 스플래시 화면
def splash_content(page: ft.Page):
    logo = ft.Image(
        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/login/login_image.png",
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

# 로그인 화면
def login_screen(page: ft.Page):
    email_input = ft.TextField(label="이메일 주소", width=page.width * 0.8)
    password_input = ft.TextField(label="비밀번호", password=True, width=page.width * 0.8)

    email_error_text = ft.Container(
        content=ft.Text("이메일 형식이 올바르지 않습니다.", color=ft.Colors.RED, size=14),
        alignment=ft.alignment.center_left,
        width=page.width * 0.8,
        visible=False
    )

    login_error_text = ft.Container(
        content=ft.Text("계정이 존재하지 않거나 비밀번호가 올바르지 않습니다.", color=ft.Colors.RED, size=14),
        alignment=ft.alignment.center_left,
        width=page.width * 0.8,
        visible=False
    )

    def on_login_click(e):
        email = email_input.value.strip()
        password = password_input.value.strip()

        if not validate_email_format(email):
            email_error_text.visible = True
            login_error_text.visible = False
        else:
            email_error_text.visible = False
            if check_credentials(email, password):
                login_error_text.visible = False
                page.go("/home")
            else:
                login_error_text.visible = True

        page.update()

    login_button = ft.ElevatedButton(
        text="로그인",
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=page.width * 0.8,
        on_click=on_login_click
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
                    ft.Image(
                        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/login/login_image.png",
                        width=300,
                        height=300
                    ),
                    email_input,
                    email_error_text,
                    ft.Container(height=10),
                    password_input,
                    login_error_text,
                    ft.Container(height=10),
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
