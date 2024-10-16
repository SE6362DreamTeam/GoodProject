import requests
from bs4 import BeautifulSoup
import app.db_map
import app.db
from sqlalchemy.orm import sessionmaker
from app.db import db
from flask import current_app





class Web_Scraper:

    def __init__(self):
        # Initialization code if needed
        pass





    def get_urls_from_database(self):
        with current_app.app_context():
            # Access Flask's db.session within the app context
            url_results = db.session.query(app.db_map.URLs).all()

            url_list = []
            for result in url_results:
                url_data = {
                    'id': result.url_id,
                    'search_term': result.search_term,
                    'url': result.url
                }
                url_list.append(url_data)

            return url_list



    def scrape_webpage(self, url, url_id):


        try:
            # Fetch the web page content
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract text with newline separators and remove tabs
                page_text = soup.get_text(separator='$', strip=True)
                page_text = page_text.replace('\t', ' ')  # Replace tabs with space

                # Split by new lines and remove empty lines
                lines = page_text.split('$')
                cleaned_lines = [line.strip() for line in lines if line.strip()]

                # Join cleaned lines back with a single newline separator
                cleaned_text = '$'.join(cleaned_lines)

                return cleaned_text

            else:
                print(f"Failed to fetch page {url}, status code: {response.status_code}")
                return "None"



        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return "None"





    def send_scraped_text_to_database(self):
        try:
            with current_app.app_context():
                url_list = self.get_urls_from_database()

                for url_data in url_list:
                    url_id = url_data['id']
                    url = url_data['url']



                    already_scraped = db.session.query(app.db_map.ScrapedData).filter_by(url_id=url_id).first()

                    if already_scraped:
                        continue
                    else:
                        # Scrape the webpage content

                        scraped_text = self.scrape_webpage(url, url_id)
                        print(f"Web page \"{url}\" has been scraped.")


                    if scraped_text:
                        # Create and store the ScrapedData object
                        scraped_data = app.db_map.ScrapedData(url_id=url_id,scraped_text=scraped_text)
                        db.session.add(scraped_data)

                # Commit the session after adding all scraped data
                db.session.commit()

        except Exception as e:
            db.session.rollback()  # Rollback on error
            print(f"Error during database commit: {str(e)}")

        finally:
            # No need to close session; Flask-SQLAlchemy handles that
            pass








