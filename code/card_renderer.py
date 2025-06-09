import flet as ft
import app_state
import httpx
from config import BASE_URL


def create_store_card(store):
    products = []
    try:
        with httpx.Client(base_url=BASE_URL) as client:
            res = client.post(
                "/api/store/products",
                json={"store_id": store["store_id"]},
                headers={"Authorization": f"Bearer {app_state.access_token}"}
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
        on_click=lambda e: print(f"{store['name']} 클릭됨"),  # 또는 상세 팝업
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
                *[ft.Text(f"- {p['name']}", size=12, color=ft.Colors.GREY_700) for p in products[:3]]
            ]
        )
    )


def create_product_card(item):
    is_bundle = "bundle_id" in item
    is_fav = item.get("is_favorite", False)

    name = item.get("name", "")
    image_url = item.get("image_url", "")
    if image_url and image_url.startswith("/static"):
        image_url = f"{BASE_URL}{image_url}"

    supplier_name = item.get("supplier_name", "")
    ingredients = item.get("ingredient", "") if not is_bundle else ""
    allergens = item.get("allergens_hit") or item.get("allergen_hit") or []
    safe_allergens = item.get("allergens_safe") or item.get("allergen_safe") or []

    return ft.Container(
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_200),
        on_click=lambda e: print(f"{name} 클릭됨"),
        content=ft.Row(
            controls=[
                ft.Image(
                    src=image_url,
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
                                ft.Text(
                                    f"{'[번들] ' if is_bundle else '[상품] '}{name}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Icon(
                                    name="star" if is_fav else "star_border",
                                    color=ft.Colors.AMBER if is_fav else ft.Colors.GREY_600,
                                    size=16
                                )
                            ]
                        ),
                        ft.Text(f"공급업체: {supplier_name}", size=12, color=ft.Colors.GREY_600),
                        ft.Text(f"원재료: {ingredients}" if not is_bundle else "묶음 상품", size=12, color=ft.Colors.GREY_700),
                        ft.Text(f"알레르기 유발: {', '.join(allergens) if allergens else '없음'}", size=12, color=ft.Colors.RED_400),
                        ft.Text(f"안전 성분: {', '.join(safe_allergens) if safe_allergens else '정보 없음'}", size=12, color=ft.Colors.GREEN_400),
                    ]
                )
            ]
        )
    )
