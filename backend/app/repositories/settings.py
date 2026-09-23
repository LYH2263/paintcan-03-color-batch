import sqlite3
from app.modules.color_batch import DEFAULT_COLOR_KEY, FALLBACK_DEFAULT_COLOR

def get_map(conn): return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}
def coverage_coats(conn):
    m = get_map(conn)
    return float(m.get("coverage", "8")), int(m.get("coats", "2"))
def default_color(conn):
    """设置中的默认色号；可能为空串（此时缺省请求应被拒绝）。"""
    return (get_map(conn).get(DEFAULT_COLOR_KEY) or FALLBACK_DEFAULT_COLOR).strip()
def set_value(conn, key, value):
    conn.execute(
        "INSERT INTO settings(key,value) VALUES (?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))
    conn.commit()
