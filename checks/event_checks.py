#!/usr/bin/env python3
"""Generic checks for an export taken during the event: duplicates, lost items and queue dwell.
No prose, no pack-specific values. Works on any export that follows the pilot schema:
  sources: JSON with "items": [{content_id, published_at, approved_for_pilot, title, ...}]
  log:     CSV with timestamp_utc, source_content_id, stage, operation_id, attempt, event, reference, detail
  queue:   JSON with "recommendations": [{recommendation_id, source_content_ids, workflow_attempt, ...}]
Usage: python3 -I checks/event_checks.py <sources.json> <log.csv> <queue.json> [--dwell-limit-min 10]
Exit code 1 if any duplicate, lost item or over-limit dwell is found, so it can gate a 15-minute check.
"""
import argparse, csv, json, sys
from collections import defaultdict
from datetime import datetime

T = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sources"); ap.add_argument("log"); ap.add_argument("queue")
    ap.add_argument("--dwell-limit-min", type=float, default=10.0)
    a = ap.parse_args()
    items = {i["content_id"]: i for i in json.load(open(a.sources))["items"] if i.get("approved_for_pilot", True)}
    log = list(csv.DictReader(open(a.log)))
    recs = json.load(open(a.queue))["recommendations"]
    problems = 0

    # 1. duplicates: more than one card per source, or more than one queue write per operation
    cards = defaultdict(list)
    for r in recs:
        for sid in r["source_content_ids"]:
            cards[sid].append(r["recommendation_id"])
    for sid, ids in cards.items():
        if len(ids) > 1:
            problems += 1; print(f"DUPLICATE  {sid}: {ids}")
    writes = defaultdict(list)
    for e in log:
        if e["stage"] == "queue" and e["event"] == "written":
            writes[e["operation_id"]].append(e["reference"])
    for op, refs in writes.items():
        if len(refs) > 1:
            problems += 1; print(f"DUPLICATE  operation {op} wrote {refs}")

    # 2. lost: approved and classified relevant but no card; or relevant with a failed/absent generation
    cls = {e["source_content_id"]: e["reference"] for e in log if e["stage"] == "classify"}
    gen_end = defaultdict(list)
    for e in log:
        if e["stage"] == "generate" and e["event"] in ("completed", "timeout", "validation_failed"):
            gen_end[e["source_content_id"]].append(e["event"])
    for sid in items:
        if sid not in cls:
            problems += 1; print(f"UNSEEN     {sid}: no classification event")
        elif cls[sid] == "true" and sid not in cards:
            problems += 1; print(f"LOST       {sid}: relevant but no card; generate events {gen_end.get(sid) or 'none'}")
        elif cls[sid] == "false":
            print(f"REJECTED   {sid}: classified not relevant ({items[sid].get('title','')[:60]})")

    # 3. dwell: published -> first queue write, and queue write -> approval if a decision log is present later
    written_at = {}
    for e in log:
        if e["stage"] == "queue" and e["event"] == "written":
            written_at.setdefault(e["source_content_id"], T(e["timestamp_utc"]))
    for sid, t in written_at.items():
        if sid in items:
            mins = (t - T(items[sid]["published_at"])).total_seconds() / 60
            flag = "OVER " if mins > a.dwell_limit_min else "ok   "
            if mins > a.dwell_limit_min: problems += 1
            print(f"DWELL {flag}{sid}: {mins:.1f} min from publish to queue (limit {a.dwell_limit_min:g}; replayed items will exceed it by design)")
    print(f"\n{problems} problem(s) flagged")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
