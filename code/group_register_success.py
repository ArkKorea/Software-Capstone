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
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            margin=ft.Margin(top=0, bottom=0, left=-20, right=0),
                            padding=ft.Padding(top=0, bottom=4, left=0, right=0),
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
                            color=ft.Colors.BLACK87,
                        ),
                        ft.Container(
                            padding=ft.Padding(top=20, bottom=0, left=0, right=0),
                            content=ft.Image(
                                src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=example",
                                width=120,
                                height=120
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(left=90, top=18, right=90, bottom=18),  # ✅ 수정된 부분
                            content=ft.FilledButton(
                                text="QR 이미지 저장하기",
                                on_click=save_qr_image,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE,
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
                                color=ft.Colors.BLACK87,
                                padding=ft.Padding(top=1, bottom=0, left=0, right=0),
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
