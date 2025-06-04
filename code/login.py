import flet as ft
import re  # 이메일 정규식 체크용

import httpx
import asyncio
from config import BASE_URL
import app_state

# 이메일 정규식 검증 함수
def validate_email_format(email):
    return re.match(r"[^@]+@[^@]+\.(com|net)$", email)

# (임시) 로그인 체크 함수 — 이메일만 맞으면 로그인 성공 처리
def check_credentials(email, password):
    return True  # 이메일 형식만 맞으면 무조건 로그인 성공

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

def login_screen(page: ft.Page):
    email_input = ft.TextField(label="이메일 주소", width=page.width * 0.8)
    password_input = ft.TextField(label="비밀번호", password=True, width=page.width * 0.8)

    email_error_text = ft.Container(
        content=ft.Text("이메일 형식이 올바르지 않습니다.", color=ft.Colors.RED, size=14),
        alignment=ft.Alignment(-1, 0),
        width=page.width * 0.8,
        visible=False
    )

    login_error_text = ft.Container(
        content=ft.Text("", color=ft.Colors.RED, size=14),  # 초기 메시지 없음
        alignment=ft.Alignment(-1, 0),
        width=page.width * 0.8,
        visible=False
    )

    def on_login_click(e):
        email = email_input.value.strip()
        password = password_input.value.strip()

        if not validate_email_format(email):
            email_error_text.visible = True
            login_error_text.visible = False
            page.update()
            return

        email_error_text.visible = False
        login_error_text.visible = False
        page.update()

        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{BASE_URL}/api/auth/login",
                    json={"email": email, "password": password},
                    headers={"Content-Type": "application/json"}
                )

            if response.status_code == 200:
                data = response.json()
                app_state.access_token = data["access_token"]
                app_state.user = data["user"]
                page.client_storage.set("display_name", app_state.user.get("email"))
                page.go("/home")
            else:
                try:
                    error_data = response.json()
                    server_message = error_data.get("detail", "로그인에 실패했습니다.")
                    if isinstance(server_message, list):  # FastAPI ValidationError 형태 대응
                        server_message = server_message[0].get("msg", "로그인에 실패했습니다.")
                except Exception:
                    server_message = "로그인에 실패했습니다."

                login_error_text.content = ft.Text(server_message, color=ft.Colors.RED, size=14)
                login_error_text.visible = True
                page.update()

        except Exception as ex:
            print("로그인 요청 중 예외 발생:", ex)
            login_error_text.content = ft.Text("로그인 중 오류가 발생했습니다.", color=ft.Colors.RED, size=14)
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
        on_click=lambda e: page.go("/resetpassword")
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
                    login_error_text,
                    ft.Container(height=10),
                    password_input,
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