import threading
import time
import requests
from datetime import datetime
from app.db_map import URLs
from app.db import db

_thread_running = False

def check_urls_periodically(app):
    """Background task to check URLs weekly and remove inactive ones."""
    global _thread_running
    if _thread_running:
        print("[Background Task] Thread already running. Exiting.")
        return
    _thread_running = True

    def run_task():
        print("Pausing for an hour before starting the URL checker...")
        time.sleep(3600)  # Pause for 1 hour

        with app.app_context():
            while True:
                print(f"[{datetime.now()}] Starting URL check...")
                urls = db.session.query(URLs).all()

                for url_entry in urls:
                    url = url_entry.url
                    try:
                        response = requests.get(url, timeout=5)
                        if response.status_code == 200:
                            print(f"[{datetime.now()}] URL is active: {url}")
                        else:
                            print(f"[{datetime.now()}] URL returned status {response.status_code}: {url}")
                    except requests.RequestException as e:
                        print(f"[{datetime.now()}] URL is inactive or unreachable: {url}, Error: {str(e)}")
                        try:
                            db.session.delete(url_entry)
                            db.session.commit()
                            print(f"[{datetime.now()}] URL removed from database: {url}")
                        except Exception as db_error:
                            db.session.rollback()
                            print(f"[{datetime.now()}] Failed to remove URL {url}: {db_error}")

                print(f"[{datetime.now()}] Sleeping for 1 week.")
                time.sleep(7 * 24 * 60 * 60)

    thread = threading.Thread(target=run_task, daemon=True)
    thread.start()
    print("[Background Task] URL checker thread started successfully.")
