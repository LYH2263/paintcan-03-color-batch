import json, sqlite3
from datetime import datetime, timezone

def insert(conn, kind, payload, result, room_id=None):
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("INSERT INTO calc_runs(kind,room_id,input_json,result_json,created_at) VALUES (?,?,?,?,?)",
        (kind, room_id, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False), now))
    conn.commit(); return int(cur.lastrowid)

def _decode(row):
    d = dict(row)
    for k in ("input_json", "result_json"):
        try:
            d[k.removesuffix("_json")] = json.loads(d.pop(k))
        except (ValueError, TypeError):
            d[k.removesuffix("_json")] = None
    return d

def list_recent(conn, limit=50):
    return [_decode(r) for r in conn.execute("SELECT * FROM calc_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]

def get(conn, rid):
    row = conn.execute("SELECT * FROM calc_runs WHERE id=?", (rid,)).fetchone()
    return _decode(row) if row else None
