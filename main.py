import asyncio
import json
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright


async def scrape_calendar():
    # Dates
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

        # Step 1: Go to calendar page (let Cloudflare JS run)
        print("🌐 Opening calendar page...")
        await page.goto("https://www.cryptocraft.com/calendar", wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)  # wait for Cloudflare to finish

        # Step 2: Call the API *inside* the browser session
        print("📡 Calling API inside browser...")
        result = await page.evaluate(
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

        print("✅ Scraped Data at", datetime.now())
        print(json.dumps(result, indent=2))

        await browser.close()


def run_loop():
    while True:
        try:
            asyncio.run(scrape_calendar())
        except Exception as e:
            print("Error:", e)

        print("Sleeping 1 hour...\n")
        time.sleep(3600)


if __name__ == "__main__":
    run_loop()
