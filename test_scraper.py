from scraper import EconomicCalendarScraper

def test_scraper():
    scraper = EconomicCalendarScraper()
    events = scraper.get_calendar_data()
    
    print("\nTest Results:")
    print(f"Total US events found: {len(events)}")
    
    if events:
        print("\nFirst event details:")
        print(f"Name: {events[0]['name']}")
        print(f"Time: {events[0]['time']}")
        print(f"Impact: {events[0]['impact']}")
        print(f"Previous: {events[0]['previous']}")
        print(f"Forecast: {events[0]['forecast']}")

if __name__ == "__main__":
    test_scraper()
