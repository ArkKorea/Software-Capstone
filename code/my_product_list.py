import flet as ft
import httpx
import app_state
from config import BASE_URL
from nav_bar import nav_bar
from card_renderer import create_product_card
from popup_manager import product_manage_popup  # ✅ 관리 팝업 추가

def get_auth_headers():
    return {"Authorization": f"Bearer " + app_state.access_token}

def fetch_my_products():
    try:
        with httpx.Client() as client:
            res = client.post(f"{BASE_URL}/api/product/list", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json()
            else:
                print("❌ 상품 목록 요청 실패:", res.status_code, res.text)
    except Exception as e:
        print("❌ 상품 목록 요청 중 예외 발생:", e)
    return []

def my_product_list_screen(page: ft.Page):
    list_ref = ft.Ref[ft.ListView]()

    def on_load():
        print("🔄 내 상품 목록 불러오는 중...")
        items = fetch_my_products()
        if not items:
            list_ref.current.controls.append(
                ft.Text("등록된 상품이 없습니다.", size=16, color=ft.Colors.GREY)
            )
        else:
            for item in items:
                card = create_product_card(item)

                # ✅ 클릭 동작을 "관리용 팝업"으로 덮어씀
                card.on_click = lambda e, i=item: product_manage_popup(page, i)

                list_ref.current.controls.append(card)
        page.update()

    view = ft.View(
        "/myproductlist",
        controls=[
            ft.AppBar(
                title=ft.Text("상 품   목 록", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/productmanagement")
                )
            ),
            ft.Column(
                controls=[
                    ft.Divider(thickness=1, height=1, color=ft.Colors.GREY_300),
                    ft.Container(
                        expand=True,
                        content=ft.ListView(
                            ref=list_ref,
                            controls=[],  # 빈 상태에서 동적으로 추가
                            spacing=15,
                            padding=ft.Padding(20, 20, 20, 80),
                            auto_scroll=False
                        )
                    )
                ],
                expand=True
            ),
            nav_bar(page, current_route="/myproductlist")
        ]
    )

    # ✅ 목록 불러오기 시작
    on_load()

    return view
