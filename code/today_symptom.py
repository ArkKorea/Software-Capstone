import flet as ft
from datetime import date
from urllib.parse import urlparse, parse_qs
from nav_bar import nav_bar
from functools import partial
from config import BASE_URL
import app_state
import httpx
SYMPTOM_CATEGORIES = ["피부", "복통", "호흡", "두통", "피로"]

def today_symptom_screen(page: ft.Page):
    qs = parse_qs(urlparse(page.route).query)
    date_str = qs.get("date", [None])[0]
    try:
        selected_date = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        selected_date = date.today()

    username = "홍길동"

    ratings = {s: 0 for s in SYMPTOM_CATEGORIES}
    error_msgs = {s: "" for s in SYMPTOM_CATEGORIES}
    result_text = ft.Text("")

    # 상위 컨테이너 안에 전체 증상 평가 영역이 들어감
    symptom_column = ft.Column(spacing=20)

    def go_back_to_day_diet(e):
        page.overlay.clear()
        page.go(f"/daydiet?date={selected_date.isoformat()}")

    def update_rating(symptom, rating):
        ratings[symptom] = rating
        error_msgs[symptom] = ""
        refresh_symptom_ui()

    def refresh_symptom_ui():
        symptom_column.controls = build_symptom_ui()
        page.update()

    def load_today_symptom():
        try:
            with httpx.Client(base_url=BASE_URL) as client:
                response = client.post(
                    "/api/user/symptoms/by-date",
                    headers={"Authorization": f"Bearer {app_state.access_token}"},
                    json={
                        "date": selected_date.isoformat()
                        
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        ratings["피부"] = data["skin"]
                        ratings["복통"] = data["stomach"]
                        ratings["호흡"] = data["breath"]
                        ratings["두통"] = data["headache"]
                        ratings["피로"] = data["fatigue"]
                    else:
                        pass
        except Exception as e:
            print(e)

    def on_submit(e):
        has_error = False
        for s in SYMPTOM_CATEGORIES:
            if ratings[s] == 0:
                error_msgs[s] = "필수 체크 항목입니다."
                has_error = True
            else:
                error_msgs[s] = ""
        with httpx.Client(base_url=BASE_URL) as client:
            response = client.post(
                "/api/user/symptoms/save",
                headers={"Authorization": f"Bearer {app_state.access_token}"},
                json={
                    "date": selected_date.isoformat(),
                    "skin": ratings["피부"],
                    "stomach": ratings["복통"],
                    "breath": ratings["호흡"],
                    "headache": ratings["두통"],
                    "fatigue": ratings["피로"]  
                }
            )
            if response.status_code == 200:
                has_error = False
            else: result_text.value = "❌ 증상 저장에 실패했습니다. 다시 시도해주세요."
        result_text.value = "" if has_error else "증상이 저장되었습니다."
        refresh_symptom_ui()

    def build_symptom_ui():
        ui_list = [
            ft.Text(f"{selected_date.strftime('%Y-%m-%d')} {username}님 오늘의 증상", size=20, weight=ft.FontWeight.BOLD)
        ]
        for symptom in SYMPTOM_CATEGORIES:
            ui_list.append(
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(symptom, size=16),
                        ft.Row(
                            spacing=2,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.GestureDetector(
                                    on_tap=lambda e, s=symptom, r=i+1: update_rating(s, r),
                                    #on_tap = partial(update_rating, symptom, i+1),
                                    #on_tap=lambda e, s=symptom, i=i: update_rating(s, i + 1),
                                    content=ft.Icon(
                                        name=ft.Icons.STAR,
                                        color=ft.Colors.GREEN if i < ratings[symptom] else ft.Colors.GREY_300,
                                        size=24
                                    )
                                )
                                for i in range(5)
                            ]
                        ),
                        ft.Text(error_msgs[symptom], size=12, color=ft.Colors.RED) if error_msgs[symptom] else ft.Container()
                    ]
                )
            )
        ui_list.extend([
            ft.ElevatedButton("저장 하기", on_click=on_submit, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=400),
            result_text
        ])
        return ui_list

    # 처음 UI 세팅
    load_today_symptom()
    symptom_column.controls = build_symptom_ui()

    return ft.View(
        route=f"/todaysymptom?date={selected_date.isoformat()}",
        controls=[
            ft.AppBar(
                title=ft.Text("오 늘 의   증 상", size=22, weight=ft.FontWeight.BOLD),
                center_title=True,
                bgcolor=ft.Colors.WHITE,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=go_back_to_day_diet)
            ),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    ft.Container(
                        padding=20,
                        content=symptom_column
                    )
                ]
            ),
            nav_bar(page, current_route="/todaysymptom")
        ]
    )
