# Ultimate Trading Bot

בוט מסחר חכם, חזק ואוטונומי שפועל בשוק האמריקאי (NYSE / NASDAQ) לפי שילוב ניתוח טכני, פונדומנטלי, מאקרו, סנטימנט, Machine Learning וניתוחים מתקדמים נוספים.

---

## מה יש בבוט:

- ניתוח טכני ופונדומנטלי (כולל צפי עתידי של החברה)
- ניהול סיכונים לפי 2% מהתיק (גודל עסקה מחושב אוטומטית)
- זיהוי חכם של:
  - יום מסחר רגיל
  - חצי יום מסחר
  - ימים ללא מסחר (כולל הודעה למה אין מסחר)
  - פערי שעות (שעון קיץ)
- שליחת איתותים ודוחות ל-Discord:
  - ערוץ ציבורי (איתותים, אירועים, עדכונים)
  - ערוץ פרטי (דו"חות, פתיחה/סגירה)
  - ערוץ שגיאות

---

## יכולות מתקדמות:

- **Timeframe:** ניתוח יומי, שבועי וחודשי (במגמה היומית והשבועית חובה להיות תיאום)
- **אזורים טכניים:** זיהוי Golden Zone, Demand Zone, Buffett Zone
- **אינדיקטורים:** RSI, MACD, Bollinger Bands, ממוצעים נעים אקספוננציאליים (EMA 9/20/50/100/200)
- **תבניות ניתוח טכני:** נרות היפוך, פסגות ותחתיות, דגלים, משולשים, מניפות
- **Machine Learning:** המלצות לפי רשת נתונים מאומנת בקובץ CSV
- **סנטימנט שוק:** ניתוח חכם כולל דירוג (חלש / בינוני / חזק)
- **ניתוח מאקרו:** ריבית, CPI, אבטלה, נאומים, אינפלציה, תמ"ג ועוד
- **סקטורים:** ניתוח סקטור ותת סקטור
- **תחזית עתידית:** זיהוי מגמות צפויות על בסיס תנועת מחיר ודוחות
- **ניהול עסקאות:** סטופ לוס וטייק פרופיט עם עדכונים אוטומטיים, כולל חישוב אחוזים ודולרים
- **הערכת סיכון/סיכוי:** יחס 1:2 לפחות, עם אחוזים ודולרים בכל איתות
- **זיהוי מוסדיים, תיקונים טכניים, שורט סקוויז, ספליט ואיחוד מניות**
- **בוט קובע:** האם להיכנס לעסקה או לא – לפי שקלול חכם

---

## קבצים עיקריים:

- `main.py` – הלב של הבוט
- `config.py` – הגדרות כלליות (שעות, סיכון, API)
- `fundamentals.py` – ניתוח פונדומנטלי
- `technicals.py` – ניתוח טכני
- `macro.py` + `macro_analyzer.py` – ניתוח מאקרו
- `ml_model.py` – ניתוח AI
- `scheduler.py` – תזמון פעולות
- `reporting.py` – שליחת דו"חות שבועיים וחודשיים
- `discord_manager.py` – שליחת הודעות ל-Discord
- `changelog_manager.py` – ניהול עדכונים
- `run_all.py` – קובץ הפעלה כולל
- `stock_list.py` – רשימת מניות לסריקה
- `open_trades.json`, `trade_log.json` – קבצי מעקב עסקאות פתוחות וסגורות

---

## איך מתקינים:

1. הכנס את משתני הסביבה לקובץ `.env` (כגון API ו־Webhook)
2. התקן את הספריות הנדרשות:

```bash
pip install -r requirements.txt
