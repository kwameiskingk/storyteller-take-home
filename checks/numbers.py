#!/usr/bin/env python3
"""Every number quoted in the README and ops documents, computed from the pack.
If a figure in the prose is not produced here, it should not be in the prose.

Usage: python3 -I checks/numbers.py data/
"""
import csv, json, sys
from datetime import datetime, timedelta
from pathlib import Path

d = Path(sys.argv[1] if len(sys.argv) > 1 else "data")
src = json.loads((d / "01_source_content.json").read_text())
recs = json.loads((d / "02_trial_recommendations.json").read_text())
cost = list(csv.DictReader((d / "05_cost_summary.csv").open()))
log = list(csv.DictReader((d / "06_trial_run_log.csv").open()))
T = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
out = {}

# --- calendar ---
for day in range(3, 12):
    out[f"weekday 2026-09-{day:02d}"] = datetime(2026, 9, day).strftime("%A")
tip = T(src["scheduled_tipoff"]); out["tipoff UTC"] = tip.strftime("%H:%M")
out["tipoff local (UTC+1 per pack README)"] = (tip + timedelta(hours=1)).strftime("%H:%M")
out["Sam event cover minutes (17:00-18:30)"] = 90
out["minutes from Sam leaving to tipoff"] = int((tip - tip.replace(hour=18, minute=30)).total_seconds() // 60)
out["Delivery Lead window minutes (17:00-23:00)"] = 360
out["minutes replay generated_at -> Jordan 09:32"] = int((datetime(2026, 9, 3, 9, 32) - T(recs["generated_at"])).total_seconds() // 60)
by = {i["content_id"]: i for i in src["items"]}
out["CourtsideWire lead over official (min)"] = int((T(by["src_003"]["published_at"]) - T(by["src_010"]["published_at"])).total_seconds() // 60)
out["age of src_001 at replay (hours)"] = round((T(src["replay_started_at"]) - T(by["src_001"]["published_at"])).total_seconds() / 3600, 1)

# --- cost ---
for c in cost:
    ini, ret, tot, items = int(c["initial_model_calls"]), int(c["retry_model_calls"]), int(c["total_model_calls"]), int(c["source_items"])
    out[f"{c['date_utc']} retries per initial"] = round(ret / ini, 3)
    out[f"{c['date_utc']} EUR per call"] = round(float(c["ai_cost_eur"]) / tot, 4)
    out[f"{c['date_utc']} implied generations"] = ini - items
    out[f"{c['date_utc']} total vs forecast"] = round(float(c["total_cost_eur"]) / float(c["forecast_cost_eur"]), 2)
c1, c2 = cost[1], cost[2]
out["2 Sep items change %"] = round((int(c2["source_items"]) / int(c1["source_items"]) - 1) * 100, 1)
out["2 Sep initial calls change %"] = round((int(c2["initial_model_calls"]) / int(c1["initial_model_calls"]) - 1) * 100, 1)
out["2 Sep retry calls multiple"] = round(int(c2["retry_model_calls"]) / int(c1["retry_model_calls"]), 1)
out["2 Sep infrastructure change %"] = round((float(c2["infrastructure_cost_eur"]) / float(c1["infrastructure_cost_eur"]) - 1) * 100, 1)
out["min operations that retried on 2 Sep (cap 3 retries)"] = -(-int(c2["retry_model_calls"]) // 3)
eur_call = sum(float(c["ai_cost_eur"]) for c in cost) / sum(int(c["total_model_calls"]) for c in cost)
r_norm = sum(int(c["retry_model_calls"]) for c in cost[:2]) / sum(int(c["initial_model_calls"]) for c in cost[:2])
r_bad = int(c2["retry_model_calls"]) / int(c2["initial_model_calls"])
EVENT_ITEMS, EVENT_RECS, PEAK = 1500, 240, 80
ev_calls = EVENT_ITEMS + EVENT_RECS
out["event AI cost EUR at normal retry rate"] = round(ev_calls * (1 + r_norm) * eur_call, 0)
out["event AI cost EUR at 2 Sep retry rate"] = round(ev_calls * (1 + r_bad) * eur_call, 0)
out["allowance EUR 100 spread over 6h = per hour"] = round(100 / 6, 1)

# --- volume and capacity ---
avg_items_day = sum(int(c["source_items"]) for c in cost) / 3
out["normal items per hour"] = round(avg_items_day / 24, 1)
out["event items per hour"] = EVENT_ITEMS / 6
out["event vs normal hourly rate (x)"] = round((EVENT_ITEMS / 6) / (avg_items_day / 24), 1)
out["event recs per hour average"] = EVENT_RECS / 6
out["pilot queue reviewed share % (30-40 of 180)"] = f"{30/180*100:.0f} to {40/180*100:.0f}"
QUICK, SLOW, SLOW_SHARE = 52.5, 150, 0.20
mins = lambda n: n * ((1 - SLOW_SHARE) * QUICK + SLOW_SHARE * SLOW) / 60
out["review minutes: 240 cards"] = round(mins(240))
out["review minutes: 80-card peak hour"] = round(mins(80))
out["review minutes: 40-card hour"] = round(mins(40))
out["cards one reviewer clears in 60 min (assumed mix)"] = int(60 / (mins(1)))
# reduced scope: high lane = result, player availability, schedule/venue change, official record
approved = [i for i in src["items"] if i["approved_for_pilot"]]
HIGH = {"src_001", "src_003", "src_004", "src_005"}
out["approved items in sample"] = len(approved)
out["high-lane items in sample"] = len(HIGH)
share = len(HIGH) / len(approved)
out["high-lane share of approved sample %"] = round(share * 100)
out["peak-hour cards after duplicates removed and high lane only"] = round(PEAK * share, 1)
out["review minutes for that peak hour"] = round(mins(PEAK * share))
out["slack minutes in that hour for one reviewer"] = round(60 - mins(PEAK * share))
# latency budget to the client's ~10 minute target
gen = {}
for e in log:
    if e["stage"] == "generate" and e["event"] == "started": gen.setdefault((e["source_content_id"], e["attempt"]), {})["start"] = T(e["timestamp_utc"])
    if e["stage"] == "generate" and e["event"] in ("completed", "timeout", "validation_failed"): gen.setdefault((e["source_content_id"], e["attempt"]), {})["end"] = T(e["timestamp_utc"])
lat = sorted(int((v["end"] - v["start"]).total_seconds()) for v in gen.values() if "start" in v and "end" in v)
out["generation latencies observed (s)"] = lat
out["latency budget: poll interval (s)"] = 300
out["latency budget: worst generation incl. one timeout+retry (s)"] = 15 + max(lat)
out["latency budget: review one card (s)"] = QUICK
out["latency budget: minutes left of 10 for queue dwell"] = round((600 - 300 - (15 + max(lat)) - QUICK) / 60, 1)

for k, v in out.items(): print(f"{k:60} {v}")
json.dump(out, open(Path(sys.argv[2]) / "numbers.json", "w") if len(sys.argv) > 2 else sys.stderr, indent=1, default=str) if len(sys.argv) > 2 else None
