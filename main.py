import requests
import xml.etree.ElementTree as ET
import json

# Replace these values with your Plex server details
PLEX_IP = "localhost"           # or the IP address of your Plex server
PLEX_PORT = "32400"
PLEX_TOKEN = "your_plex_token"  # Replace with your myPlexToken value

# URL to get watch history
url = f"http://{PLEX_IP}:{PLEX_PORT}/status/sessions/history/all?X-Plex-Token={PLEX_TOKEN}"

def get_watch_history():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful

        # Parse the XML response
        root = ET.fromstring(response.content)
        
        # Extract watched items and store details in a list
        history = []
        for media in root.findall("MediaContainer/Video"):
            title = media.get("title")
            view_count = media.get("viewCount")
            last_viewed_at = media.get("lastViewedAt")
            
            # Add each watched item to the history list as a dictionary
            history.append({
                "title": title,
                "view_count": int(view_count) if view_count else 0,
                "last_viewed_at": last_viewed_at  # Optional: Convert to a readable date format
            })
        
        return history
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def save_history_to_json(history, filename="plex_watch_history.json"):
    try:
        with open(filename, "w") as json_file:
            json.dump(history, json_file, indent=4)
        print(f"Watch history saved to {filename}")
    except IOError as e:
        print(f"Error saving to JSON file: {e}")

# Fetch and save watch history
history = get_watch_history()
if history:
    save_history_to_json(history)
else:
    print("No watch history found or unable to connect to Plex.")
