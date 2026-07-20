import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import json
import os
import re

# URL of the ICS file
ICS_URL = "https://burnside.school.kiwi/ics/f75540d590cb0cf8656dfbd759fac6e6.ics"

def get_current_monday():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return monday.date()

def parse_calendar():
    response = requests.get(ICS_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch calendar: {response.status_code}")
    
    cal = Calendar.from_ical(response.content)
    today_monday = get_current_monday()
    
    rotation = None
    term = None
    week = None
    
    for component in cal.walk('VEVENT'):
        event_date = component.get('dtstart').dt
        
        # Check if event is on the current Monday
        if isinstance(event_date, datetime):
            event_date = event_date.date()
        
        if event_date == today_monday:
            summary = str(component.get('summary'))
            
            # Check for Week A/B
            if "Week A" in summary:
                rotation = "A"
            elif "Week B" in summary:
                rotation = "B"
            
            # Check for Term and Week
            # Format: "Term 1 - Week 2"
            match = re.search(r"Term (\d+) - Week (\d+)", summary)
            if match:
                term = match.group(1)
                week = match.group(2)
                
    return {
        "rotation": rotation,
        "term": term,
        "week": week
    }

if __name__ == "__main__":
    data = parse_calendar()
    
    # Save to JSON
    with open("current_week.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {data}")
