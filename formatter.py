from config import IMPACT_LEVELS
import pytz
from datetime import datetime

def format_arabic_time(dt):
    """Format time in Arabic-friendly format"""
    hour = dt.strftime('%H')
    minute = dt.strftime('%M')
    return f"{hour}:{minute}"

def format_event_message(event):
    """Format event details into a nice-looking message"""
    if not isinstance(event['time'], datetime):
        raise ValueError("Event time must be a datetime object")

    impact_emoji = IMPACT_LEVELS.get(event['impact'], '')
    event_time = event['time'].astimezone(pytz.timezone('Asia/Riyadh'))

    message = f"""
🗓 *الحدث*:
{event['name']}

⏰ *الموعد*:
{format_arabic_time(event_time)}

📊 *التأثير*:
{event['impact']} {impact_emoji}

📈 *سابق*:
{event['previous']}

🔄 *تقدير*:
{event['forecast']}
"""
    return message

def format_notification_message(event):
    """Format notification message for upcoming events"""
    if not isinstance(event['time'], datetime):
        raise ValueError("Event time must be a datetime object")

    impact_emoji = IMPACT_LEVELS.get(event['impact'], '')
    event_time = event['time'].astimezone(pytz.timezone('Asia/Riyadh'))

    message = f"""
⚠️ *حدث اقتصادي قادم بعد 15 دقيقة* ⚠️

🗓 *الحدث*:
{event['name']}

⏰ *الموعد*:
{format_arabic_time(event_time)}

📊 *التأثير*:
{event['impact']} {impact_emoji}

📈 *سابق*:
{event['previous']}

🔄 *تقدير*:
{event['forecast']}
"""
    return message