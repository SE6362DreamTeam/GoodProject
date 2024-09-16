import requests
from bs4 import BeautifulSoup

# This code was generated with assistance from ChatGPT, a large language model created by OpenAI.
# Citation: OpenAI. (2024). ChatGPT (September 2024 version) [Large language model]. https://chat.openai.com/
def scrape_webpage(url):

    # get web page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the text from the page
        page_text = soup.get_text(separator=' ', strip=True)

        return page_text
