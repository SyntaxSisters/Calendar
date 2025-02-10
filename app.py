import flet as ft
import calendar

# creating calendar for year and month
def create_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    header = ft.Row(
        [ft.Text(day, size=24, width=60, text_align=ft.TextAlign.CENTER) 
            for day in weekdays]
    )

    days_grid = []
    for week in cal:
        days_grid.append(
            ft.Row([ft.Text(str(day) if day != 0 else "", size=24, width=60, text_align=ft.TextAlign.CENTER) 
                for day in week])
        )
    
    return header, days_grid

#main function what it gets outputted why is it like this i don't know but it's annoying..
def main(page):

    #just for base 
    current_year = 2025
    current_month = 2

    # function to switch through months
    def update_calendar():
        # remove old content
        page.controls.clear()
        
        # new calendar
        header, days_grid = create_calendar(current_year, current_month)
        
        # calendar layout
        calendar_column = ft.Column(
            [header] + days_grid, alignment=ft.MainAxisAlignment.START
        )

        # become one page
        page.add(
            ft.Row([
                #possible side panel
                ft.Column(
                    [ft.Text("Column on Left", size=20)], width=200),  
                ft.Column([calendar_column], width=800)
            ], alignment=ft.MainAxisAlignment.START)
        )

        #become one navigation bar
        page.add(
            ft.Row([
                ft.IconButton(ft.icons.ARROW_LEFT, on_click=prev_month, tooltip="Previous Month", width=40),
                ft.Text(f"{calendar.month_name[current_month]} {current_year}", size=18),
                ft.IconButton(ft.icons.ARROW_RIGHT, on_click=next_month, tooltip="Next Month", width=40),
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # change the month
    def prev_month(e):
        nonlocal current_month, current_year
        # previous month
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
        update_calendar()

    def next_month(e):
        nonlocal current_month, current_year
        # next month
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1
        update_calendar()

    # calendar display
    update_calendar()

# work app pls don't crash..
ft.app(target=main)
