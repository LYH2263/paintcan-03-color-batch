from app.db import connect
from app.engines.estimate import estimate_room
from app.modules import color_batch
from app.repositories import openings, rooms, runs, settings

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self): return settings.get_map(self._c)
    def update_settings(self, default_color_code=None):
        if default_color_code is not None:
            code = color_batch.normalize(default_color_code)
            if not code: raise ValueError("默认色号不能为空")
            settings.set_value(self._c, color_batch.DEFAULT_COLOR_KEY, code)
        return self.settings()
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def get_run(self, rid): return runs.get(self._c, rid)
    def estimate(self, room_id, persist, coats=None, coverage=None, color_code=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        # 显式色号优先；缺省回退设置中的默认色号；空/仅空白整单拒绝（不写记录）。
        code = color_batch.resolve_color(color_code, settings.default_color(self._c))
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct)
        # 钉选：色号与测算当下的净面积、升数、涂布率、遍数一并固化。
        pin = color_batch.pin_snapshot(code, result)
        result = {**result, **pin}
        payload = {"room_id": room_id, "coats": ct, "coverage": cov, "color_code": code}
        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
