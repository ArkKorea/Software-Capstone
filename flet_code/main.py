# main.py
import flet as ft
import asyncio
from login import splash_content, login_screen
from signup import signup_screen
from terms1 import terms1_screen
from terms2 import terms2_screen
from terms3 import terms3_screen
from email_verification_sent import email_verification_sent_screen
from email_verified import email_verified_screen

async def main(page: ft.Page):
    page.title = "ALLERT SIGN"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

    user_email = ""  # 전역 email 상태 저장

    # splash 먼저 보여주기
    page.clean()
    page.add(splash_content(page))
    await asyncio.sleep(2)
    page.go("/login")

    def route_change(e):
        page.views.clear()

        route = page.route.split("?")[0]
        params = dict(p.split("=") for p in page.route.split("?")[1:] if "=" in p)

        email = params.get("email", "")

        if route == "/signup":
            page.views.append(signup_screen(page))
        elif route == "/login":
            page.views.append(login_screen(page))
        elif route == "/terms1":
            page.views.append(terms1_screen(page))
        elif route == "/terms2":
            page.views.append(terms2_screen(page))
        elif route == "/terms3":
            page.views.append(terms3_screen(page))
        elif route == "/email_verification_sent":
            page.views.append(email_verification_sent_screen(page, email))
        elif route == "/email_verified":
            page.views.append(email_verified_screen(page, email))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
