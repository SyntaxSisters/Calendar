import csv
import os
import uuid
from datetime import datetime, date
import flet as ft
from typing import Any
from database.pdf_handler import get_recommendations2

# CSV file name for events, called it events_data.csv 
CSV_FILE = "events_data.csv"

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
        color: str = "#000000",
        team_name: str = "",
        pdf_summary: str = ""
    ):
        """
        A  calendar event, optionally with PDF analysis.
        """
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags
        self.title = title
        self.location = location
        self.id = uuid.uuid4()
        self.attachments = attachments
        self.color = color
        self.team_name = team_name

        # if no pdf_summary , run PDF analysis automatically (i dont remember what this does guys help)
        if pdf_summary:
            self.pdf_summary = pdf_summary
        else:
            self.pdf_summary = self.process_pdf_summary(attachments)

    def process_pdf_summary(self, attachments: list[str]) -> str:
        if attachments:
            filename = attachments[0]
            top_words = get_recommendations2(filename)
            print(f"📄 PDF Analysis - {filename}: {top_words}")
            return f"{filename} is attached"
        return "No PDF provided"

class calendar_events:
    #list of all events
    events: list["calendar_event"] = []

    @staticmethod
    def get_events_for_day(day: date, team: str) -> list["calendar_event"]:
        """
        Return events for the given date, filtered by team:
        - If team == "admin", return all events for that date.
        - Otherwise, only return events whose team_name matches the user's team.
        """
        if team.lower() == "admin":
            return [ev for ev in calendar_events.events if ev.start_date == day]
        else:
            return [
                ev for ev in calendar_events.events
                if ev.start_date == day and ev.team_name.lower() == team.lower()
            ]

    @staticmethod
    def delete_event(event_id: str):
        """
        Remove the event with the given ID from memory, then save CSV.
        """
        calendar_events.events = [
            ev for ev in calendar_events.events
            if str(ev.id) != event_id
        ]
        calendar_events.save_to_csv()

    @staticmethod
    def show_create_event_popup(e, selected_date: date, refresh_ui_callback: callable):
        """
        Opens a 'Create Event' dialog (for Admin only)
        - Single 'Location' field
        - 'Team Name' field
        - PDF analysis -> top 5 words to tags
        - Saves to CSV
        """
        start_time_field = ft.TextField(value="00:00", label="Start Time (HH:MM)")
        end_time_field = ft.TextField(value="23:59", label="End Time (HH:MM)")
        tags_field = ft.TextField(value="", label="Tags (comma-separated)")
        title_field = ft.TextField(value="", label="Title", hint_text="Enter a title")
        location_field = ft.TextField(value="", label="Location", hint_text="Enter an address")
        color_field = ft.TextField(value="#FF0000", label="Color (e.g. 'red' or '#FF0000')")
        team_field = ft.TextField(value="", label="Team Name", hint_text="e.g. 'Guests'")
        attachments: list[str] = []

        def handle_file_upload(fp_event: ft.FilePickerResultEvent):
            if fp_event.files and len(fp_event.files) > 0:
                picked_file = fp_event.files[0]
                pdf_path = picked_file.path
                attachments.clear()
                attachments.append(pdf_path)

                #  PDF handle it -> top 5 words go into 'tags_field'
                top_words = get_recommendations2(pdf_path)
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

            # time check so its not <0 or 25<
            if not (is_valid_time_format(s_time) and is_valid_time_format(e_time)):
                start_time_field.error_text = "Invalid time format (HH:MM required)"
                end_time_field.error_text = "Invalid time format (HH:MM required)"
                start_time_field.update()
                end_time_field.update()
                return

            tags = [t.strip() for t in tags_field.value.split(",")] if tags_field.value else []
            title = title_field.value.strip() or "Untitled Event"
            loc_value = location_field.value.strip() or ""
            color_value = color_field.value.strip() or "#000000"
            team_value = team_field.value.strip() or ""

            # build the new event
            new_event = calendar_event(
                start_date=selected_date,
                start_time=s_time,
                end_time=e_time,
                tags=tags,
                title=title,
                location=loc_value,
                attachments=attachments,
                color=color_value,
                team_name=team_value
            )
            
            calendar_events.events.append(new_event)
            # Save to CSV
            calendar_events.save_to_csv()

            # Close dialog
            dlg_model.open = False
            e.control.page.update()
            refresh_ui_callback()

            # Clear popups
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
                        ft.Row([color_field, team_field], spacing=20),
                        ft.Row([upload_button, upload_status]),
                    ],
                    spacing=20
                ),
                padding=20,
                width=800,
                height=500,
            ),
            actions=[
                ft.TextButton("Create Event", on_click=create_event),
                ft.TextButton("Cancel", on_click=lambda __: close_dialogue(__))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda __: close_dialogue(__),
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
        Displays a read-only dialog with the event's info (including location, color, team, PDF summary).
        Both Admin and non-admin can view.
        """
        # I FUCKING HATE COMMENTS I HATE COMMENTS WHY DO I HAVE TO D THIS SHIT I DONT EVEN KNOW HOW IT WORKS BRO
        page = e.control.page

        title_text = ft.Text(f"Title: {ev_obj.title}")
        start_text = ft.Text(f"Start Time: {ev_obj.start_time}")
        end_text = ft.Text(f"End Time: {ev_obj.end_time}")
        tags_text = ft.Text(f"Tags: {', '.join(ev_obj.tags)}")
        location_text = ft.Text(f"Location: {ev_obj.location}")
        color_text = ft.Text(f"Color: {ev_obj.color}")
        team_text = ft.Text(f"Team Name: {ev_obj.team_name}")
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
                        team_text,
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

    @staticmethod
    def save_to_csv():
        """
        Overwrite the CSV file with the current list of events.
        We store: id, start_date, start_time, end_time, tags, title,
                  location, color, team_name, attachments, pdf_summary
        """
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "start_date", "start_time", "end_time",
                "tags", "title", "location", "color",
                "team_name", "attachments", "pdf_summary"
            ])
            for ev in calendar_events.events:
                writer.writerow([
                    str(ev.id),
                    ev.start_date.isoformat(),
                    ev.start_time,
                    ev.end_time,
                    ";".join(ev.tags),
                    ev.title,
                    ev.location,
                    ev.color,
                    ev.team_name,
                    ";".join(ev.attachments),
                    ev.pdf_summary.replace("\n", " ").replace("\r", ""),
                ])

    @staticmethod
    def load_from_csv():
        """
        If CSV exists, load all events into memory.
        """
        if not os.path.exists(CSV_FILE):
            return

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                return

            calendar_events.events.clear()

            for row in reader:
                if len(row) < 11:
                    continue
                ev_id_str       = row[0]
                start_date_str  = row[1]
                start_time      = row[2]
                end_time        = row[3]
                tags_str        = row[4]
                title           = row[5]
                location        = row[6]
                color           = row[7]
                team_name       = row[8]
                attachments_str = row[9]
                pdf_summary     = row[10]

                try:
                    start_date = date.fromisoformat(start_date_str)
                except ValueError:
                    start_date = date.today()

                tags_list = [t.strip() for t in tags_str.split(";")] if tags_str else []
                attachments_list = [a.strip() for a in attachments_str.split(";")] if attachments_str else []

                ev = calendar_event(
                    start_date=start_date,
                    start_time=start_time,
                    end_time=end_time,
                    tags=tags_list,
                    title=title,
                    location=location,
                    attachments=attachments_list,
                    color=color,
                    team_name=team_name,
                    pdf_summary=pdf_summary
                )
                try:
                    ev.id = uuid.UUID(ev_id_str)
                except ValueError:
                    pass

                calendar_events.events.append(ev)

# load events 
calendar_events.load_from_csv()
