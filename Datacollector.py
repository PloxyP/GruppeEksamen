import requests
import time

# ThingSpeak API URL for updating a channel
url = "https://api.thingspeak.com/update"

# ThingSpeak Channel API Key (replace with your actual API Key)
api_key = "RS1DFZK1ZEULO72E"

# Code identifier (replace with the name of your code)
code = "calendar.py"
count = 0

while True:
    # Your code activation logic here
    # For example, if the code is activated, increment the count
    # Replace this logic with your actual code activation condition
    if code_activation_condition:
        count += 1

    # Prepare the data to send to ThingSpeak
    data = {
        "api_key": api_key,
        "field1": code,
        "field2": str(count)
    }

    # Send data to ThingSpeak
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

    # Wait for a specified interval (e.g., 1 minute)
    time.sleep(60)
