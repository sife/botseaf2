from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import EconomicCalendarScraper
from formatter import format_notification_message
import pytz
import asyncio

class EventScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.scraper = EconomicCalendarScraper()
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Riyadh'))

    def start(self):
        # Schedule daily update at midnight
        self.scheduler.add_job(
            self.schedule_daily_events,
            CronTrigger(hour=0, minute=0),
            id='daily_update'
        )

        # Run initial schedule
        asyncio.create_task(self.schedule_daily_events())

        # Start the scheduler
        self.scheduler.start()

    def shutdown(self):
        """Properly shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    async def schedule_daily_events(self):
        """Schedule notifications for today's events"""
        try:
            # Clear existing event jobs
            for job in self.scheduler.get_jobs():
                if job.id != 'daily_update':
                    self.scheduler.remove_job(job.id)

            # Get today's events
            events = self.scraper.get_calendar_data()
            print(f"Found {len(events)} events for today")

            # Schedule notifications for each event
            for event in events:
                notification_time = event['time'] - timedelta(minutes=15)
                current_time = datetime.now(pytz.timezone('Asia/Riyadh'))

                # Only schedule future events
                if notification_time > current_time:
                    print(f"Scheduling notification for {event['name']} at {notification_time}")
                    self.scheduler.add_job(
                        self.send_notification,
                        'date',
                        run_date=notification_time,
                        args=[event],
                        id=f"notification_{event['name']}_{notification_time.timestamp()}"
                    )
        except Exception as e:
            print(f"Error scheduling daily events: {e}")

    async def send_notification(self, event):
        """Send notification for an upcoming event"""
        try:
            message = format_notification_message(event)
            await self.bot.send_notification(message)
            print(f"Sent notification for event: {event['name']}")
        except Exception as e:
            print(f"Error sending notification: {e}")