import flet as ft

def terms3_screen(page: ft.Page):
    def go_back(e):
        page.go("/signup")

    return ft.View(
        "/terms3",
        controls=[
            ft.AppBar(
                title=ft.Text("알레르기 정보 제공 및 면책 조항"),
                leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=go_back),
                bgcolor=ft.Colors.WHITE
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            """
< ALLERT SIGN 알레르기 정보 제공 및 면책 조항 >

제1조 (목적) 본 조항은 Allert Sign(이하 "본 서비스")이 제공하는 알레르기 정보 및 관련 콘텐츠의 정확성, 신뢰성, 책임 범위에 대해 설명하며, 이용자의 안전한 서비스 이용을 돕기 위한 것입니다.

제2조 (알레르기 정보의 제공 범위)

본 서비스는 사용자가 입력한 알레르기 정보를 바탕으로 음식 및 식품의 알레르기 성분 정보를 제공하며, 식당, 제조업체, 공공 데이터 등에서 제공하는 정보를 기반으로 합니다.

본 서비스는 정보 제공 목적으로 운영되며, 의료적 진단 또는 전문적인 영양 상담을 대체할 수 없습니다.

알레르기 정보는 시간이 지나면서 변경될 수 있으며, 제조업체 및 음식점의 성분 변동 사항이 실시간으로 반영되지 않을 수 있습니다.

제3조 (사용자의 책임과 유의사항)

본 서비스에서 제공하는 알레르기 정보는 참고용이며, 최종적인 섭취 여부는 이용자가 직접 확인해야 합니다.

이용자는 음식 섭취 전 반드시 음식점, 제조업체 또는 전문가와 추가적으로 확인해야 합니다.

본 서비스의 정보를 바탕으로 음식물을 섭취하여 발생하는 건강 문제(알레르기 반응 포함)에 대해 운영자는 법적 책임을 지지 않습니다.

이용자는 자신의 알레르기 정보를 정확하게 입력 및 관리할 책임이 있으며, 잘못된 정보 입력으로 인한 불이익에 대해 본 서비스는 책임지지 않습니다.

제4조 (책임의 한계)

본 서비스는 제공되는 정보의 정확성과 신뢰성을 유지하기 위해 최선을 다하지만, 정보의 완전성, 최신성, 정확성을 100% 보장할 수 없습니다.

본 서비스는 이용자가 본 정보를 신뢰하여 내린 결정(음식 섭취 등)에 대해 직접적, 간접적 손해에 대한 책임을 지지 않습니다.

이용자가 본 서비스에서 제공하는 정보를 신뢰하여 발생한 모든 결과는 본인의 책임이며, 이를 고려하여 신중히 이용해야 합니다.

제5조 (면책 사항)

본 서비스는 이용자의 건강 상태, 특이 체질 및 개인의 알레르기 반응을 개별적으로 분석하거나 진단하지 않습니다.

본 서비스에서 제공하는 알레르기 정보와 실제 음식 성분이 다를 수 있으며, 이에 따른 건강상의 문제 발생 시 본 서비스는 책임지지 않습니다.

서비스 운영자는 이용자가 음식점 또는 식품 제조업체에 직접 문의하여 정보를 확인할 것을 강력히 권장합니다.
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
