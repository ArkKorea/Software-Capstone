import flet as ft
from nav_bar import nav_bar

def group_register_success_screen(page: ft.Page):
    def save_qr_image(e):
        print("QR 이미지 저장하기 클릭")

    def share_qr(e):
        print("공유하기 클릭")

    def go_back(e):
        page.go("/myproductgroup")  # 원래 화면 경로로 바꿔줘

    return ft.View(
        route="/groupregistersuccess",
        controls=[
            # AppBar 추가
            ft.AppBar(
                title=ft.Text("등 록   완 료", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=go_back
                )
            ),
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            margin=ft.margin.only(left=-20),
                            padding=ft.padding.only(bottom=4),
                            content=ft.Image(
                                src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/productmanagement/home_productmanagement_registersuccess.png",
                                width=260,
                                height=260
                            )
                        ),
                        ft.Text(
                            "그룹등록이\n완료되었습니다.",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.BLACK87,
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=ft.Image(
                                src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=example",
                                width=120,
                                height=120
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=40),
                            content=ft.FilledButton(
                                text="QR 이미지 저장하기",
                                on_click=save_qr_image,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.GREEN,
                                    color=ft.colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=90, vertical=18),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    text_style=ft.TextStyle(
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                    )
                                )
                            )
                        ),
                        ft.TextButton(
                            text="공유하기",
                            on_click=share_qr,
                            style=ft.ButtonStyle(
                                color=ft.colors.BLACK87,
                                padding=ft.padding.only(top=10),
                                text_style=ft.TextStyle(
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                )
                            )
                        ),
                    ]
                )
            ),
            nav_bar(page, current_route="/history")
        ]
    )
