import flet as ft

# 비밀번호 재설정 화면
def reset_password_screen(page: ft.Page):
    email_input = ft.TextField(label="이메일 주소", width=page.width * 0.8)
    reset_error_text = ft.Container(
        content=ft.Text("이메일을 확인해주세요.", color=ft.Colors.RED, size=14),
        alignment=ft.Alignment(-1, 0),
        width=page.width * 0.8,
        visible=False
    )

    # 메일 발송 버튼 클릭 이벤트
    def on_reset_click(e):
        email = email_input.value.strip()

        if not email:
            reset_error_text.visible = True
        else:
            reset_error_text.visible = False
            # 이메일로 비밀번호 재설정 링크 발송 처리를 여기에 추가
            page.go("/login")  # 예시로 로그인 화면으로 이동

        page.update()

    reset_button = ft.ElevatedButton(
        text="메일 발송",  # 버튼 텍스트 변경
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=page.width * 0.4,  # 버튼 좌우 너비 줄임
        on_click=on_reset_click
    )

    return ft.View(
        "/resetpassword",
        controls=[
            ft.AppBar(
                title=ft.Text("비밀번호 재설정", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: page.go("/login")
                )
            ),
            ft.Column(
                [
                    ft.Image(
                        src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/login/login_image.png",  # 이미지 소스는 여기에 넣어주세요
                        width=300,
                        height=300
                    ),
                    # 새로운 문구 추가
                    ft.Text(
                        "계정의 이메일 주소를 입력해주세요.\n비밀번호 재설정 링크가 포함된 메일이\n계정의 이메일 주소로 발송됩니다.",
                        size=16,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    email_input,
                    reset_error_text,
                    ft.Container(height=10),
                    reset_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
