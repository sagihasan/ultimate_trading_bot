from pathlib import Path
import pandas as pd

# יצירת תיקיית data אם לא קיימת
data_path = Path("data")
data_path.mkdir(parents=True, exist_ok=True)

# הגדרת העמודות של trades_log.xlsx כולל תוצאת AI
trades_log_columns = [
    "תאריך",
    "מניה",
    "סוג עסקה",
    "מחיר כניסה",
    "סטופ לוס",
    "טייק פרופיט",
    "תוצאה",
    "(% תשואה)",
    "אזור כניסה",
    "תמיכת מגמה",
    "תשואת AI",  # חדש
]

# הגדרת העמודות של trade_management_log.xlsx
management_columns = [
    "סטופ קודם", "סטופ חדש", "טייק קודם", "טייק חדש", "תוצאה צפויה"
]

# יצירת קובץ trades_log.xlsx ריק אם לא קיים
trades_file = data_path / "trades_log.xlsx"
if not trades_file.exists():
    df = pd.DataFrame(columns=trades_log_columns)
    df.to_excel(trades_file, index=False)
    print("✅ trades_log.xlsx נוצר בהצלחה.")
else:
    print("ℹ️ trades_log.xlsx כבר קיים.")

# יצירת קובץ trade_management_log.xlsx ריק אם לא קיים
management_file = data_path / "trade_management_log.xlsx"
if not management_file.exists():
    df_management = pd.DataFrame(columns=management_columns)
    df_management.to_excel(management_file, index=False)
    print("✅ trade_management_log.xlsx נוצר בהצלחה.")
else:
    print("ℹ️ trade_management_log.xlsx כבר קיים.")
