import os.path
import tkinter as tk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_events(creds):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return "No upcoming events found."

        event_list = []
        # Build a list of event summaries
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_list.append(f"{start}: {event['summary']}")

        return "\n".join(event_list)

    except HttpError as error:
        return f"An error occurred: {error}"

def display_calendar_on_screen(events_text):
    root = tk.Tk()
    root.title("Google Calendar")

    label = tk.Label(root, text=events_text, justify="left", padx=10, pady=10)
    label.pack()

    root.mainloop()

def main():
    # Load the client secret JSON file
    client_secret_file = r"C:\Users\thoma\OneDrive\Desktop\Calendar code API\client_secret_799663632067-fq9t9eim22l18r3a2hkdi86e6gbbgibn.apps.googleusercontent.com.json"  

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                client_secret_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    events_text = get_calendar_events(creds)
    display_calendar_on_screen(events_text)

if __name__ == "__main__":
    main()

