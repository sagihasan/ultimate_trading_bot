# macro.py

import random
from datetime import datetime

def analyze_macro_conditions():
    today = datetime.now().weekday()

    # ברירת מחדל
    macro_sentiment = "ניטרלי"
    macro_note = "אין השפעה מהותית מהמאקרו כרגע."

    # סימולציה לאירועים – לדוגמה:
    if today == 1 and random.random() < 0.5:
        macro_sentiment = "שלילי"
        macro_note = "נאום של הפד היום – השוק מתוח."

    elif today == 3 and random.random() < 0.3:
        macro_sentiment = "חיובי"
        macro_note = "צפי לדוחות חזקים ומדדים חיוביים."

    return {
        "macro_sentiment": macro_sentiment,
        "note": macro_note
    }

