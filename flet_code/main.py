import flet as ft
import asyncio
from login import splash_content, login_screen
from signup import signup_screen

async def main(page: ft.Page):
    page.title = "ALLERT SIGN"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

    # splash 화면 먼저 보여주기
    page.clean()
    page.add(splash_content(page))
    await asyncio.sleep(2)
    page.go("/login")

    # 라우트 변경될 때마다 실행
    def route_change(e):
        page.views.clear()

        if page.route == "/signup":
            page.views.append(signup_screen(page))
        elif page.route == "/login":
            page.views.append(login_screen(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)  # 현재 라우트를 강제로 처리해줌

ft.app(target=main, view=ft.AppView.WEB_BROWSER)