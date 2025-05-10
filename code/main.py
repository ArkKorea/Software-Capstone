# ✅ main.py - day_diet_screen 라우트 추가 및 정리
import flet as ft
import asyncio
from urllib.parse import urlparse, parse_qs

from login import splash_content, login_screen
from sign_up import sign_up_screen
from terms_1 import terms_1_screen
from terms_2 import terms_2_screen
from terms_3 import terms_3_screen
from email_verification_sent import email_verification_sent_screen
from email_verified import email_verified_screen
from home import home_screen
from profile_view import profile_view_screen
from product_management import product_management_screen
from diet_management import diet_management_screen
from favorites import favorites_screen
from my_allergy import my_allergy_screen
from product_register import product_register_screen
from my_product_list import my_product_list_screen
from my_product_group import my_product_group_screen
from product_register_success import product_register_success_screen
from group_register import group_register_screen
from group_register_success import group_register_success_screen
from today_symptom import today_symptom_screen
from add_diet import add_diet_screen
from day_diet import day_diet_screen
from reset_password import reset_password_screen
from history import history_screen
from search_view import search_view_screen
from datetime import date

async def main(page: ft.Page):
    page.title = "ALLERT SIGN"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE

    page.clean()
    page.add(splash_content(page))
    await asyncio.sleep(2)
    page.go("/home")

    def route_change(e):
        route = page.route.split("?")[0]
        qs = parse_qs(urlparse(page.route).query)
        email = qs.get("email", [""])[0]

        page.views.clear()

        if route == "/signup":
            page.views.append(sign_up_screen(page))
        elif route == "/login":
            page.views.append(login_screen(page))
        elif route == "/terms1":
            page.views.append(terms_1_screen(page))
        elif route == "/terms2":
            page.views.append(terms_2_screen(page))
        elif route == "/terms3":
            page.views.append(terms_3_screen(page))
        elif route == "/emailverificationsent":
            page.views.append(email_verification_sent_screen(page, email))
        elif route == "/emailverified":
            page.views.append(email_verified_screen(page, email))
        elif route == "/home":
            page.views.append(home_screen(page))
        elif route == "/profileview":
            page.views.append(profile_view_screen(page))
        elif route == "/productmanagement":
            page.views.append(product_management_screen(page))
        elif route == "/dietmanagement":
            page.overlay.clear()
            page.views.append(diet_management_screen(page))
        elif route == "/favorites":
            page.views.append(favorites_screen(page))
        elif route == "/myallergy":
            page.views.append(my_allergy_screen(page))
        elif route == "/productregister":
            page.views.append(product_register_screen(page))
        elif route == "/myproductlist":
            page.views.append(my_product_list_screen(page))
        elif route == "/myproductgroup":
            page.views.append(my_product_group_screen(page))
        elif route == "/productregistersuccess":
            page.views.append(product_register_success_screen(page))
        elif route == "/groupregister":
            page.views.append(group_register_screen(page))
        elif route == "/groupregistersuccess":
            page.views.append(group_register_success_screen(page))
        elif route == "/adddiet":
            page.views.append(add_diet_screen(page))
        elif route == "/todaysymptom":
            page.views.append(today_symptom_screen(page))
        elif route == "/resetpassword":
            page.views.append(reset_password_screen(page))
        elif route == "/history":
            page.views.append(history_screen(page))
        elif route == "/searchview":
            page.views.append(search_view_screen(page))
        elif route == "/daydiet":
            date_str = qs.get("date", [None])[0]
            if date_str:
                page.views.append(day_diet_screen(page, date.fromisoformat(date_str)))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
