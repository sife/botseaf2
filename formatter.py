from config import IMPACT_LEVELS
import pytz
from datetime import datetime

def format_arabic_time(dt):
    """Format time in Arabic-friendly format with AM/PM indicator"""
    hour = int(dt.strftime('%H'))
    minute = dt.strftime('%M')

    # Convert to 12-hour format with Arabic period indicator
    if hour == 0:
        period = "صباحاً"
        hour = 12
    elif hour < 12:
        period = "صباحاً"
    elif hour == 12:
        period = "مساءً"
    else:
        period = "مساءً"
        hour = hour - 12

    return f"{hour}:{minute} {period}"

def format_notification_message(event):
    """Format notification message for upcoming events"""
    if not isinstance(event['time'], datetime):
        raise ValueError("Event time must be a datetime object")

    impact_emoji = IMPACT_LEVELS.get(event['impact'], '')
    event_time = event['time'].astimezone(pytz.timezone('Asia/Riyadh'))

    message = f"""⚠️ حدث اقتصادي قادم بعد 15 دقيقة ⚠️

🗓 الحدث:{event['name']}

⏰ الموعد:{format_arabic_time(event_time)}

📊 التأثير:{event['impact']} {impact_emoji}

📈 سابق:{event['previous']}

🔄 تقدير:{event['forecast']}""".strip()

    return message