import flet as ft
from typing import Callable, cast
from login import show_login  

def main(page: ft.Page):
    # lock em out and show login
    show_login(page)

# it doesnt crash or duplicate guys are you proud
_ = cast(Callable[[Callable[[ft.Page], None]], None], ft.app)(main)

