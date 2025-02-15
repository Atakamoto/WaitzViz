# Waitz Data Scraper (for UCSD Building Availability Information)

This project retrieves real-time occupancy data from the **Waitz API** which contains information about how crowded places like Geisel Library and RIMAC are and uploads it to **Google Sheets** using an AWS Lambda function. The script extracts location names, occupancy percentages, and open/closed status while also recording timestamps for tracking trends over time.

## Features

- **Extracts real-time occupancy data** from the Waitz API.
- **Formats the data** with location names, occupancy percentages, and open status.
- **Uploads data to Google Sheets** via the Google Sheets API.
- **Runs automatically** using AWS Lambda.

## Future Plans

- **Create visualizations based on data once enough is collected**
- **Work on live updating calendar or visuals for website**
