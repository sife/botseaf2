import asyncio
from datetime import datetime
import pytz
from bot import EconomicCalendarBot
from formatter import format_notification_message
from scraper import EconomicCalendarScraper

async def test_bot_notification():
    try:
        print("Initializing test bot...")
        bot = EconomicCalendarBot()
        await bot.initialize()

        # Get the first real event
        print("Fetching calendar data...")
        scraper = EconomicCalendarScraper()
        events = scraper.get_calendar_data()

        if events:
            first_event = events[0]
            print("\nSending notification for first event:")
            print(f"Event: {first_event['name']}")
            print(f"Time: {first_event['time']}")
            print(f"Impact: {first_event['impact']}")
            print(f"Previous: {first_event['previous']}")
            print(f"Forecast: {first_event['forecast']}")

            # Format and send notification
            message = format_notification_message(first_event)
            print("\nFormatted message:")
            print(message)
            print("\nSending notification to channel...")
            await bot.send_notification(message)
            print("Test message sent successfully")
        else:
            print("No events found to test")

    except Exception as e:
        print(f"Error testing bot: {e}")
    finally:
        print("Starting test cleanup...")
        if 'bot' in locals():
            if bot.scheduler:
                print("Shutting down scheduler...")
                bot.scheduler.shutdown()
            if bot.application:
                print("Stopping application...")
                await bot.application.stop()
                print("Shutting down application...")
                await bot.application.shutdown()
                print("Application shutdown completed")
        print("Test cleanup completed")

if __name__ == "__main__":
    try:
        asyncio.run(test_bot_notification())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test error: {e}")