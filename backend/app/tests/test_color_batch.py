import json
import pytest

from app import db as db_mod
from app import seed
from app.modules import color_batch
from app.services.paint_service import PaintService


@pytest.fixture()
def service(tmp_path, monkeypatch):
    monkeypatch.setattr(db_mod, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    with PaintService() as s:
        yield s


# --- 纯模块逻辑 ---

def test_resolve_explicit_color():
    assert color_batch.resolve_color("R118", "N001") == "R118"

def test_resolve_trims_whitespace():
    assert color_batch.resolve_color("  B205 ", "N001") == "B205"

def test_resolve_falls_back_to_default():
    assert color_batch.resolve_color(None, "N001") == "N001"

def test_resolve_empty_explicit_rejected():
    with pytest.raises(ValueError):
        color_batch.resolve_color("   ", "N001")

def test_resolve_empty_default_rejected():
    with pytest.raises(ValueError):
        color_batch.resolve_color(None, "  ")

def test_pin_snapshot_captures_all():
    r = {"net_m2": 46.41, "liters": 11.6, "coverage": 8.0, "coats": 2}
    pin = color_batch.pin_snapshot("R118", r)
    assert pin == {"color_code": "R118", "net_m2": 46.41,
                   "liters": 11.6, "coverage": 8.0, "coats": 2}


# --- 服务/落库行为 ---

def test_estimate_uses_default_color_when_absent(service):
    out = service.estimate(1, persist=False)
    assert out["color_code"] == "N001"
    assert out["run_id"] is None  # 不落库

def test_estimate_persist_false_does_not_write(service):
    before = len(service.history())
    service.estimate(1, persist=False)
    assert len(service.history()) == before

def test_empty_color_rejected_and_no_record(service):
    before = len(service.history())
    with pytest.raises(ValueError):
        service.estimate(1, persist=True, color_code="   ")
    assert len(service.history()) == before

def test_persist_pins_snapshot(service):
    out = service.estimate(1, persist=True, color_code="R118")
    run = service.get_run(out["run_id"])
    assert run["input"]["color_code"] == "R118"
    assert run["result"]["color_code"] == "R118"
    for k in ("net_m2", "liters", "coverage", "coats"):
        assert run["result"][k] == out[k]

def test_changing_default_keeps_old_records(service):
    first = service.estimate(1, persist=True)  # 写入时默认 N001
    assert first["color_code"] == "N001"
    first_liters = first["liters"]

    service.update_settings(default_color_code="B205")

    old = service.get_run(first["run_id"])
    assert old["result"]["color_code"] == "N001"        # 旧记录色号不变
    assert old["result"]["liters"] == first_liters       # 旧记录升数不变

    again = service.estimate(1, persist=False)           # 当场再测用新默认
    assert again["color_code"] == "B205"
