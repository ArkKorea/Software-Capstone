import flet as ft

def terms_2_screen(page: ft.Page):
    def go_back(e):
        page.go("/signup")

    return ft.View(
        "/terms_2",
        controls=[
            ft.AppBar(
                title=ft.Text("개인정보 수집 및 이용 동의"),
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.WHITE
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            """
< ALLERT SIGN 개인정보 수집 및 이용에 대한 동의 약관 >

Allert Sign(이하 "본 서비스")은 이용자의 개인정보를 보호하며, 관련 법령에 따라 개인정보 수집 및 이용에 대한 동의를 받고자 합니다.

1. 수집하는 개인정보 항목

본 서비스는 다음과 같은 개인정보를 수집합니다.

<필수 수집 항목>
이름, 이메일 주소, 비밀번호, 성별, 생년월일, 알레르기 정보 및 건강 관련 정보 (사용자가 입력한 정보)

<선택 수집 항목>
위치 정보 (알레르기 메뉴 검색 시 활용), 기타 사용자가 추가 입력한 정보

2. 개인정보 수집 및 이용 목적

수집된 개인정보는 다음 목적을 위해 활용됩니다.

- 회원가입 및 서비스 이용 관리
- 회원 가입, 본인 확인 및 인증
- 서비스 제공 및 사용자 맞춤형 정보 제공
- 알레르기 관리 서비스 제공
- 사용자가 입력한 알레르기 정보에 기반한 음식 및 식품 추천
- QR 코드 검색을 통한 매장 메뉴 알레르기 성분 확인
- 서비스 운영 및 개선
- 서비스 이용 분석 및 통계 목적 활용
- 사용자 문의 및 고객 지원

3. 개인정보 보유 및 이용 기간

이용자가 회원 탈퇴 시, 즉시 개인정보를 파기합니다. 단, 법령에서 정한 일정 기간 동안 보관이 필요한 경우 해당 기간 동안 보관 후 파기합니다.

4. 동의 거부 권리 및 불이익 안내

이용자는 개인정보 수집 및 이용 동의를 거부할 권리가 있습니다. 단, 필수 항목 동의 거부 시 서비스 이용이 제한될 수 있습니다.

5. 개인정보 제3자 제공 및 위탁

원칙적으로 이용자의 개인정보를 제3자에게 제공하지 않습니다. 단, 이용자의 별도 동의가 있는 경우 또는 법적 요구가 있을 경우에 한해 제공될 수 있습니다.

6. 개인정보 보호 문의처

담당 부서: Allert Sign 고객지원팀  
이메일: support@allertsign.com  
연락처: 010-xxxx-xxxx
                            """,
                            size=14,
                            selectable=True
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                ),
                padding=20,
                expand=True
            )
        ]
    )
