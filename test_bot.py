import asyncio
from datetime import datetime
import pytz
from bot import EconomicCalendarBot
from formatter import format_notification_message
from scraper import EconomicCalendarScraper

async def test_bot_notification():
    try:
        print("\nبدء اختبار إرسال الإشعارات...")
        bot = EconomicCalendarBot()
        await bot.initialize()

        # Get all events
        print("جاري جلب بيانات التقويم الاقتصادي...")
        scraper = EconomicCalendarScraper()
        events = scraper.get_calendar_data()

        if events:
            print("\nالأحداث المجدولة لليوم:")
            for idx, event in enumerate(events, 1):
                print(f"\nالحدث {idx}:")
                print(f"الاسم: {event['name']}")
                print(f"الوقت: {event['time']}")
                print(f"التأثير: {event['impact']}")
                print(f"السابق: {event['previous']}")
                print(f"التوقع: {event['forecast']}")

                # Send notification for each event
                message = format_notification_message(event)
                print(f"\nإرسال إشعار للحدث {idx}...")
                await bot.send_notification(message)
                print("تم إرسال الإشعار بنجاح")

                # Add a small delay between messages
                await asyncio.sleep(2)
        else:
            print("لم يتم العثور على أحداث للاختبار")

    except Exception as e:
        print(f"خطأ في اختبار البوت: {e}")
    finally:
        if 'bot' in locals() and bot:
            await bot.cleanup()
            print("تم إنهاء الاختبار")

if __name__ == "__main__":
    try:
        asyncio.run(test_bot_notification())
    except KeyboardInterrupt:
        print("\nتم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"خطأ: {e}")