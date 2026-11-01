"""Hand-derived expectations for reconcile.py. The numbers below were counted by hand from the pack
BEFORE the script was run, so the script is checked against a human reading, not against itself.
Run:  python3 -I -m pytest -q checks/   (or python3 -I checks/test_reconcile.py)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import reconcile as R

DATA = Path(__file__).parent.parent / "data"
src, recs, log, cost = R.load(DATA)
rows, events, recs_by_src = R.build_fact_table(src, recs, log)
by_id = {r["content_id"]: r for r in rows}


def test_ten_sources_eight_cards():
    assert len(src) == 10 and len(recs) == 8


def test_duplicate_is_src_001_only():
    dups = {sid: [r["recommendation_id"] for r in rs] for sid, rs in recs_by_src.items() if len(rs) > 1}
    assert dups == {"src_001": ["rec_001", "rec_003"]}


def test_timed_out_request_still_completed():
    ev = [(e["attempt"], e["event"]) for e in events["src_001"] if e["stage"] == "generate"]
    assert ("1", "timeout") in ev and ("1", "completed") in ev and ("2", "completed") in ev


def test_lost_items():
    lost = sorted(r["content_id"] for r in rows if r["approved"] and r["card_count"] == 0)
    assert lost == ["src_003", "src_004"]
    assert by_id["src_003"]["outcome"] == "relevant, LOST (no card)"
    assert by_id["src_004"]["outcome"] == "classified not relevant"


def test_unapproved_item_not_processed():
    assert by_id["src_010"]["outcome"] == "not approved, not processed"


def test_mensah_record_claim_is_unsupported():
    rec = next(r for r in recs if r["recommendation_id"] == "rec_004")
    body = (by_id["src_005"]["title"] + " " + src[4]["body"]).lower()
    assert "tying" in body and "league record" not in body.replace("league playoff record", "")
    assert "broke" in rec["summary"].lower() and "sets new" in rec["headline"].lower()


def test_cost_arithmetic_by_hand():
    by_date = {c["date_utc"]: c for c in cost}
    assert int(by_date["2026-09-02"]["retry_model_calls"]) == 2412
    assert int(by_date["2026-08-31"]["retry_model_calls"]) == 54
    # retries per initial call: 54/1300=0.0415, 63/1360=0.0463, 2412/1390=1.735
    assert round(2412 / 1390, 3) == 1.735
    # implied generations = initial - items: 1300-1120=180, 1360-1180=180, 1390-1205=185
    assert [int(c["initial_model_calls"]) - int(c["source_items"]) for c in cost] == [180, 180, 185]
    # per-call cost: 24.40/1354=0.01802, 65.60/3802=0.01725
    assert round(24.40 / 1354, 4) == 0.0180 and round(65.60 / 3802, 4) == 0.0173


def test_latency_hand_counts():
    # gen_002 started 09:15:04, completed 09:15:19 = 15s. gen_001 attempt 1: 09:15:02 -> timeout 09:15:17 = 15s, completed 09:15:23 = 21s
    assert "a1:completed:15s" in by_id["src_002"]["generate_events"]
    assert "a1:timeout:15s" in by_id["src_001"]["generate_events"] and "a1:completed:21s" in by_id["src_001"]["generate_events"]


def test_courtsidewire_lead_time():
    a = R.ts("2026-09-03T07:48:00Z"); b = R.ts("2026-09-03T08:10:00Z")
    assert (b - a).total_seconds() == 22 * 60


def test_canonical_url_strips_tracking():
    assert R.canonical("https://example.com/broadcast/grant-game-2-highlights?utm_source=abl") == "https://example.com/broadcast/grant-game-2-highlights"


if __name__ == "__main__":
    import inspect
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and inspect.isfunction(fn):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, e)
    sys.exit(1 if fails else 0)
