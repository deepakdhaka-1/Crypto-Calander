import asyncio
import json
import time
from datetime import datetime, timedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.async_api import async_playwright


# Google Sheets setup
SHEET_URL = "https://docs.google.com/spreadshe....."
SHEET_NAME = "Calender"

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL).worksheet(SHEET_NAME)
    return sheet


async def scrape_calendar():
    today = datetime.today()
    end_date = today + timedelta(days=7)

    payload = {
        "begin_date": today.strftime("%B %d, %Y"),
        "end_date": end_date.strftime("%B %d, %Y"),
        "default_view": "this_week",
        "impacts": [3],
        "event_types": [1, 2, 3, 4, 7, 10]
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        print("🌐 Opening calendar page...")
        await page.goto("https://www.cryptocraft.com/calendar", wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)

        print("📡 Calling API inside browser...")
        data = await page.evaluate(
            """async (payload) => {
                const res = await fetch(
                    "https://www.cryptocraft.com/calendar/apply-settings/1?navigation=0",
                    {
                        method: "POST",
                        headers: {
                            "accept": "application/json, text/plain, */*",
                            "content-type": "application/json"
                        },
                        body: JSON.stringify(payload)
                    }
                );
                return await res.json();
            }""",
            payload
        )

        await browser.close()

        # Parse data
        events = []
        for day in data.get("days", []):
            date = day.get("date", "")
            for ev in day.get("events", []):
                events.append([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
                    date,
                    ev.get("name", ""),
                    ev.get("timeLabel", ""),
                    ev.get("actual", ""),
                    ev.get("previous", ""),
                    ev.get("revision", ""),
                    ev.get("forecast", "")
                ])

        return events


def write_to_sheet(events):
    sheet = get_sheet()
    headers = ["Timestamp", "Date", "Name", "Time", "Actual", "Previous", "Revision", "Forecast"]

    # Clear + rewrite everything
    sheet.clear()
    sheet.insert_row(headers, 1)

    if events:
        sheet.insert_rows(events, 2)

    print(f"✅ Wrote {len(events)} events to Google Sheet.")


def run_loop():
    while True:
        try:
            events = asyncio.run(scrape_calendar())
            write_to_sheet(events)
        except Exception as e:
            print("Error:", e)

        print("Sleeping 1 hour...\n")
        time.sleep(3600)


if __name__ == "__main__":
    run_loop()
