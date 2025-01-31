import os
import requests
import icalendar
import yaml
from datetime import datetime, date, timedelta
from flair_api import make_client
from dotenv import load_dotenv

load_dotenv()

def is_occupied(target_date, ical_url):
    """
    Checks if a given date is occupied based on events from an iCal URL.

    Parameters:
    target_date (datetime.date): The date to check for events.
    ical_url (str): URL of the iCal file.

    Returns:
    bool: True if the date is occupied, False otherwise.

    Raises:
    Exception: If there is an error fetching or processing the iCal file.
    """
    # Fetch the iCal file
    response = requests.get(ical_url)
    response.raise_for_status()

    # Parse the iCal file
    calendar = icalendar.Calendar.from_ical(response.text)
    print(f"Parsed: {response.text}")

    # Check events in the calendar
    for component in calendar.walk():
        if component.name == "VEVENT":
            start_date = component.get("dtstart").dt
            end_date = component.get("dtend").dt
            summary = component.get("summary")

            # Normalize to date if datetime
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            if isinstance(end_date, datetime):
                end_date = end_date.date()

            # Debug print statement for each event
            print(f"Event: Start = {start_date}, End = {end_date}, Summary = {summary}")

            # Check if the target date is within the event's range (excluding checkout day) and summary is "Reserved"
            if start_date <= target_date < end_date and summary != "Airbnb (Not available)":
                return True
            
    return False

def set_rooms(flair_client, temp_c, occupied):
    print("Getting structure details")
    structures = flair_client.get('structures')
    until = datetime.utcnow() + timedelta(days=2)
    formatted_date = until.isoformat() + "+00:00"

    print(f"Setting rooms to {'occupied' if occupied else 'unoccupied'} with set point {temp_c}°C.")
    for structure in structures:
        print(f'Structure: {structure.attributes["name"]}')
        rooms = structure.get_rel("rooms")

        for room in rooms:
            room.update(attributes={"set-point-c": temp_c, "hold-until": formatted_date, "active": occupied})
            print(f"Updated room {room.attributes['name']} to {'occupied' if occupied else 'unoccupied'} with set point {temp_c}°C until {formatted_date}")

if __name__ == "__main__":
    ical_url = os.getenv("ICAL_URL")

    if not ical_url:
        raise SystemExit("Fatal Error: Calendar URL is not set in config.yml.")
    
    flair_client_id = os.getenv("FLAIR_CLIENT_ID")
    flair_client_secret = os.getenv("FLAIR_CLIENT_SECRET")

    print(f"Flair Client ID: {flair_client_id} / Secret: {flair_client_secret}")
    
    # True if there is any value for FLAIR_CLIENT_USE_OAUTH_2, False otherwise
    flair_client_use_oauth_2 = bool(os.getenv("FLAIR_CLIENT_USE_OAUTH_2"))

    if flair_client_use_oauth_2:
        print("Using OAuth 2 for Flair API.")
        
    if not flair_client_id or not flair_client_secret:
        raise SystemExit("Fatal Error: Flair API credentials not set in environment variables, FLAIR_CLIENT_ID and FLAIR_CLIENT_SECRET.")

    flair_client = make_client(flair_client_id, flair_client_secret, 'https://api.flair.co/', use_oauth_2=flair_client_use_oauth_2)

    away_temp_c = float(os.getenv("AWAY_TEMP_C") or 10)
    occupied_temp_c = float(os.getenv("OCCUPIED_TEMP_C") or 18.34)

    # # Check if today is occupied

    today = date.today()
    try:
        occupied = is_occupied(today, ical_url)
    except Exception as e:
        print("AirBNB Error: ", e)
        raise SystemExit(f"AirBNB Error: {e}")
    
    try:
        if occupied:
            print("The calendar shows occupied for today.")
            set_rooms(flair_client, occupied_temp_c, True)
        else:
            print("The calendar does not show occupied for today.")
            set_rooms(flair_client, away_temp_c, False)
    except Exception as e:
        print("Flair Error: ", e, e.json)
        raise SystemExit(f"Flair Error: {e}")