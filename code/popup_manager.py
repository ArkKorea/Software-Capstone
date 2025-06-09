import flet as ft
from app_state import access_token

def product_detail_popup(page: ft.Page, product: dict):
    allergens = product.get("allergens_hit") or product.get("allergen_hit") or []
    safe_allergens = product.get("allergens_safe") or product.get("allergen_safe") or []
    is_fav = product.get("is_favorite", False)

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
                                src=product["image_url"],
                                fit=ft.ImageFit.COVER,
                                height=180,
                                border_radius=ft.border_radius.all(12)
                            )
                        ]
                    ),
                    ft.Row(
                        spacing=5,
                        controls=[
                            ft.Text(product["name"], size=20, weight=ft.FontWeight.BOLD),
                            ft.Icon(
                                name="star" if is_fav else "star_border",
                                color=ft.Colors.AMBER if is_fav else ft.Colors.GREY_600,
                                size=20
                            )
                        ]
                    ),
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

import flet as ft

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
