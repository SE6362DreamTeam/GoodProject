import requests
from bs4 import BeautifulSoup
import app.db_map
import app.db
from sqlalchemy.orm import sessionmaker




class Web_Scraper:

    def __init__(self):
        self.Session = sessionmaker(bind=app.db.get_engine())




    def get_urls_from_database(self):

        session = self.Session()

        try:
            url_results = session.query(app.URLs).all()

            url_list = []

            for result in url_results:
                url_data ={
                    'id': result.url_id,
                    'search_term': result.search_term,
                    'url': result.url

                }
                url_list.append(url_data)

            return url_list

        finally:
            session.close()





    def scrape_webpage(self, url):

        try:
            # get web page content
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the page content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract all the text from the page
                page_text = soup.get_text(separator=' ', strip=True)

                return page_text

            else:
                return None

        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return None





    def send_scraped_text_to_database(self):
        session = self.Session()

        try:
            url_list = self.get_urls_from_database()

            for url_data in url_list:
                url_id = url_data['id']
                url = url_data['url']

                scraped_text = self.scrape_webpage(url)

                if scraped_text:
                    # Create a new ScrapedData object
                    scraped_data = app.ScrapedData(
                        url_id=url_id,
                        scraped_text=scraped_text
                    )

                    # Add the scraped data to the session
                    session.add(scraped_data)


            session.commit()

        finally:
            # Always close the session
            session.close()



