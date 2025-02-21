import asyncio
from datetime import datetime
import pytz
from bot import EconomicCalendarBot
from formatter import format_notification_message

async def test_bot_notification():
    try:
        print("Initializing test bot...")
        bot = EconomicCalendarBot()
        await bot.initialize()

        # Create a test event with current time
        current_time = datetime.now(pytz.timezone('Asia/Riyadh'))
        test_event = {
            'name': 'اختبار البوت - مؤشر أسعار المستهلك الأمريكي',
            'time': current_time,
            'impact': 'قوي',
            'previous': '3.4%',
            'forecast': '3.0%'
        }

        # Test notification format
        message = format_notification_message(test_event)
        print("\nSending test notification with new format:")
        print(message)
        await bot.send_notification(message)
        print("Test message sent successfully")

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