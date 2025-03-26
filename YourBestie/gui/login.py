import flet as ft
import subprocess

def main(page: ft.Page):
    page.title = "Syntax Sisters"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "black"

    def handle_login(event):
        subprocess.run(["python", "calendarPage.py"])
        page.close()

    login_box = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Syntax Sisters", 
                    size=30, 
                    weight=ft.FontWeight.BOLD, 
                    text_align=ft.TextAlign.CENTER,
                    color="white"
                ),
                ft.TextField(label="Username", width=250, autofocus=True),
                ft.TextField(label="Password", password=True, width=250),
                ft.ElevatedButton(
                    "Login", 
                    on_click=handle_login, 
                    bgcolor="#6200EE", 
                    color="white"
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
    )

    page.add(
        ft.Container(
            content=login_box, 
            alignment=ft.alignment.center, 
            expand=True
        )
    )

ft.app(target=main)
