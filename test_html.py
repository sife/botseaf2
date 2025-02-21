import requests
import trafilatura
from bs4 import BeautifulSoup
from config import CALENDAR_URL

def test_html_structure():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("Fetching page content...")
    response = requests.get(CALENDAR_URL, headers=headers)
    response.raise_for_status()
    
    # First try with trafilatura
    downloaded = trafilatura.fetch_url(CALENDAR_URL)
    if downloaded:
        print("\nPage Content (Trafilatura):")
        text = trafilatura.extract(downloaded)
        print(text[:1000])  # Print first 1000 chars
    
    # Then check with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    us_events = soup.find_all('tr', {'class': 'js-event-item'})
    
    if us_events:
        print("\nFirst event HTML structure:")
        first_event = us_events[0]
        print(first_event.prettify()[:1000])
        
        # Try to find country info
        country_cell = first_event.find('td', {'class': 'flagCur'})
        if country_cell:
            print("\nCountry cell content:")
            print(country_cell.prettify())

if __name__ == "__main__":
    test_html_structure()
