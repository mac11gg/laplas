import sqlite3
from database import DB

def generate_learning_path(goal: str, level: str, timeframe: int):
    counts = {'Початковий': 4, 'Середній': 6, 'Просунутий': 8}
    n = counts.get(level, 4)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT topic, materials FROM {goal} LIMIT ?", (n,))
    rows = cursor.fetchall()
    conn.close()
    plan = []
    for i, (topic, materials) in enumerate(rows):
        plan.append({"№": i+1, "Тема": topic, "Матеріали": materials})
    return plan
