import asyncio
from telegram.ext import Application, CommandHandler
from telegram.constants import ParseMode
from config import BOT_TOKEN, CHANNEL_ID, BOT_DESCRIPTION
from scheduler import EventScheduler

class EconomicCalendarBot:
    def __init__(self):
        self.token = BOT_TOKEN
        self.channel_id = CHANNEL_ID
        self.application = Application.builder().token(self.token).build()
        self.scheduler = EventScheduler(self)

    async def start(self, update, context):
        """Handle the /start command"""
        await update.message.reply_text(
            BOT_DESCRIPTION,
            parse_mode=ParseMode.MARKDOWN
        )

    async def send_notification(self, message):
        """Send notification to the channel"""
        try:
            await self.application.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error sending notification: {e}")

    async def run(self):
        """Start the bot"""
        try:
            print("Initializing bot...")
            await self.application.initialize()

            # Add command handlers
            self.application.add_handler(CommandHandler("start", self.start))

            # Start the scheduler
            self.scheduler.start()

            print("Starting bot polling...")
            await self.application.start()
            await self.application.run_polling(allowed_updates=["message"])
        except Exception as e:
            print(f"Error running bot: {e}")
        finally:
            print("Shutting down bot...")
            await self.application.stop()
            await self.application.shutdown()

async def main():
    bot = EconomicCalendarBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())