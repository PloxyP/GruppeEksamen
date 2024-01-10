import requests

# Define your Teamup API URL and API key
api_url = "https://api.teamup.com"
api_key = "699e02c0555e1804ea722d893851875e8444e8bf17199c8d8e46bc393a60f960"

# Specify the calendar key from the URL
calendar_key = "kskp2dg3mpgu24n3ww"

# Create the API request URL
request_url = f"{api_url}/{calendar_key}/events"

# Set up headers with your API key
headers = {
    "Teamup-Token": api_key
}

# Make the API request to retrieve calendar events
response = requests.get(request_url, headers=headers)

if response.status_code == 200:
    calendar_data = response.json()
    # Process and display the calendar data as you like
    print(calendar_data)
else:
    print(f"Failed to retrieve calendar data. Status code: {response.status_code}")
    print(response.text)  # Print the response content for debugging
