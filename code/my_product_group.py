import flet as ft
import httpx
import app_state
from config import BASE_URL
from nav_bar import nav_bar

def get_auth_headers():
    return {"Authorization": f"Bearer " + app_state.access_token}

def fetch_my_groups():
    try:
        with httpx.Client() as client:
            res = client.post(f"{BASE_URL}/api/bundles/list", headers=get_auth_headers())
            if res.status_code == 200:
                return res.json().get("bundles", [])
            else:
                print("❌ 그룹 목록 요청 실패:", res.status_code, res.text)
    except Exception as e:
        print("❌ 그룹 목록 요청 중 예외:", e)
    return []

def my_product_group_screen(page: ft.Page):
    selected_sort_option = ft.Text("정렬", size=14, color=ft.Colors.GREEN)
    search_field = ft.Ref[ft.TextField]()
    list_container = ft.Ref[ft.Column]()

    groups_data = []

    def apply_search_filter(e=None):
        keyword = search_field.current.value.strip().lower()
        filtered = [g for g in groups_data if keyword in g["name"].lower()]
        render_group_list(filtered)

    def render_group_list(bundles):
        if not bundles:
            list_container.current.controls = [
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    padding=ft.Padding(top=20, left=20, right=20, bottom=20),
                    content=ft.Text("그룹이 없습니다.", size=18, color=ft.Colors.GREY)
                )
            ]
        else:
            list_container.current.controls = [
                ft.Container(
                    padding=ft.Padding(10, 20, 10, 20),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.GREY_200),
                    on_click=lambda e, id=bundle["id"]: print(f"그룹 {id} 클릭됨"),
                    content=ft.Row(
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src=bundle["image_url"],
                                width=60,
                                height=60,
                                fit=ft.ImageFit.COVER,
                                border_radius=8
                            ),
                            ft.Text(bundle["name"], size=18, weight=ft.FontWeight.W_500)
                        ]
                    )
                )
                for bundle in bundles
            ]
        page.update()

    def on_load():
        nonlocal groups_data
        groups_data = fetch_my_groups()
        apply_search_filter()

    view = ft.View(
        "/myproductgroup",
        controls=[
            ft.AppBar(
                title=ft.Text("그 룹   관 리", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/productmanagement")
                )
            ),

            ft.Column(
                controls=[
                    # 검색창
                    ft.Container(
                        padding=ft.Padding(top=0, left=20, right=20, bottom=10),
                        content=ft.TextField(
                            ref=search_field,
                            hint_text="검색",
                            prefix_icon=ft.Icons.SEARCH,
                            on_change=apply_search_filter,
                            filled=True,
                            fill_color=ft.Colors.GREY_100,
                            border_radius=15,
                            border_color=ft.Colors.TRANSPARENT
                        )
                    ),

                    # 정렬 & 추가하기 버튼
                    ft.Container(
                        padding=ft.Padding(top=0, left=20, right=20, bottom=10),
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    width=105,
                                    height=40,
                                    border=ft.Border(
                                        top=ft.BorderSide(1, ft.Colors.GREEN),
                                        right=ft.BorderSide(1, ft.Colors.GREEN),
                                        bottom=ft.BorderSide(1, ft.Colors.GREEN),
                                        left=ft.BorderSide(1, ft.Colors.GREEN),
                                    ),
                                    border_radius=12,
                                    bgcolor=ft.Colors.WHITE,
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.PopupMenuButton(
                                        items=[
                                            ft.PopupMenuItem(
                                                text="이름순",
                                                on_click=lambda _: (
                                                    setattr(selected_sort_option, "value", "이름순"),
                                                    page.update()
                                                )
                                            ),
                                            ft.PopupMenuItem(
                                                text="생성순",
                                                on_click=lambda _: (
                                                    setattr(selected_sort_option, "value", "생성순"),
                                                    page.update()
                                                )
                                            )
                                        ],
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=4,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            controls=[
                                                ft.Icon(name=ft.Icons.UNFOLD_MORE, size=18, color=ft.Colors.GREEN),
                                                selected_sort_option,
                                                ft.Icon(name=ft.Icons.KEYBOARD_ARROW_DOWN, size=18, color=ft.Colors.GREY_400),
                                            ]
                                        )
                                    )
                                ),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    text="추가하기",
                                    icon=ft.Icons.ADD,
                                    on_click=lambda _: page.go("/groupregister"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.GREEN,
                                        bgcolor=ft.Colors.WHITE,
                                        side=ft.BorderSide(1, ft.Colors.GREEN),
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.Padding(10, 5, 10, 5)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),

                    # 그룹 리스트 영역
                    ft.Column(ref=list_container, controls=[]),

                    ft.Container(height=70)
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN
            ),

            nav_bar(page, current_route="/myproductgroup")
        ]
    )

    on_load()
    return view
