# main.py
import flet as ft
import asyncio
from login import splash_content, login_screen
from signup import signup_screen
from terms_1 import terms_1_screen
from terms_2 import terms_2_screen
from terms_3 import terms_3_screen
from email_verification_sent import email_verification_sent_screen
from email_verified import email_verified_screen
from home import home_screen
from profile_view import profile_screen
from productmanagement import product_management_screen  # ✅ 추가

async def main(page: ft.Page):
    page.title = "ALLERT SIGN"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

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
        elif route == "/terms_1":
            page.views.append(terms_1_screen(page))
        elif route == "/terms_2":
            page.views.append(terms_2_screen(page))
        elif route == "/terms_3":
            page.views.append(terms_3_screen(page))
        elif route == "/email_verification_sent":
            page.views.append(email_verification_sent_screen(page, email))
        elif route == "/email_verified":
            page.views.append(email_verified_screen(page, email))
        elif route == "/home":
            page.views.append(home_screen(page))
        elif route == "/profile":
            page.views.append(profile_screen(page))
        elif route == "/productmanagement":  # ✅ 추가
            page.views.append(product_management_screen(page))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
