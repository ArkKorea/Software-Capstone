import flet as ft
from datetime import date, datetime
from config import BASE_URL
import httpx
import app_state

def day_diet_screen(page: ft.Page, selected_date: date) -> ft.View:
    sample_data = {
        "2025-04-05": [
            {"time": "11:35", "meals": ["치즈불닭볶음면", "참치마요 삼각김밥", "쿨피스 복숭아맛"]},
            {"time": "13:15", "meals": ["아몬드 초콜릿"]},
            {"time": "15:10", "meals": ["토마토 파스타", "고르곤졸라 피자", "청포도 에이드"]}
        ]
    }

    date_str = selected_date.strftime("%Y-%m-%d")
    #meals = sample_data.get(date_str, [])
    with httpx.Client(base_url=BASE_URL) as client:
        res = client.post(
            "api/user/meals/by-date",
            headers={"Authorization": f"Bearer {app_state.access_token}"},
            json={"date": date_str}
        )
        if res.status_code == 200:
            meals = res.json()["meals"]
        else:
            meals = []

    # 상단 날짜 및 버튼 표시
    date_display = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                controls=[
                    ft.Text(selected_date.strftime("%d"), size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(selected_date.strftime("%A").upper(), size=16, color=ft.Colors.GREY),
                    ft.Text(selected_date.strftime("%B %Y"), size=16, color=ft.Colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Container(  # ✅ 외부 패딩으로 감쌈
                padding=ft.Padding(0, 0, 20, 0),
                content=ft.TextButton(
                    text="오늘의 증상",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_100,
                        color=ft.Colors.GREEN,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: page.go(f"/todaysymptom?date={selected_date.isoformat()}")
                )
            )
        ]
    )

    def show_instake_log_detail(entry):
        dt_str = entry.get("datetime", "")
        try:
            date_str = datetime.fromisoformat(dt_str).strftime("%Y-%m-%d %H:%M")
        except Exception:
            date_str = "알 수 없음"

        food_name = entry.get("food_name", "알 수 없음")
        quantity = entry.get("quantity", "정보 없음")
        memo = entry.get("memo", "없음")
        matched_product = entry.get("matched_product")

        # 연동 식품 정보
        if matched_product:
            product_image = matched_product.get("image_url", "")
            product_name = matched_product.get("name", "이름 없음")
        else:
            product_image = ""
            product_name = "연동된 제품 없음"

        popup = ft.Container(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=20,
                width=350,
                height=480,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=12,
                    controls=[
                        ft.Text("🍽 식단 기록 상세", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"날짜: {date_str}", size=14),
                        ft.Text(f"식사명: {food_name}", size=14),
                        ft.Text(f"섭취량: {quantity}", size=14),
                        ft.Text(f"메모: {memo}", size=14),

                        ft.Divider(),

                        ft.Text("🔗 연동 제품", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            controls=[
                                ft.Image(
                                    src=product_image,
                                    width=60,
                                    height=60,
                                    border_radius=10
                                ) if product_image else ft.Icon(ft.Icons.NO_PHOTOGRAPHY),
                                ft.Text(product_name, size=14)
                            ]
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

    # 식단 목록
    meal_list_controls = []
    if meals:
        for entry in meals:
            dt_str = entry.get("datetime", "")
            try:
                time_str = datetime.fromisoformat(dt_str).strftime("%H:%M")
            except Exception:
                time_str = "??:??"

            food_name = entry.get("food_name", "알 수 없음")
            #quantity = entry.get("quantity", 1)
            #memo = entry.get("memo", "")
            meal_list_controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=16,
                controls=[
                    ft.Text(time_str, size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        expand=True,
                        padding=ft.Padding(10, 10, 10, 10),
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(food_name, size=16)
                            ]
                        ),
                        on_click=lambda e: show_instake_log_detail(entry)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.MORE_VERT,
                        icon_color=ft.Colors.GREY_600,
                        on_click=lambda e: print("옵션 클릭")
                    )
                ]
            )
        )
    else:
        meal_list_controls.append(
            ft.Text("등록된 식단이 없습니다.", size=16, color=ft.Colors.GREY_600, italic=True)
        )

    return ft.View(
        route=f"/daydiet?date={selected_date.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text(""),
                bgcolor=ft.Colors.WHITE,
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/dietmanagement")
                )
            ),
            ft.Container(
                padding=ft.Padding(20, 0, 0, 0),
                content=ft.Column(
                    controls=[
                        date_display,
                        ft.Container(height=10),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=40,
                                    controls=[
                                        ft.Text("Time", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                        ft.Text("식단 기록", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                                    ]
                                ),
                                ft.Container(  # ✅ 외부 패딩으로 감쌈
                                    padding=ft.Padding(0, 0, 20, 0),
                                    content=ft.TextButton(
                                        text="추가하기",
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.GREEN_100,
                                            color=ft.Colors.GREEN,
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=lambda e: page.go(f"/adddiet?from=daydiet&date={selected_date.isoformat()}")
                                    )
                                )
                            ]
                        ),
                        ft.Divider(),
                        *meal_list_controls,
                        ft.Container(height=20)
                    ],
                    scroll=ft.ScrollMode.HIDDEN
                )
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
