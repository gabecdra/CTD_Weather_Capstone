# CTD Weather Capstone

## Summary
Scrapes weather data from timeanddate.com using Selenium, cleans it with Pandas, 
stores it in SQLite, and displays it in a Streamlit dashboard.

## Setup
1. Clone the repo
2. Create virtual environment: `python3.11 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Run scraper: `python Scraper.py`
6. Run cleaner: `python Cleaner.py`
7. Load to database: `python load_to_sqlite.py`
8. Run dashboard: `streamlit run streamlit_app.py`

## Screenshot
![Dashboard Screenshot](screenshot.png)

## Files
- `Scraper.py` - Web scraping
- `Cleaner.py` - Data cleaning
- `load_to_sqlite.py` - Database loading
- `streamlit_app.py` - Dashboard
