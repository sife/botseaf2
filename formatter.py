from config import IMPACT_LEVELS

def format_event_message(event):
    """Format event details into a nice-looking message"""
    impact_emoji = IMPACT_LEVELS.get(event['impact'], '')
    
    message = f"""
🗓 *الحدث*:
{event['name']}

⏰ *الموعد*:
{event['time'].strftime('%H:%M')}

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
    impact_emoji = IMPACT_LEVELS.get(event['impact'], '')
    
    message = f"""
⚠️ *تنبيه: خبر اقتصادي قادم خلال 15 دقيقة* ⚠️

🗓 *الحدث*:
{event['name']}

⏰ *الموعد*:
{event['time'].strftime('%H:%M')}

📊 *التأثير*:
{event['impact']} {impact_emoji}
"""
    return message
