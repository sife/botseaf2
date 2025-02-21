import asyncio
from telegram.ext import Application
from config import BOT_TOKEN, CHANNEL_ID
from scheduler import EventScheduler

class EconomicCalendarBot:
    def __init__(self):
        self.token = BOT_TOKEN
        self.channel_id = CHANNEL_ID
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
            self.application = Application.builder().token(self.token).build()
            await self.application.initialize()
            await self.application.start()

            self.scheduler = EventScheduler(self)
            self.scheduler.start()

            print("Bot initialized successfully")
        except Exception as e:
            print(f"Error initializing bot: {e}")
            if self.application:
                await self.application.shutdown()
            raise e

    async def run(self):
        """Start the bot"""
        try:
            await self.initialize()
            print("Bot is running...")
            await self.application.run_polling(drop_pending_updates=True)
        except Exception as e:
            print(f"Error running bot: {e}")
            raise e

async def main():
    """Main entry point"""
    bot = None
    try:
        bot = EconomicCalendarBot()
        await bot.run()
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if bot and bot.scheduler:
            bot.scheduler.shutdown()
        if bot and bot.application:
            await bot.application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())