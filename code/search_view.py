import flet as ft
from nav_bar import nav_bar
from config import BASE_URL
import app_state
import httpx


def search_view_screen(page: ft.Page):
    search_filter = ft.Ref[str]()
    search_filter.current = "제품명"
    recent_searches = []
    search_result = ft.Column(spacing=10)
    recent_search_column = ft.Column()

    def change_filter(e):
        selected = e.control.text
        search_filter.current = selected
        selected_filter_label.value = selected
        page.update()

    selected_filter_label = ft.Text(search_filter.current, size=14)
    filter_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="제품명", on_click=change_filter),
            ft.PopupMenuItem(text="매장명", on_click=change_filter)
        ]
    )
    filter_row = ft.Row(
        controls=[selected_filter_label, filter_menu],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    def clear_search_history(e):
        recent_searches.clear()
        update_recent_searches()
        page.update()

    def update_recent_searches():
        recent_search_column.controls = [
            ft.Text(item, size=14) for item in recent_searches
        ]

    def product_preview(products, show_all=False):
        visible_products = products if show_all else products[:3]
        product_controls = [
            ft.Text(f"- {p['name']}", size=12, color=ft.Colors.GREY_700)
            for p in visible_products
        ]
        if not products:
            product_controls.append(ft.Text("등록된 상품 없음", size=12, color=ft.Colors.GREY_400))
        elif not show_all and len(products) > 3:
            product_controls.append(ft.Text("...", size=16, color=ft.Colors.GREY_400))
        return product_controls

    def show_all_products_popup(products):
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
                        *product_preview(products, show_all=True),
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

    def store_detail_popup(store_info, products):
        popup = ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=20,
                width=350,
                content=ft.Column(
                    spacing=12,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
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
                        *product_preview(products),
                        ft.TextButton(
                            text="전체보기",
                            on_click=lambda e: show_all_products_popup(products),
                            style=ft.ButtonStyle(color=ft.Colors.BLUE)
                        ),
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
            on_click=lambda e: store_detail_popup(store, products),
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
                    *product_preview(products)
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
            on_click=lambda e: product_detail_popup(product),
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


    def product_detail_popup(product):
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
                        # ✅ 이미지 가운데 정렬
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
                        ft.Text("홍길동님 알레르기 유발 식품", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(", ".join(allergens) if allergens else "없음", size=14, color=ft.Colors.RED_400),
                        ft.Text(f"{product['name']} 알레르기 유발 식품", size=14),
                        ft.Text(", ".join(safe_allergens) if safe_allergens else "없음", size=14, color=ft.Colors.BLUE_400),
                        ft.Text("전체 성분", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(product.get("ingredients_text", "성분 정보 없음"), size=13),

                        # ✅ 닫기 버튼 가운데 정렬
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



    def search_enter(e):
        keyword = search_field.value.strip()
        if not keyword:
            return

        if keyword not in recent_searches:
            recent_searches.insert(0, keyword)
        if len(recent_searches) > 10:
            recent_searches.pop()
        update_recent_searches()

        category = "product" if search_filter.current == "제품명" else "store"
        search_result.controls.clear()

        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/search",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={"type": category, "query": keyword}
            )
            if response.status_code == 200:
                if category == "product":
                    data = response.json()
                    products = data.get("products", [])
                    bundles = data.get("bundles", [])

                    if products:
                        search_result.controls.append(ft.Text("상품", size=18, weight=ft.FontWeight.BOLD))
                        for p in products:
                            search_result.controls.append(create_product_card(p))

                    if bundles:
                        search_result.controls.append(ft.Text("묶음 상품", size=18, weight=ft.FontWeight.BOLD))
                        for b in bundles:
                            search_result.controls.append(create_product_card(b))

                    if not products and not bundles:
                        search_result.controls.append(ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600))
                else:
                    stores = response.json().get("stores", [])
                    if stores:
                        search_result.controls.append(ft.Text("매장", size=18, weight=ft.FontWeight.BOLD))
                        for s in stores:
                            search_result.controls.append(create_store_card(s))
                    else:
                        search_result.controls.append(ft.Text("검색 결과가 없습니다.", size=16, color=ft.Colors.GREY_600))
            else:
                search_result.controls.append(ft.Text("검색 중 오류가 발생했습니다.", size=16, color=ft.Colors.RED))
        page.update()

    search_field = ft.TextField(
        hint_text="Search",
        border=None,
        filled=False,
        height=40,
        bgcolor=None,
        text_size=16,
        cursor_color=ft.Colors.BLACK,
        content_padding=ft.Padding(0, 0, 0, 0),
        border_color=ft.Colors.TRANSPARENT,
        border_radius=0,
        on_submit=search_enter
    )

    search_field.value = app_state.search_keyword or ""
    search_filter.current = app_state.search_category
    selected_filter_label.value = app_state.search_category
    if app_state.search_keyword:
        search_enter(None)
        app_state.search_keyword = ""

    return ft.View(
        route="/searchview",
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=ft.Padding(10, 40, 10, 10),
                        content=ft.Image(
                            src="https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image/home/home_text.png",
                            width=200
                        )
                    ),
                    ft.Container(
                        padding=ft.Padding(10, 20, 5, 20),
                        content=ft.Container(
                            height=50,
                            border_radius=10,
                            bgcolor=ft.Colors.GREY_100,
                            padding=ft.Padding(10, 0, 10, 0),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Icon(name="search", color=ft.Colors.GREY_600, size=22),
                                    ft.Container(width=page.width * 0.5, content=search_field),
                                    filter_row
                                ]
                            )
                        )
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        padding=ft.Padding(20, 0, 20, 0),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("최근 검색", size=16, weight=ft.FontWeight.BOLD),
                                ft.TextButton("전체 삭제", on_click=clear_search_history)
                            ]
                        )
                    ),
                    ft.Container(padding=ft.Padding(20, 0, 20, 0), content=recent_search_column),
                    ft.Container(height=10),
                    ft.Container(padding=ft.Padding(20, 0, 20, 80), content=search_result)
                ]
            ),
            nav_bar(page, current_route="/searchview")
        ]
    )