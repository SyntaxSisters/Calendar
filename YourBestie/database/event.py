from datetime import datetime, date
import uuid
import flet as ft
from typing import Any
from database.pdf_handler import get_recommendations2

class calendar_event:
    def __init__(
        self,
        start_date: date,
        start_time: str,
        end_time: str,
        tags: list[str],
        title: str,
        location: str,
        attachments: list[str],
        color: str = "#000000"
    ):
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags
        self.title = title
        self.location = location
        self.id = uuid.uuid4()
        self.attachments = attachments
        self.color = color
        self.pdf_summary = self.process_pdf_summary(attachments)

    def process_pdf_summary(self, attachments: list[str]) -> str:
        if attachments:
            filename = attachments[0]
            top_words = get_recommendations2(filename)
            print(f"📄 PDF Analysis - {filename}: {top_words}")
            return f"{filename} is attached"
        return "No PDF provided"


class calendar_events:
    events: list["calendar_event"] = []

    @staticmethod
    def get_events_for_day(day: date) -> list["calendar_event"]:
        return [ev for ev in calendar_events.events if ev.start_date == day]

    @staticmethod
    def delete_event(event_id: str):
        """Remove the event with the given ID from the global events list."""
        calendar_events.events = [
            ev for ev in calendar_events.events
            if str(ev.id) != event_id
        ]

    @staticmethod
    def show_create_event_popup(e, selected_date: date, refresh_ui_callback: callable):
        """
        Opens a 'Create Event' dialog with extra spacing,
        a single 'Location' field, and top 5 PDF words placed in 'Tags'.
        """
        start_time_field = ft.TextField(value="00:00", label="Start Time (HH:MM)")
        end_time_field = ft.TextField(value="23:59", label="End Time (HH:MM)")
        tags_field = ft.TextField(value="", label="Tags (comma-separated)")
        title_field = ft.TextField(value="", label="Title", hint_text="Enter a title")

        location_field = ft.TextField(value="", label="Location", hint_text="Enter an address")
        color_field = ft.TextField(value="#FF0000", label="Color (e.g. 'red' or '#FF0000')")

        attachments: list[str] = []

        def handle_file_upload(file_picker_event: ft.FilePickerResultEvent):
            if file_picker_event.files and len(file_picker_event.files) > 0:
                picked_file = file_picker_event.files[0]
                pdf_path = picked_file.path
                attachments.clear()
                attachments.append(pdf_path)

                # extract top 5 words from the PDF
                top_words = get_recommendations2(pdf_path)
                print(f"PDF top 5 words: {top_words}")

                # put those words into the Tags field
                tags_field.value = ", ".join(top_words)
                tags_field.update()

                upload_status.value = f"1 file attached: {picked_file.name}"
                upload_status.update()

        file_picker = ft.FilePicker(on_result=handle_file_upload)
        upload_button = ft.ElevatedButton(
            "Upload PDF",
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.ANY,
                allowed_extensions=["pdf"]
            ),
        )
        upload_status = ft.Text(value="No files uploaded.", size=12, color=ft.Colors.ON_SURFACE)

        def is_valid_time_format(time_str):
            try:
                datetime.strptime(time_str, "%H:%M")
                return True
            except ValueError:
                return False

        def create_event(_):
            s_time = start_time_field.value.strip()
            e_time = end_time_field.value.strip()

            # Time check
            if not (is_valid_time_format(s_time) and is_valid_time_format(e_time)):
                start_time_field.error_text = "Invalid time format (HH:MM required)"
                end_time_field.error_text = "Invalid time format (HH:MM required)"
                start_time_field.update()
                end_time_field.update()
                return

            tags = [t.strip() for t in tags_field.value.split(",")] if tags_field.value else []
            title = title_field.value.strip() if title_field.value else "Untitled Event"
            loc_value = location_field.value.strip() if location_field.value else ""
            color_value = color_field.value.strip() or "#000000"

            new_event = calendar_event(
                start_date=selected_date,
                start_time=s_time,
                end_time=e_time,
                tags=tags,
                title=title,
                location=loc_value,
                attachments=attachments,
                color=color_value
            )
            calendar_events.events.append(new_event)

            # close the dialog
            dlg_model.open = False
            e.control.page.update()
            refresh_ui_callback()

            # clear  popups
            e.control.page.overlay.clear()
            e.control.page.update()

        dlg_model = ft.AlertDialog(
            title=ft.Text("Create Event"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        title_field,
                        start_time_field,
                        end_time_field,
                        tags_field,
                        location_field,
                        color_field,
                        ft.Row([upload_button, upload_status]),
                    ],
                    spacing=25  # extra spacing between fields
                ),
                padding=ft.padding.all(30),  # bigger padding around content
                width=900,
                height=650
            ),
            actions=[
                ft.TextButton("Create Event", on_click=create_event),
                ft.TextButton("Cancel", on_click=lambda ev: close_dialogue(ev))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=ft.padding.only(top=20),  # space above the buttons
            on_dismiss=lambda ev: close_dialogue(ev),
        )

        def close_dialogue(_):
            dlg_model.open = False
            e.control.page.update()

        def open_dialogue(_):
            e.control.page.overlay.append(file_picker)
            e.control.page.controls.append(dlg_model)
            dlg_model.open = True
            e.control.page.update()

        open_dialogue(e)

    @staticmethod
    def show_view_event_popup(e, ev_obj: "calendar_event"):
        """
        Displays a read-only dialog with the event's info:
        Title, Start/End times, Tags, Location, Color, PDF summary.
        """
        page = e.control.page

        title_text = ft.Text(f"Title: {ev_obj.title}")
        start_text = ft.Text(f"Start Time: {ev_obj.start_time}")
        end_text = ft.Text(f"End Time: {ev_obj.end_time}")
        tags_text = ft.Text(f"Tags: {', '.join(ev_obj.tags)}")
        location_text = ft.Text(f"Location: {ev_obj.location}")
        color_text = ft.Text(f"Color: {ev_obj.color}")
        pdf_text = ft.Text(f"PDF Summary: {ev_obj.pdf_summary}")

        def close_view_dialog(_):
            view_dlg.open = False
            page.update()

        view_dlg = ft.AlertDialog(
            title=ft.Text("View Event"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        title_text,
                        start_text,
                        end_text,
                        tags_text,
                        location_text,
                        color_text,
                        pdf_text,
                    ],
                    spacing=10
                ),
                padding=20,
                width=450
            ),
            actions=[
                ft.TextButton("Close", on_click=close_view_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.controls.append(view_dlg)
        view_dlg.open = True
        page.update()
