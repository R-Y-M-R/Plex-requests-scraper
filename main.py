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
    print(f"Attempting to connect to Plex at: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses
        
        # Log the raw XML response content
        print("Raw XML Response:")
        print(response.text)  # Show the entire XML response
        
        print("Parsing XML data...")

        # Parse XML response
        root = ET.fromstring(response.content)
        
        history = []
        for media in root.findall("Video"):  # Adjusted to match XML structure
            title = media.get("title")
            viewed_at = media.get("viewedAt")
            library_section_id = media.get("librarySectionID")
            parent_title = media.get("parentTitle")
            grandparent_title = media.get("grandparentTitle")
            
            history.append({
                "title": title,
                "viewed_at": viewed_at,
                "library_section_id": library_section_id,
                "parent_title": parent_title,
                "grandparent_title": grandparent_title
            })
        
        return history
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ET.ParseError as parse_err:
        print(f"XML parse error: {parse_err}")

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