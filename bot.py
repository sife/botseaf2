import asyncio
from telegram.ext import Application
from config import BOT_TOKEN, CHANNEL_ID
from scheduler import EventScheduler
import os

class EconomicCalendarBot:
    def __init__(self):
        # Get environment variables with fallback to config values
        self.token = os.getenv('BOT_TOKEN', BOT_TOKEN)
        self.channel_id = os.getenv('CHANNEL_ID', CHANNEL_ID)
        self.application = None
        self.scheduler = None

    async def send_notification(self, message):
        """Send notification to the channel"""
        try:
            await self.application.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="MARKDOWN"
            )
        except Exception as e:
            print(f"Error sending notification: {e}")

    async def initialize(self):
        """Initialize bot and scheduler"""
        try:
            print("Initializing bot application...")
            self.application = Application.builder().token(self.token).build()

            print("Starting bot application...")
            await self.application.initialize()
            await self.application.start()

            print("Initializing scheduler...")
            self.scheduler = EventScheduler(self)
            self.scheduler.start()

            print("Bot initialized successfully")
        except Exception as e:
            print(f"Error initializing bot: {e}")
            await self.cleanup()
            raise e

    async def cleanup(self):
        """Clean up resources"""
        print("Starting cleanup process...")
        if self.scheduler:
            print("Shutting down scheduler...")
            self.scheduler.shutdown()

        if self.application:
            try:
                print("Stopping application...")
                await self.application.stop()
                print("Shutting down application...")
                await self.application.shutdown()
                print("Application shutdown complete")
            except Exception as e:
                print(f"Error during application shutdown: {e}")
        print("Cleanup process completed")

    async def run(self):
        """Start the bot"""
        try:
            await self.initialize()
            print("Bot is running...")

            # Create a future that will never complete unless cancelled
            stop_future = asyncio.get_running_loop().create_future()

            try:
                # Wait for the future to complete (which it won't unless cancelled)
                await stop_future
            except asyncio.CancelledError:
                print("Received stop signal")

        except Exception as e:
            print(f"Error running bot: {e}")
        finally:
            await self.cleanup()

async def main():
    """Main entry point"""
    bot = None
    try:
        bot = EconomicCalendarBot()
        await bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if bot:
            await bot.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")