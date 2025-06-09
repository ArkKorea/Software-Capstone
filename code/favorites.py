import flet as ft
import app_state
import httpx
from config import BASE_URL
from nav_bar import nav_bar
from popup_manager import product_detail_popup, store_detail_popup

def get_auth_headers():
    return {"Authorization": f"Bearer {app_state.access_token}"}


def fetch_favorite_suppliers():
    try:
        with httpx.Client() as client:
            res = client.get(f"{BASE_URL}/api/user/favorites/suppliers", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json().get("stores", [])
    except Exception as e:
        print("매장 즐겨찾기 요청 실패:", e)
    return []


def fetch_favorite_items():
    try:
        with httpx.Client() as client:
            res = client.get(f"{BASE_URL}/api/user/favorites/items", headers=get_auth_headers())
            if res.status_code == 200:
                data = res.json()
                return data.get("products", []), data.get("bundles", [])
    except Exception as e:
        print("음식/번들 즐겨찾기 요청 실패:", e)
    return [], []


def favorites_screen(page: ft.Page):
    tab_state = ft.Ref[int]()
    content_area = ft.Ref[ft.Container]()
    store_box = ft.Ref[ft.Container]()
    food_box = ft.Ref[ft.Container]()

    favorites_store = []
    favorites_food = []

    def create_store_card(store):
        products = []
        try:
            with httpx.Client(base_url=BASE_URL) as client:
                res = client.post(
                    "/api/store/products",
                    json={"store_id": store["store_id"]},
                    headers=get_auth_headers()
                )
                if res.status_code == 200:
                    products = res.json().get("products", [])
        except Exception as e:
            print("상품 조회 실패:", e)

        return ft.Container(
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_200),
            on_click=lambda e: store_detail_popup(page, store, products),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Image(
                                src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/product/store.png",
                                width=30,
                                height=30
                            ),
                            ft.Text(store["name"], size=16, weight=ft.FontWeight.BOLD),
                            ft.Icon(
                                name="star" if store.get("is_favorite", False) else "star_border",
                                color=ft.Colors.AMBER if store.get("is_favorite", False) else ft.Colors.GREY_600,
                                size=16
                            )
                        ]
                    ),
                    ft.Text(store["address"], size=14, color=ft.Colors.GREY_600),
                    ft.Text("판매 상품", size=13, weight=ft.FontWeight.BOLD),
                    *[
                        ft.Text(f"- {p['name']}", size=12, color=ft.Colors.GREY_700)
                        for p in products[:3]
                    ]
                ]
            )
        )

    def create_product_card(product):
        allergens = product.get("allergens_hit") or product.get("allergen_hit") or []
        safe_allergens = product.get("allergens_safe") or product.get("allergen_safe") or []
        is_fav = product.get("is_favorite", False)

        return ft.Container(
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_200),
            on_click=lambda e: product_detail_popup(page, product),
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=product["image_url"],
                        width=80,
                        height=80,
                        fit=ft.ImageFit.COVER,
                        border_radius=8
                    ),
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Text(product["name"], size=16, weight=ft.FontWeight.BOLD),
                                    ft.Icon(
                                        name="star" if is_fav else "star_border",
                                        color=ft.Colors.AMBER if is_fav else ft.Colors.GREY_600,
                                        size=16
                                    )
                                ]
                            ),
                            ft.Text(f"공급업체: {product.get('supplier_name', '')}", size=12, color=ft.Colors.GREY_600),
                            ft.Text(f"원재료: {product.get('ingredients_text', '')}", size=12, color=ft.Colors.GREY_700),
                            ft.Text(f"알레르기 유발: {', '.join(allergens) if allergens else '없음'}", size=12, color=ft.Colors.RED_400),
                            ft.Text(f"안전 성분: {', '.join(safe_allergens) if safe_allergens else '정보 없음'}", size=12, color=ft.Colors.GREEN_400),
                        ]
                    )
                ]
            )
        )

    def update_content(index):
        tab_state.current = index
        page.client_storage.set("favorite_tab", "store" if index == 0 else "food")
        store_box.current.bgcolor = ft.Colors.GREEN_400 if index == 0 else ft.Colors.GREY_300
        food_box.current.bgcolor = ft.Colors.GREEN_400 if index == 1 else ft.Colors.GREY_300

        items = favorites_store if index == 0 else favorites_food
        if not items:
            content_area.current.content = ft.Container(
                alignment=ft.Alignment(0, 0),
                height=page.height * 0.7,
                bgcolor=ft.Colors.GREY_100,
                content=ft.Text("즐겨찾기 항목이 없습니다.", size=16, color=ft.Colors.GREY)
            )
        else:
            content_area.current.content = ft.Container(
                bgcolor=ft.Colors.GREY_100,
                padding=10,
                height=page.height * 0.7,
                content=ft.Column(
                    controls=[
                        create_store_card(item) if index == 0 else create_product_card(item)
                        for item in items
                    ],
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        page.update()

    def on_load():
        nonlocal favorites_store, favorites_food
        favorites_store = fetch_favorite_suppliers()
        products, bundles = fetch_favorite_items()
        favorites_food = products + bundles
        initial_tab = page.client_storage.get("favorite_tab") or "store"
        update_content(0 if initial_tab == "store" else 1)

    page.on_view_pop = lambda _: update_content(
        0 if page.client_storage.get("favorite_tab") == "store" else 1
        )

    view = ft.View(
        "/favorites",
        controls=[
            ft.Column(
                [
                    ft.Container(
                        padding=ft.Padding(top=40, left=10, right=10, bottom=10),
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Text("즐 겨 찾 기", size=22, weight=ft.FontWeight.BOLD),
                                    expand=True,
                                ),
                                ft.Container(
                                    alignment=ft.Alignment(-1, 0),
                                    content=ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK,
                                        on_click=lambda _: page.go("/home")
                                    ),
                                )
                            ],
                            height=50
                        )
                    ),

                    ft.Container(
                        padding=ft.Padding(top=0, bottom=0, left=10, right=10),
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    ref=store_box,
                                    expand=1,
                                    height=40,
                                    bgcolor=ft.Colors.GREEN_400,
                                    alignment=ft.Alignment(0, 0),
                                    border_radius=10,
                                    content=ft.Text("매장", size=16, color=ft.Colors.WHITE),
                                    on_click=lambda _: update_content(0),
                                ),
                                ft.Container(
                                    ref=food_box,
                                    expand=1,
                                    height=40,
                                    bgcolor=ft.Colors.GREY_300,
                                    alignment=ft.Alignment(0, 0),
                                    border_radius=10,
                                    content=ft.Text("음식", size=16, color=ft.Colors.WHITE),
                                    on_click=lambda _: update_content(1),
                                ),
                            ],
                            spacing=10
                        )
                    ),

                    ft.Container(ref=content_area),
                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),
            nav_bar(page, current_route="/favorites")
        ]
    )

    on_load()
    return view
