import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
from config import CALENDAR_URL

class EconomicCalendarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timezone = pytz.timezone('Asia/Riyadh')

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
                    # Check if it's a US event
                    us_flag = row.find('span', {'class': 'ceFlags United_States'})
                    if not us_flag:
                        continue

                    # Extract event details
                    time_cell = row.find('td', {'class': 'time'})
                    event_cell = row.find('td', {'class': 'event'})

                    if not all([time_cell, event_cell]):
                        continue

                    # Parse time and create datetime object
                    time = time_cell.text.strip()
                    event_time = self._parse_time(time)

                    # If time can't be parsed, try to handle special cases
                    if not event_time and time.lower() not in ['tentative', 'all day', 'تقريبي', 'طوال اليوم']:
                        try:
                            # Try to parse time in different formats
                            if ':' not in time:
                                # For cases like "1400" or "0900"
                                if len(time) == 4:
                                    hour = int(time[:2])
                                    minute = int(time[2:])
                                    now = datetime.now(self.timezone)
                                    event_time = now.replace(
                                        hour=hour,
                                        minute=minute,
                                        second=0,
                                        microsecond=0
                                    )
                        except Exception as e:
                            print(f"Failed to parse special time format for event: {event_cell.text.strip()} - {str(e)}")
                            continue

                    # Skip events without a valid time
                    if not event_time:
                        print(f"Skipping event due to invalid time: {event_cell.text.strip()} ({time})")
                        continue

                    event_name = event_cell.text.strip()
                    impact = self._get_impact_level(row)

                    # Get previous and forecast values
                    prev_cell = row.find('td', {'class': 'prev'})
                    forecast_cell = row.find('td', {'class': 'fore'})

                    previous = prev_cell.text.strip() if prev_cell else "غير متوفر"
                    forecast = forecast_cell.text.strip() if forecast_cell else "غير متوفر"

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
        """Parse time string and return a timezone-aware datetime object"""
        try:
            now = datetime.now(self.timezone)
            if ':' in time_str:
                hour, minute = map(int, time_str.split(':'))

                # Create datetime object with current date and parsed time
                event_time = now.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                # If event time is in the past (crossed midnight), skip it
                if event_time < now:
                    return None

                return event_time
            return None
        except Exception as e:
            print(f"Error parsing time {time_str}: {str(e)}")
            return None