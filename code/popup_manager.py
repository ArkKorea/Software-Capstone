import flet as ft
from flet import Ref
from app_state import access_token
import httpx
from config import BASE_URL
import app_state

def record_history(item_type: str, item_id: int):
    try:
        with httpx.Client(base_url=BASE_URL) as client:
            client.post(
                "/api/history/add",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={"type": item_type, "target_id": item_id}
            )
    except Exception as e:
        print(f"[ERROR] history 기록 실패: {e}")

def toggle_favorite(page: ft.Page, item_type: str, item_id: int, is_fav_ref: Ref):
    import httpx
    from config import BASE_URL
    from app_state import access_token

    action = "remove" if is_fav_ref.current else "add"
    body = {
        "type": item_type,
        "action": action,
    }
    if item_type == "food":
        body["food_id"] = item_id
    elif item_type == "bundle":
        body["bundle_id"] = item_id
    elif item_type == "supplier":
        body["supplier_id"] = item_id

    try:
        with httpx.Client(base_url=BASE_URL) as client:
            res = client.post(
                "/api/user/favorites",
                headers={"Authorization": f"Bearer {access_token}"},
                json=body
            )
            if res.status_code == 200:
                is_fav_ref.current = not is_fav_ref.current
                page.update()
    except Exception as e:
        print("즐겨찾기 실패:", e)


def product_detail_popup(page: ft.Page, product: dict):
    is_bundle = product.get("bundle_id") is not None
    product_id = product["bundle_id"] if is_bundle else product["product_id"]
    product_type = "bundle" if is_bundle else "food"
    image_url = f"{BASE_URL}{product['image_url']}" if product["image_url"].startswith("/static") else product["image_url"]

    record_history(product_type, product_id)

    allergens = product.get("allergens_hit") or product.get("allergen_hit") or []
    safe_allergens = product.get("allergens_safe") or product.get("allergen_safe") or []
    is_fav_ref = Ref[bool]()
    is_fav_ref.current = product.get("is_favorite", False)

    def update_star_icon():
        star_icon.name = "star" if is_fav_ref.current else "star_border"
        star_icon.icon_color = ft.Colors.AMBER if is_fav_ref.current else ft.Colors.GREY_600
        page.update()

    star_icon = ft.IconButton(
        icon="star" if is_fav_ref.current else "star_border",
        icon_color=ft.Colors.AMBER if is_fav_ref.current else ft.Colors.GREY_600,
        icon_size=20,
        on_click=lambda e: (
            toggle_favorite(page, product_type, product_id, is_fav_ref),
            update_star_icon()
            
        )
    )

    popup = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=20,
            width=350,
            height=580,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src=image_url,
                                fit=ft.ImageFit.COVER,
                                height=180,
                                border_radius=ft.border_radius.all(12)
                            )
                        ]
                    ),
                    ft.Row(spacing=5, controls=[
                        ft.Text(product["name"], size=20, weight=ft.FontWeight.BOLD),
                        star_icon
                    ]),
                    ft.Text(f"📍 {product.get('supplier_name', '')}", size=14, color=ft.Colors.GREY_600),
                    ft.Text("알레르기 유발 성분", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(", ".join(allergens) if allergens else "없음", size=14, color=ft.Colors.RED_400),
                    ft.Text("안전 성분", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(", ".join(safe_allergens) if safe_allergens else "정보 없음", size=14, color=ft.Colors.GREEN_400),
                    ft.Text("전체 성분", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(product.get("ingredients_text", "성분 정보 없음"), size=13),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                text="닫기",
                                on_click=lambda e: (page.overlay.clear(), page.go(page.route, replace=True)),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE,
                                    padding=ft.Padding(40, 10, 40, 10),
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            )
                        ]
                    )
                ]
            )
        )
    )

    page.overlay.clear()
    page.overlay.append(popup)
    page.update()

def show_all_products_popup(page: ft.Page, products: list):
    popup = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=20,
            width=350,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=[
                    ft.Text("전체 판매 상품", size=18, weight=ft.FontWeight.BOLD),
                    *[
                        ft.Text(f"- {p['name']}", size=12, color=ft.Colors.GREY_700)
                        for p in products
                    ],
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                text="닫기",
                                on_click=lambda e: (page.overlay.clear(), page.update()),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREEN,
                                    color=ft.Colors.WHITE,
                                    padding=ft.Padding(40, 10, 40, 10),
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                )
                            )
                        ]
                    )
                ]
            )
        )
    )
    page.overlay.clear()
    page.overlay.append(popup)
    page.update()


def store_detail_popup(page: ft.Page, store_info: dict, products: list, show_all_button: bool = False):
    record_history("supplier", store_info["store_id"])

    try:
        with httpx.Client(base_url=BASE_URL) as client:
            res = client.post(
                "/api/store/products",
                json={"store_id": store_info["store_id"]},
                headers={"Authorization": f"Bearer {app_state.access_token}"}
            )
            if res.status_code == 200:
                products = res.json().get("products", [])
    except Exception as e:
        print("상품 목록 조회 실패:", e)

    is_fav_ref = Ref[bool]()
    is_fav_ref.current = store_info.get("is_favorite", False)

    def update_star_icon():
        star_icon.icon = "star" if is_fav_ref.current else "star_border"
        star_icon.icon_color = ft.Colors.AMBER if is_fav_ref.current else ft.Colors.GREY_600
        page.update()

    star_icon = ft.IconButton(
        icon="star" if is_fav_ref.current else "star_border",
        icon_color=ft.Colors.AMBER if is_fav_ref.current else ft.Colors.GREY_600,
        icon_size=20,
        on_click=lambda e: (
            toggle_favorite(page, "supplier", store_info["store_id"], is_fav_ref),
            update_star_icon()
        )
    )

    def build_product_list():
        items = [
            ft.Text(f"- {p['name']}", size=12, color=ft.Colors.GREY_700)
            for p in products[:5]
        ]
        if not products:
            items = [ft.Text("등록된 상품 없음", size=12, color=ft.Colors.GREY_400)]
        return items

    controls = [
        ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/product/store.png",
                    width=30,
                    height=30
                ),
                ft.Text(store_info["name"], size=20, weight=ft.FontWeight.BOLD),
                star_icon  # ⭐ 즐겨찾기 버튼 추가됨
            ]
        ),
        ft.Text(f"주소: {store_info['address']}", size=14, color=ft.Colors.GREY_600),
        ft.Container(height=10),
        ft.Text("판매 상품", size=14, weight=ft.FontWeight.BOLD),
        *build_product_list()
    ]

    if show_all_button:
        controls.append(
            ft.TextButton(
                text="전체보기",
                on_click=lambda e: show_all_products_popup(page, products),
                style=ft.ButtonStyle(color=ft.Colors.BLUE)
            )
        )

    controls.append(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(
                    text="닫기",
                    on_click=lambda e: (page.overlay.clear(), page.go(page.route, replace=True)),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN,
                        color=ft.Colors.WHITE,
                        padding=ft.Padding(40, 10, 40, 10),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            ]
        )
    )

    popup = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        content=ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            padding=20,
            width=350,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=controls
            )
        )
    )
    page.overlay.clear()
    page.overlay.append(popup)
    page.update()
