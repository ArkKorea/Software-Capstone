import flet as ft
from nav_bar import nav_bar
import httpx
from config import BASE_URL
import app_state

def my_allergy_screen(page: ft.Page):
    allergy_items = [
        ("home_myallergy_crab", "게"), ("home_myallergy_shrimp", "새우"), ("home_myallergy_fish", "고등어"),
        ("home_myallergy_beef", "소고기"), ("home_myallergy_pork", "돼지고기"), ("home_myallergy_chicken", "닭고기"),
        ("home_myallergy_abalone", "조개류"), ("home_myallergy_cashew", "땅콩"), ("home_myallergy_walnut", "호두"),
        ("home_myallergy_peach", "복숭아"), ("home_myallergy_tomato", "토마토"), ("home_myallergy_nuts", "메밀"),
        ("home_myallergy_wheat", "밀"), ("home_myallergy_sesame", "잣"), ("home_myallergy_sulfurousacid", "아황산류"),
        ("home_myallergy_egg", "난류"), ("home_myallergy_squid", "오징어"), ("home_myallergy_milk", "우유"),
        ("home_myallergy_soybean", "대두")
    ]

    with httpx.Client(base_url=BASE_URL) as client:
        response = client.post("/api/user/allergies/get", 
                               headers={"Authorization": f"Bearer {app_state.access_token}"})
        if response.status_code == 200:
            data = response.json()
            user_allergies = data["allergies"]

    if user_allergies:
        selected_allergies = set(user_allergies)
    else:
        selected_allergies = set()

    allergy_count_text = ft.Text(f"알  레  르  기   :   {len(selected_allergies)}  개", size=18, text_align=ft.TextAlign.CENTER)

    def update_allergy_count():
        allergy_count_text.value = f"알  레  르  기   :   {len(selected_allergies)}  개"
        allergy_count_text.update()

    def create_allergy_button(image_id, label):
        selected = label in user_allergies
        if selected:
            selected_allergies.add(label)

        container = ft.Container(
            bgcolor=ft.Colors.GREEN_300 if selected else ft.Colors.LIGHT_GREEN_100,
            border_radius=12,
            padding=ft.Padding(8, 8, 8, 8),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(
                        src=f"https://raw.githubusercontent.com/ArkKorea/Software-Capstone/ui/image//home/myallergy/{image_id}.png",
                        width=29,
                        height=29
                    ),
                    ft.Text(label, size=14, text_align=ft.TextAlign.CENTER)
                ]
            )
        )

        def toggle_selection(e):
            nonlocal selected
            selected = not selected
            if selected:
                selected_allergies.add(label)
                container.bgcolor = ft.Colors.GREEN_300
            else:
                selected_allergies.discard(label)
                container.bgcolor = ft.Colors.LIGHT_GREEN_100
            container.update()
            update_allergy_count()

        return ft.GestureDetector(on_tap=toggle_selection, content=container)

    # ✅ 정확히 4개씩 배치되도록 설정
    allergy_grid = ft.GridView(
        max_extent=95,
        child_aspect_ratio=1.1,
        spacing=12,
        run_spacing=12,
        controls=[create_allergy_button(img_id, label) for img_id, label in allergy_items],
        expand=False
    )

    def save_allergies(selected_allergies):
        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/user/allergies/save",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={"allergies": list(selected_allergies)}
            )
            if response.status_code == 200:
                print("알레르기 정보가 성공적으로 저장되었습니다.")
            else:
                print("알레르기 정보 저장에 실패했습니다.")

    return ft.View(
        "/myallergy",
        controls=[
            ft.AppBar(
                title=ft.Text("내   알 레 르 기", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/home")
                ),
                actions=[
                    ft.Container(
                        margin=ft.Margin(top=0, bottom=0, left=0, right=10),
                        content=ft.TextButton(
                            "저장",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                            on_click=lambda _: save_allergies(selected_allergies)
                        )
                    )
                ]
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("홍  길  동  님", size=18, text_align=ft.TextAlign.CENTER),
                                allergy_count_text,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        )
                    ),
                    ft.Container(height=20),
                    # ✅ 좌우 여백 포함한 GridView
                    ft.Container(
                        padding=ft.Padding(top=0, bottom=0, left=20, right=20),
                        content=allergy_grid
                    ),
                    ft.Container(height=30),
                ]
            ),
            nav_bar(page, current_route="/myallergy")
        ]
    )
