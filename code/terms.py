import flet as ft
from nav_bar import nav_bar  # 네비게이션 바 임포트

def terms_screen(page: ft.Page):
    tab_index = ft.Ref[int]()
    content_area = ft.Ref[ft.Container]()
    tab_btn_refs = [ft.Ref[ft.Container]() for _ in range(3)]

    terms_content = [
        ft.Text(
            '''제 1 조 (목적)
본 약관은 Allert Sign 애플리케이션(이하 "본 서비스")의 이용과 관련하여, 제공하는 서비스와 이용자의 권리, 의무 및 책임사항을 규정하는 것을 목적으로 합니다.

제 2 조 (정의)
"서비스"라 함은 Allert Sign 앱을 통해 제공되는 모든 기능과 관련된 서비스를 의미합니다.
"이용자"라 함은 본 약관에 따라 Allert Sign 서비스를 이용하는 개인 또는 단체를 의미합니다.
"운영자"라 함은 Allert Sign 서비스를 관리 및 운영하는 주체를 의미합니다.

제 3 조 (약관의 효력 및 변경)
본 약관은 이용자가 본 서비스를 이용함과 동시에 효력이 발생합니다.
운영자는 필요 시 본 약관을 변경할 수 있으며, 변경 사항은 앱 내 공지사항 또는 이메일을 통해 이용자에게 고지됩니다.
변경된 약관에 동의하지 않는 경우, 이용자는 서비스 이용을 중단할 수 있으며, 계속 사용할 경우 변경된 약관에 동의한 것으로 간주됩니다.

제 4 조 (서비스 이용 및 제한)
본 서비스는 이용자가 경고 및 알림 시스템을 효율적으로 활용할 수 있도록 지원합니다.
이용자는 관련 법령 및 본 약관을 준수하여야 하며, 다음과 같은 행위를 금지합니다:
- 서비스 운영을 방해하는 행위
- 허위 정보 입력 및 제공 행위
- 타인의 권리를 침해하는 행위
- 불법적인 목적으로 서비스를 이용하는 행위
위반 행위가 발견될 경우, 운영자는 서비스 이용을 제한하거나 계정을 정지할 수 있습니다.

제 5 조 (개인정보 보호)
운영자는 이용자의 개인정보를 보호하며, 관련 법령 및 개인정보처리방침을 준수합니다.
이용자는 개인정보 보호를 위해 본인의 계정 정보를 타인과 공유하지 않아야 합니다.

제 6 조 (책임의 한계)
운영자는 서비스 이용과 관련하여 발생하는 직접적, 간접적 손해에 대해 책임을 지지 않습니다.
이용자는 본 서비스를 이용함에 있어 스스로 판단하여 사용하며, 이에 따른 책임은 이용자 본인에게 있습니다.

제 7 조 (서비스 중단 및 변경)
운영자는 다음과 같은 사유로 서비스의 전부 또는 일부를 변경하거나 중단할 수 있습니다:
- 시스템 유지보수 및 업그레이드
- 운영 상의 필요에 따라 결정된 경우
- 천재지변, 정전, 서버 장애 등 불가항력적인 사유
이에 대해 운영자는 사전에 이용자에게 고지하며, 긴급한 경우에는 사후 공지할 수 있습니다.

제 8 조 (기타 조항)
본 약관에서 정하지 않은 사항은 관련 법령 및 운영자의 정책에 따릅니다.
본 서비스와 관련된 모든 분쟁은 대한민국 법률을 따르며, 관할 법원에서 해결합니다.

부칙: 본 약관은 2025년 3월 31일부터 적용됩니다.''',
            selectable=True
        ),
        ft.Text(
            '''Allert Sign(이하 "본 서비스")은 이용자의 개인정보를 보호하며, 관련 법령에 따라 개인정보 수집 및 이용에 대한 동의를 받고자 합니다.

1. 수집하는 개인정보 항목
- 필수: 이름, 이메일, 비밀번호, 성별, 생년월일, 알레르기 정보 및 건강 정보
- 선택: 위치 정보, 기타 사용자가 입력한 정보

2. 수집 및 이용 목적
- 회원 가입 및 관리, 맞춤형 정보 제공, 알레르기 기반 추천, QR 코드 기능 등

3. 보유 및 이용 기간
- 회원 탈퇴 시 즉시 파기. 법령에 따른 보관 시 해당 기간 이후 파기.

4. 동의 거부 권리 및 불이익
- 필수 항목 거부 시 서비스 이용 제한 가능

5. 개인정보 제3자 제공
- 원칙적으로 제공하지 않음. 법적 요구 또는 별도 동의 시 가능

6. 문의처
- Allert Sign 고객지원팀 / eogus117@naver.com / 010-7167-9801''',
            selectable=True
        ),
        ft.Text(
            '''제1조 (목적)
본 조항은 Allert Sign이 제공하는 알레르기 정보의 정확성, 신뢰성, 책임 범위를 규정합니다.

제2조 (정보 제공 범위)
- 입력된 정보를 기반으로 알레르기 정보를 제공합니다.
- 정보는 참고용이며, 의료적 진단을 대체하지 않습니다.
- 제조사/음식점 정보는 실시간으로 반영되지 않을 수 있습니다.

제3조 (사용자 책임)
- 최종 섭취 여부는 사용자 본인이 확인해야 합니다.
- 발생하는 건강 문제에 대해 서비스는 책임지지 않습니다.
- 사용자는 자신의 알레르기 정보를 정확히 입력 및 관리해야 합니다.

제4조 (책임의 한계)
- 정보는 최선을 다해 제공되나, 완전성과 정확성을 100% 보장할 수 없습니다.
- 본 정보를 신뢰해 발생한 손해에 대해 책임을 지지 않습니다.

제5조 (면책 조항)
- 본 서비스는 개인 건강 상태나 알레르기 반응을 진단하지 않으며, 실물과 차이 발생 시 책임을 지지 않습니다.
- 음식점/제조사에 직접 문의할 것을 권장합니다.''',
            selectable=True
        ),
    ]

    def on_tab_click(index):
        tab_index.current = index
        content_area.current.content = ft.Container(
            padding=ft.Padding(16, 16, 16, 16),
            content=terms_content[index]
        )
        for i, ref in enumerate(tab_btn_refs):
            ref.current.bgcolor = ft.Colors.GREEN if i == index else ft.Colors.GREY_400
        page.update()

    tab_index.current = 0

    return ft.View(
        "/terms",
        controls=[
            ft.AppBar(
                title=ft.Text("이  용  약  관", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/profileview")
                )
            ),
            ft.Container(
                padding=ft.Padding(10, 10, 0, 10),
                content=ft.Row(
                    controls=[
                        ft.Container(
                            ref=tab_btn_refs[0],
                            content=ft.Text("이용약관", size=16, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREEN,
                            border_radius=10,
                            padding=ft.Padding(12, 8, 12, 8),
                            on_click=lambda _: on_tab_click(0),
                        ),
                        ft.Container(
                            ref=tab_btn_refs[1],
                            content=ft.Text("개인정보 동의", size=16, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREY_400,
                            border_radius=10,
                            padding=ft.Padding(12, 8, 12, 8),
                            on_click=lambda _: on_tab_click(1),
                        ),
                        ft.Container(
                            ref=tab_btn_refs[2],
                            content=ft.Text("면책 조항", size=16, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.GREY_400,
                            border_radius=10,
                            padding=ft.Padding(12, 8, 12, 8),
                            on_click=lambda _: on_tab_click(2),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                )
            ),
            ft.Container(
                ref=content_area,
                padding=ft.Padding(16, 16, 16, 16),
                content=terms_content[0],
                expand=True,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                margin=ft.Margin(10, 10, 10, 10)
            ),
            ft.Container(height=70),
            nav_bar(page, current_route="/terms")
        ],
        bgcolor=ft.Colors.WHITE
    )
