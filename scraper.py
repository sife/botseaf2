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

            # Find the economic calendar table
            calendar_table = soup.find('table', {'id': 'economicCalendarData'})
            if not calendar_table:
                print("Calendar table not found")
                return []

            events = []
            table_body = calendar_table.find('tbody')
            if not table_body:
                print("Table body not found")
                return []

            rows = table_body.find_all('tr', {'class': 'js-event-item'})
            print(f"Found {len(rows)} total events, filtering for US events...")

            for row in rows:
                try:
                    # Check if it's a US event
                    country_cell = row.find('td', {'class': 'flagCur'})
                    if not country_cell or 'الولايات المتحدة' not in country_cell.text.strip():
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
                    value_cells = row.find_all('td', {'class': 'bold'})
                    previous = value_cells[0].text.strip() if len(value_cells) > 0 else "غير متوفر"
                    forecast = value_cells[1].text.strip() if len(value_cells) > 1 else "غير متوفر"

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
                    print(f"Error processing row: {e}")
                    continue

            print(f"Successfully found {len(events)} US events")
            return events

        except Exception as e:
            print(f"Error scraping calendar data: {e}")
            return []

    def _get_impact_level(self, row):
        try:
            impact_cell = row.find('td', {'class': 'sentiment'})
            if not impact_cell:
                return "ضعيف"

            impact_bull = impact_cell.find_all('i', {'class': 'grayFullBull'})
            num_bulls = len(impact_bull) if impact_bull else 0

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