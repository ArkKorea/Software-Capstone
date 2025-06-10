import flet as ft
from urllib.parse import parse_qs, urlparse
from nav_bar import nav_bar
from config import BASE_URL
from qr_maker import qr_code_maker
import requests

def product_register_success_screen(page: ft.Page):
    qs = parse_qs(urlparse(page.route).query)
    product_name = qs.get("name", [None])[0]
    print("저장에 성공한 상품의 id는 " + product_name + "입니다.")
    qr_code_url = qr_code_maker("product", product_name)

    def save_qr_image(e):
        save_path = f"product_{product_name}.png"
        response = requests.get(qr_code_url)
        if response.status_code == 200:
            with open(save_path , "wb") as f:
                f.write(response.content)
            print("저장완료")
        print("QR 이미지 저장하기 클릭")

    def share_qr(e):
        print("공유하기 클릭")

    def go_back(e):
        page.go("/productmanagement")  # 원래 화면 경로로 바꿔줘

    return ft.View(
        route=f"/productregistersuccess?id={product_name}",
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
                            "상품등록이\n완료되었습니다.",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK87,
                        ),
                        ft.Container( #qr코드 부분분
                            padding=ft.Padding(top=20, bottom=0, left=0, right=0),
                            content=ft.Image(
                                src=qr_code_url,
                                width=120,
                                height=120
                            )
                        ),
                        ft.Container(
                            padding=ft.Padding(top=40, bottom=0, left=0, right=0),
                            content=ft.FilledButton(
                                text="QR 이미지 저장하기",
                                on_click=save_qr_image,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE,
                                    padding=ft.Padding(90, 18, 90, 18),
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
                                padding=ft.Padding(top=10, bottom=0, left=0, right=0),
                                text_style=ft.TextStyle(
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                )
                            )
                        ),
                    ]
                )
            ),
            nav_bar(page, current_route="/productregistersuccess")
        ]
    )
