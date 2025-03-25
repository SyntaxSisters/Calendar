import flet as ft
from gui.window import gui
def main(page: ft.Page):
    """Entry point of application. This is called from Flet's initializer.

    Args:
        page (ft.Page): the Flet Page used to handle the window
    """
    application = gui(page)
    application._page.update() # pyright: ignore[reportUnknownMemberType,reportPrivateUsage]

_ = ft.app(main) # pyright: ignore[reportUnknownMemberType]