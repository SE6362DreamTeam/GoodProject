import requests
from bs4 import BeautifulSoup
import app.db_map
import app.db
from sqlalchemy.orm import sessionmaker
from app.db import db
from flask import current_app
import re




class Web_Scraper:

    def __init__(self):
        # Initialization code if needed
        self.noise_words = {"the", "is", "in", "at", "of", "and", "a", "to", "on", "with", "as", "for", "it", "was",
                             "by", "be", "has", "had", "that", "which", "so", "but", "or", "if", "not", "are", "were",
                               "we", "he", "she", "they", "them", "their", "our", "his", "her", "who", "will", "can",
                                 "could", "would", "about", "above", "after", "again", "against", "all", "am", "an",
                                   "any", "because", "been", "before", "being", "below", "between", "both", "during",
                                     "each", "how", "its", "itself", "just", "like", "more", "most", "now", "other",
                                       "over", "same", "some", "such", "than", "then", "there", "these", "this", "those",
                                         "through", "up", "very", "what", "when", "where", "why", "your", "&"}


        pass

        self.char_replacements = {
            'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a', 'ã': 'a', 'å': 'a', 'æ': 'ae',
            'ç': 'c', 'č': 'c', 'ć': 'c',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ě': 'e', 'ē': 'e', 'ė': 'e', 'ę': 'e',
            'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i', 'ī': 'i', 'į': 'i',
            'ñ': 'n', 'ń': 'n',
            'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'o', 'œ': 'oe',
            'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u', 'ū': 'u', 'ų': 'u', 'ű': 'u',
            'ý': 'y', 'ÿ': 'y',
            'ß': 'ss', 'þ': 'th', 'ð': 'd', 'ł': 'l', 'ø': 'o',
        }





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
                page_text = page_text.replace('\t', ' ')  # Replace tabs with spaces

                # Split by new lines and remove empty lines
                lines = page_text.split('$')
                cleaned_lines = [line.strip() for line in lines if line.strip()]

                # Remove noise words from each line
                cleaned_lines = [self.remove_noise_words(line) for line in cleaned_lines]

                # Remove lines without any letters
                cleaned_lines = self.remove_empty_lines(cleaned_lines)

                # Replace non-English characters with their English equivalents
                cleaned_lines = [self.replace_non_english_characters(line) for line in cleaned_lines]

                # Join cleaned lines back with a single newline separator
                cleaned_text = '$'.join(cleaned_lines)

                return cleaned_text

            else:
                print(f"Failed to fetch page {url}, status code: {response.status_code}")
                return "None"

        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return "None"



    def replace_non_english_characters(self, text):
        """Replaces non-English letters with their English equivalents."""
        for char, replacement in self.char_replacements.items():
            text = text.replace(char, replacement)
        return text

    def remove_noise_words(self, text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.noise_words]
        return ' '.join(filtered_words).strip()

    def remove_empty_lines(self, lines):
        return [line for line in lines if re.search(r'[a-zA-Z]', line)]


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








