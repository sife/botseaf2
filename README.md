# بوت التقويم الاقتصادي الأمريكي 🇺🇸

بوت تيليجرام يقوم بإرسال إشعارات للأحداث الاقتصادية الأمريكية المهمة باللغة العربية.

## المميزات 🌟
- جلب الأخبار الاقتصادية الأمريكية فقط
- إرسال إشعارات قبل 15 دقيقة من صدور كل خبر
- عرض التفاصيل باللغة العربية
- تحديث تلقائي يومي
- تصنيف الأخبار حسب التأثير:
  - متوسط 🟡🟡
  - قوي 🔴🔴🔴

## متطلبات التشغيل 🔧
1. Python 3.11 أو أحدث
2. حساب Telegram Bot (يمكن إنشاؤه عبر [@BotFather](https://t.me/BotFather))
3. قناة Telegram لإرسال الإشعارات

## خطوات التثبيت 📥

1. استنساخ المشروع:
```bash
git clone https://github.com/your-username/us-economic-calendar-bot.git
cd us-economic-calendar-bot
```

2. تثبيت المكتبات المطلوبة:
```bash
pip install -r requirements.txt
```

3. إعداد متغيرات البيئة:
   - قم بإنشاء ملف `.env` في المجلد الرئيسي
   - أضف المتغيرات التالية:
```
BOT_TOKEN=your_bot_token_here
CHANNEL_ID=@your_channel_name
```

4. تشغيل البوت:
```bash
python bot.py
```

## كيفية الاستخدام 📱
1. تأكد من أن البوت مشرف في القناة المحددة
2. شغل البوت باستخدام الأمر `python bot.py`
3. سيبدأ البوت في إرسال إشعارات قبل 15 دقيقة من كل حدث اقتصادي مهم

## الدعم والمساهمة 🤝
- يمكنك الإبلاغ عن المشاكل عبر [Issues](https://github.com/your-username/us-economic-calendar-bot/issues)
- المساهمات مرحب بها عبر [Pull Requests](https://github.com/your-username/us-economic-calendar-bot/pulls)

## الترخيص 📄
هذا المشروع مرخص تحت رخصة MIT.
