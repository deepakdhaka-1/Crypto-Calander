<div align="center">

# 🚀 CryptoCraft Scraper

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python"/>
<img src="https://img.shields.io/badge/Playwright-✅-green" alt="Playwright"/>
<img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status"/>
<img src="https://img.shields.io/badge/CryptoCraft-🌐-orange" alt="CryptoCraft"/>

</div>

---

## 📌 Overview
CryptoCraft Scraper is a Python-based automation tool that uses **Playwright** to scrape the latest Calenders from **CryptoCraft** and saves the data directly into **Google Sheets** for real-time tracking.  

---

## ⚡ Features
- 🔎 Scrapes live data from [CryptoCraft](https://cryptocraft.com/)
- 📄 Extracts titles, previews, timestamps, and links
- 📊 Stores results automatically in Google Sheets
- ⏰ Runs every hour using Linux `screen` or `cron`
- 🛡️ Lightweight and customizable

---

## 🛠️ Requirements
- Python **3.8+**
- A Google Cloud **Service Account** with Sheets API enabled
- Installed dependencies:
  ```bash
  pip install playwright gspread oauth2client google-auth google-api-python-client
  playwright install
