import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from config import CALENDAR_URL

class EconomicCalendarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_calendar_data(self):
        try:
            print("Fetching calendar data from investing.com...")
            response = requests.get(CALENDAR_URL, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all event rows
            rows = soup.find_all('tr', {'class': 'js-event-item'})
            print(f"Found {len(rows)} total events, filtering for US events...")

            events = []
            for row in rows:
                try:
                    # Check if it's a US event by looking for the US flag span
                    us_flag = row.find('span', {'class': 'ceFlags United_States'})
                    if not us_flag:
                        continue

                    # Extract event details
                    time_cell = row.find('td', {'class': 'time'})
                    event_cell = row.find('td', {'class': 'event'})

                    if not all([time_cell, event_cell]):
                        continue

                    time = time_cell.text.strip()
                    event_name = event_cell.text.strip()
                    impact = self._get_impact_level(row)

                    # Get previous and forecast values
                    prev_cell = row.find('td', {'class': 'prev'})
                    forecast_cell = row.find('td', {'class': 'fore'})

                    previous = prev_cell.text.strip() if prev_cell else "غير متوفر"
                    forecast = forecast_cell.text.strip() if forecast_cell else "غير متوفر"

                    # Convert time to datetime
                    event_time = self._parse_time(time)
                    if event_time:
                        events.append({
                            'time': event_time,
                            'name': event_name,
                            'impact': impact,
                            'previous': previous,
                            'forecast': forecast
                        })
                        print(f"Added US event: {event_name} at {event_time}")
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue

            print(f"Successfully found {len(events)} US events")
            return events

        except Exception as e:
            print(f"Error scraping calendar data: {str(e)}")
            return []

    def _get_impact_level(self, row):
        try:
            impact_cell = row.find('td', {'class': 'sentiment'})
            if not impact_cell:
                return "ضعيف"

            impact_bulls = impact_cell.find_all('i', {'class': 'grayFullBullishIcon'})
            num_bulls = len(impact_bulls) if impact_bulls else 0

            if num_bulls <= 1:
                return "ضعيف"
            elif num_bulls == 2:
                return "متوسط"
            else:
                return "قوي"
        except:
            return "ضعيف"

    def _parse_time(self, time_str):
        try:
            now = datetime.now(pytz.timezone('Asia/Riyadh'))
            hour, minute = map(int, time_str.split(':'))
            event_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return event_time
        except:
            return None
