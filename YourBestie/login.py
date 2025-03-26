import flet as ft
import csv
import os
from typing import Callable, cast
from gui.window import gui  


#  loads account when app starts up

accounts = []
try:
    with open("accounts.csv", "r", encoding="utf-8") as f: #utf 8 so people can use shit like emojis too 
        reader = csv.DictReader(f)
        for row in reader:
            accounts.append(row)
except Exception as e:
    print("Error loading accounts.csv:", e)



def show_login(page: ft.Page):
    page.title = "Your Bestie Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # BIG TITLE !!!
    title_text = ft.Text(
        "Syntax Sisters: Your Bestie",
        size=40,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
    )

    # Username
    username_field = ft.TextField(
        hint_text="Username",
        width=300,
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        color=ft.colors.WHITE,
        border_color=ft.colors.WHITE,
        cursor_color=ft.colors.WHITE,
    )

    # Password 
    password_field = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        color=ft.colors.WHITE,
        border_color=ft.colors.WHITE,
        cursor_color=ft.colors.WHITE,
    )

    # wrong credentials
    error_text = ft.Text(value="", color=ft.colors.RED_400)

    def login_clicked(_):
        entered_username = username_field.value
        entered_password = password_field.value
        matched_account = None

        for acc in accounts:
            if acc["username"] == entered_username and acc["password"] == entered_password:
                matched_account = acc
                break

        if matched_account:
            # pass the user's team to the main GUI.
            team = matched_account["team"]
            page.controls.clear()
            # Launch your calendar window with the correct team
            application = gui(page, team=team)
            page.update()
        else:
            error_text.value = "Invalid credentials. Try again."
            error_text.update()

    login_button = ft.ElevatedButton(
        "Login",
        on_click=login_clicked,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor="#9b59b6",  # Purple shade
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # login screen
    login_screen = ft.Column(
        controls=[
            title_text,
            username_field,
            password_field,
            login_button,
            error_text,
        ],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(login_screen)
    page.update()
