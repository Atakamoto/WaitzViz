
import requests
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets Config
SHEET_ID = "1VHi6DhFyQmOy3MBq0YvYpRQRechfFyThzcrF2Xt0-cs"
SHEET_NAME = "Waitz Data"

# Load credentials from AWS Lambda environment variable
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# API URL
URL = "https://www.waitz.io/live/ucsd"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_waitz_data():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Failed to fetch data:", response.status_code)
        return None


def parse_location_data(loc):
    """ Extract relevant fields and format them properly """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = loc.get("name", "Unknown")
    percentage = loc.get("percentage", 0)  # Busyness percentage
    is_open = loc.get("isOpen", False)  # Open status

    return [timestamp, name, percentage, str(is_open)]  # Convert boolean to string

def upload_to_google_sheets(data):
    """ Uploads parsed data to Google Sheets """

    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    if isinstance(data, dict):
        locations = data.get("data", [])  # Extract list from dictionary
    elif isinstance(data, list):
        locations = data  # If already a list, use it directly
    else:
        raise ValueError("ERROR: Unexpected data format - Expected dict or list, got", type(data))
    parsed_data = [parse_location_data(loc) for loc in locations if isinstance(loc, dict)]

    if not parsed_data:
        print("No valid data to upload!")
        return

    # Convert to DataFrame for easy manipulation
    df = pd.DataFrame(parsed_data, columns=["Timestamp", "Name", "Busyness (%)", "Is Open"])

    # Append data to Google Sheets
    sheet.append_rows(df.values.tolist())

    print("Data successfully uploaded to Google Sheets!")

def lambda_handler(event, context):
    data = fetch_waitz_data()
    if data:
        upload_to_google_sheets(data)
    return {
        "statusCode": 200,
        "body": "Data saved to Google Sheets!"
    }








