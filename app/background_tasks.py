import threading
import time
import requests
from datetime import datetime
from app.db_map import URLs
from app.db import db

# Flag to ensure the thread runs only once
_thread_running = False

def check_urls_periodically(app):
    """Background task to check URLs weekly and remove inactive ones."""
    global _thread_running
    if _thread_running:  # If thread is already running, exit
        return
    _thread_running = True

    with app.app_context():
        while True:
            print(f"[{datetime.now()}] Starting URL check...")

            # Query all URLs from the database
            urls = db.session.query(URLs).all()

            for url_entry in urls:
                url = url_entry.url
                try:
                    # Ping the URL with a timeout
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        print(f"[{datetime.now()}] URL is active: {url}")
                    else:
                        print(f"[{datetime.now()}] URL returned status {response.status_code}: {url}")
                except requests.RequestException as e:
                    print(f"[{datetime.now()}] URL is inactive or unreachable: {url}, Error: {str(e)}")
                    try:
                        # Delete the URL entry if it is unreachable
                        db.session.delete(url_entry)
                        db.session.commit()
                        print(f"[{datetime.now()}] URL removed from database: {url}")
                    except Exception as db_error:
                        db.session.rollback()
                        print(f"[{datetime.now()}] Failed to remove URL {url}: {db_error}")

            # Wait for 1 week (in seconds)
            time.sleep(7 * 24 * 60 * 60)
