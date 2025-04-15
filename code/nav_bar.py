# nav_bar.py
import flet as ft

def nav_bar(page: ft.Page, current_route: str):
    def is_selected(route):
        return current_route == route

    def nav_icon(icon, label, route):
        selected = is_selected(route)
        color = ft.Colors.GREEN if selected else ft.Colors.BLUE_GREY
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route),
            content=ft.Column(
                [
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(label, size=11, color=color)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=ft.Padding(top=8, bottom=8, left=8, right=8),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nav_icon(ft.Icons.HOME, "Home", "/home"),
                nav_icon(ft.Icons.SEARCH, "Search", "/search"),

                ft.Container(
                    content=ft.FloatingActionButton(
                        icon=ft.Icons.QR_CODE_SCANNER,
                        bgcolor=ft.Colors.GREEN,
                        mini=True,
                        height=40,
                        width=40
                    ),
                    margin=ft.margin.only(top=-10)
                ),

                nav_icon(ft.Icons.HISTORY, "History", "/history"),
                nav_icon(ft.Icons.PERSON_OUTLINE, "Profile", "/profile")
            ]
        ),
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        height=65
    )
