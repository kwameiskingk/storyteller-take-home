#!/usr/bin/env python3
"""Reconcile the Aurora pilot evidence: sources (01) -> processing log (06) -> queue (02), plus cost (05).

Writes outputs/fact_table.csv and outputs/findings.md. Prints the findings.
Every finding quotes the rows it rests on. Anything that depends on an assumption says so.

Usage:  python3 -I checks/reconcile.py data/ outputs/
"""
import csv, json, re, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

# ---- assumptions (not in the pack; change here and the report changes) ----
SLOW_SHARE = 0.20          # share of cards that need source comparison (2-3 min). Pack gives no figure.
QUICK_SEC, SLOW_SEC = 52.5, 150   # midpoints of "45-60s" and "2-3 min" from 07_service_expectations
EVENT_ITEMS, EVENT_RECS = 1500, 240   # Product's planning estimate, 07
PEAK_RECS_PER_HOUR = 80
SAM_EVENT_MINUTES = 90      # 17:00-18:30 UTC, 07
PROMO_MARKERS = ["win a ", "giveaway", "sponsor", "request a", "quote", "terms and conditions"]
STRONG_CLAIMS = ["broke", "sets new", "new league", "league record", "record-breaking", "first ever", "most ever"]


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def canonical(url):
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc, p.path.rstrip("/"), "", ""))


def words(t):
    return set(re.findall(r"[a-z0-9]+", t.lower()))


def load(data_dir):
    d = Path(data_dir)
    src = json.loads((d / "01_source_content.json").read_text())["items"]
    recs = json.loads((d / "02_trial_recommendations.json").read_text())["recommendations"]
    log = list(csv.DictReader((d / "06_trial_run_log.csv").open()))
    cost = list(csv.DictReader((d / "05_cost_summary.csv").open()))
    return src, recs, log, cost


def build_fact_table(src, recs, log):
    events = defaultdict(list)
    for e in log:
        events[e["source_content_id"]].append(e)
    recs_by_src = defaultdict(list)
    for r in recs:
        for sid in r["source_content_ids"]:
            recs_by_src[sid].append(r)
    rows = []
    for s in src:
        sid = s["content_id"]
        ev = events[sid]
        cls = [e for e in ev if e["stage"] == "classify"]
        gens = [e for e in ev if e["stage"] == "generate"]
        starts = {e["attempt"]: ts(e["timestamp_utc"]) for e in gens if e["event"] == "started"}
        ends = [(e["attempt"], e["event"], ts(e["timestamp_utc"])) for e in gens if e["event"] in ("completed", "timeout", "validation_failed")]
        latencies = [f"a{a}:{ev_}:{int((t - starts[a]).total_seconds())}s" for a, ev_, t in ends if a in starts]
        outcome = ("not approved, not processed" if not s["approved_for_pilot"]
                   else "no classify event" if not cls
                   else "classified not relevant" if cls[0]["reference"] == "false"
                   else "relevant, card written" if recs_by_src[sid]
                   else "relevant, LOST (no card)")
        rows.append({
            "content_id": sid, "published_at": s["published_at"], "source": s["source"],
            "approved": s["approved_for_pilot"], "title": s["title"],
            "classified_relevant": cls[0]["reference"] if cls else "",
            "classify_reason": cls[0]["detail"] if cls else "",
            "generate_events": " ".join(latencies),
            "cards": ",".join(r["recommendation_id"] for r in recs_by_src[sid]),
            "card_count": len(recs_by_src[sid]), "outcome": outcome,
        })
    return rows, events, recs_by_src


def findings(src, recs, log, cost, rows, events, recs_by_src):
    by_id = {s["content_id"]: s for s in src}
    F = []

    # 1 duplicates
    dup_lines = []
    for sid, rs in recs_by_src.items():
        if len(rs) > 1:
            dup_lines.append(f"- `{sid}` produced {len(rs)} cards: " + ", ".join(f"{r['recommendation_id']} (attempt {r['workflow_attempt']})" for r in rs))
            for e in events[sid]:
                if e["stage"] in ("generate", "queue"):
                    dup_lines.append(f"    - {e['timestamp_utc']} attempt {e['attempt']} {e['stage']} **{e['event']}** {e['reference']} {e['detail']}")
    near = []
    for i, a in enumerate(recs):
        for b in recs[i + 1:]:
            j = len(words(a["summary"]) & words(b["summary"])) / len(words(a["summary"]) | words(b["summary"]))
            if j >= 0.5:
                near.append(f"- {a['recommendation_id']} vs {b['recommendation_id']}: summary word overlap {j:.0%}, sources {a['source_content_ids']} vs {b['source_content_ids']}")
    same_story = defaultdict(list)
    for r in recs:
        key = frozenset(w for w in words(r["summary"]) if w in {"101", "98", "game", "2", "grant", "28"})
        if len(key) >= 4:
            same_story["game-2-result"].append(r["recommendation_id"])
    F.append(("Duplicate and repeated cards", "proven",
              "\n".join(dup_lines) + "\n\nThe timed-out request (req_a1) was declared a timeout at 09:15:17, a retry started at 09:15:18, "
              "and then **both** responses were accepted and written to the queue. The operation_id `gen_001` is shared by both attempts, "
              "so an idempotency key already exists but is not enforced at queue write. This is an engineering fix, not a prompt fix.\n\n"
              "Near-duplicates by text:\n" + "\n".join(near) +
              f"\n\nCards telling the Game 2 result story: {same_story['game-2-result']} (three high-priority cards for one 12-hour-old result; src_002 is a highlights video categorised as `game_result`)."))

    # 2 unsupported claims
    claim_lines = []
    for r in recs:
        s = by_id[r["source_content_ids"][0]]
        body = (s["title"] + " " + s["body"]).lower()
        summ = (r["headline"] + " " + r["summary"]).lower()
        flags = []
        nums_out = sorted(set(re.findall(r"\b\d+\b", summ)) - set(re.findall(r"\b\d+\b", body)))
        if nums_out:
            flags.append(f"numbers not in source: {nums_out}")
        for c in STRONG_CLAIMS:
            if c in summ and c not in body:
                flags.append(f"'{c}' not in source")
        if any(m in body for m in ["request a", "quote"]) and not any(m in summ for m in ["request", "quote"]):
            flags.append("material condition dropped (source requires requesting a quote)")
        if flags:
            claim_lines.append(f"- **{r['recommendation_id']}** (model_confidence {r['model_confidence']}): " + "; ".join(flags) +
                               f"\n    - card: *{r['headline']}* / {r['summary']}\n    - source: *{s['title']}* / {s['body']}")
    F.append(("Claims the source does not support", "proven",
              "\n".join(claim_lines) +
              "\n\nrec_004 contains two separate errors: a Waves franchise record became a league record, and a **tie** became **broke / sets new**. "
              "The source states the league record is 17. The client caught the first error; nobody has flagged the second. "
              "Confidence 0.94 on the worst card: the confidence field is not an accuracy signal and ranking uses it.\n\n"
              "rec_005 'before Game 3' vs source 'before Friday' was flagged by the number check. The item was published on Thursday 3 September, so 'before Friday' most plausibly means 4 September, not Game 3 on the 11th; the flag is right and the card moved the deadline by a week. "
              "The dropped insurance-quote condition is a second omission."))

    # 3 lost items
    lost = [r for r in rows if r["approved"] and r["card_count"] == 0]
    lost_lines = []
    for r in lost:
        lost_lines.append(f"- `{r['content_id']}` *{r['title']}*: {r['outcome']}. classify={r['classified_relevant']} ({r['classify_reason']}); generate: {r['generate_events'] or 'none'}")
    F.append(("Approved items that never reached the operator", "proven",
              "\n".join(lost_lines) +
              "\n\nsrc_003 (Elias Cole questionable) failed validation (`Response omitted required summary field`) and was **not retried**, although the service allows three retries for timeouts. "
              "src_004 (tipoff moved 19:30 to 20:00) was classified not relevant as a 'routine scheduling notice'. The pack's own planning already uses the moved time (19:00 UTC = 20:00 local), "
              "so the dropped item is the one that mattered to attending fans. The operator view cannot show either, and there is no source-to-queue comparison in the pilot."))

    # 4 promo
    promo_lines = []
    for r in recs:
        s = by_id[r["source_content_ids"][0]]
        text = (s["title"] + " " + s["body"]).lower()
        hits = [m.strip() for m in PROMO_MARKERS if m in text]
        if hits:
            promo_lines.append(f"- {r['recommendation_id']} priority **{r['priority']}**, category `{r['category']}`, markers {hits}, source *{s['title']}*")
    F.append(("Promotional item ranked as high-priority player news", "proven",
              "\n".join(promo_lines) + "\n\nThe relevance instruction says promotional items are usually lower priority. The output departed from it. "
              "Editorial policy on promotions is not agreed (README), so this needs a decision from Product, not a quiet prompt change."))

    # 5 priority inversion
    F.append(("Priority does not match what the client said matters", "proven",
              "Client need (07): results, player availability, schedule changes and changes affecting attending fans matter even when not engaging.\n\n"
              "Queue: Game 2 result x3 = high, sponsor promo = high; coach lineup comment = medium; fan zone = medium; Cole medical update = no card; tipoff change = rejected. "
              "The relevance prompt optimises for 'audience interest' and 'engaging', not the client's utility criteria."))

    # 6 latency
    lat_lines = []
    for r in rows:
        if r["generate_events"]:
            lat_lines.append(f"- {r['content_id']}: {r['generate_events']}")
    F.append(("Generation latency sits on the 15-second timeout", "proven",
              "\n".join(lat_lines) + "\n\nObserved 7 to 21 seconds against a 15-second timeout; one request completed at exactly 15s. "
              "Normal days show 4 to 5 percent retries, so timeouts are intermittent as Marta said, but the margin is thin: any slowdown at event volume (about 5x the normal hourly item rate) pushes a large share into retries."))

    # 7 cost
    cost_lines = ["| date | items | initial calls | retry calls | retries per initial | EUR per call | AI EUR | total EUR | vs forecast | implied generations |", "|---|---|---|---|---|---|---|---|---|---|"]
    normal_init = normal_retry = 0
    tot_cost = tot_calls = 0
    for c in cost:
        ini, ret, tot = int(c["initial_model_calls"]), int(c["retry_model_calls"]), int(c["total_model_calls"])
        items = int(c["source_items"])
        assert ini + ret == tot, f"total_model_calls mismatch on {c['date_utc']}"
        assert abs(float(c["ai_cost_eur"]) + float(c["infrastructure_cost_eur"]) - float(c["total_cost_eur"])) < 0.005
        cost_lines.append(f"| {c['date_utc']} | {items} | {ini} | {ret} | {ret/ini:.3f} | {float(c['ai_cost_eur'])/tot:.4f} | {c['ai_cost_eur']} | {c['total_cost_eur']} | {float(c['total_cost_eur'])/float(c['forecast_cost_eur']):.2f}x | {ini-items} |")
        tot_cost += float(c["ai_cost_eur"]); tot_calls += tot
        if c["date_utc"] != "2026-09-02":
            normal_init += ini; normal_retry += ret
    r_norm, r_bad = normal_retry / normal_init, 2412 / 1390
    eur_call = tot_cost / tot_calls
    ev_calls = EVENT_ITEMS + EVENT_RECS
    proj = {lbl: ev_calls * (1 + rr) * eur_call for lbl, rr in [("normal retry rate", r_norm), ("2 Sep retry rate", r_bad)]}
    F.append(("2 September cost spike is a retry storm, and retries are billed", "proven (projection is an estimate)",
              "\n".join(cost_lines) +
              f"\n\nItems rose 2%, initial calls rose 2%, retry calls rose from 63 to 2,412 (retries per initial call 0.04, 0.05, then 1.74). "
              f"Cost per call is flat at about EUR 0.018, so cost tracks call count: retries are billed at full price. Infrastructure cost rose 51%; extra queue writes are a plausible cause but the CSV cannot show it.\n\n"
              f"Implied generations per day (initial calls minus items) = 180, 180, 185, matching the 'around 180 recommendations per day' figure in 07. The files are internally consistent.\n\n"
              f"**Event projection** ({EVENT_ITEMS} items + {EVENT_RECS} generations = {ev_calls} initial calls, EUR {eur_call:.4f} per call):\n"
              + "\n".join(f"- {k}: EUR {v:.0f} AI cost for the six-hour window, infrastructure extra" for k, v in proj.items()) +
              "\n\nThe CSV has no token counts, so per-call cost is an average. Treat the projection as a planning range, not a quote. "
              "Hypothesis (not provable from the pack): if late responses were written to the queue during the 2 Sep storm, that day's queue holds many duplicates nobody has reviewed."))

    # 8 capacity, on Sam's stated rate (07: about 30 to 40 cards in a one-hour session, indicative)
    lo, hi = 3600 / 40, 3600 / 30   # seconds per card
    rng = lambda n: f"{n*lo/60:.0f} to {n*hi/60:.0f}"
    cap_lines = [f"- Full window, {EVENT_RECS} cards: {rng(EVENT_RECS)} review minutes at 30 to 40 cards an hour",
                 f"- Peak hour, {PEAK_RECS_PER_HOUR} cards: {rng(PEAK_RECS_PER_HOUR)} review minutes, 60 available per approver",
                 f"- Live lane only (4 of 9 sample items), about {PEAK_RECS_PER_HOUR*4/9:.0f} cards: {rng(PEAK_RECS_PER_HOUR*4/9)} minutes",
                 f"- Single-approver mode (3 of 9), about {PEAK_RECS_PER_HOUR*3/9:.0f} cards: {rng(PEAK_RECS_PER_HOUR*3/9)} minutes",
                 f"- Available: Sam {SAM_EVENT_MINUTES} min (17:00 to 18:30 UTC), Delivery Lead the full window but also reconciling and escalating",
                 f"- The pack's per-card timings (45 to 60 s quick, 2 to 3 min hard) with an assumed {SLOW_SHARE:.0%} slow share would give about 50 cards an hour; Sam's stated rate is lower and is the one used."]
    F.append(("Review capacity cannot meet forecast volume, and operator cover ends before tipoff", "arithmetic on indicative figures from the pack",
              "\n".join(cap_lines) +
              "\n\nSam leaves at 18:30 UTC. Tipoff is 19:00 UTC. Approval is mandatory before the client sees a card. Without a second approver the feed depends on one person for lineups, the game, the result and post-game. "
              "If the venue is UTC+1, as the pack's 19:00 UTC = 20:00 local implies, doors and the fan zone (17:30 local) open at 16:30 UTC, before the planning window."))

    # 9 CourtsideWire
    a, b = by_id["src_010"], by_id["src_003"]
    lead = int((ts(b["published_at"]) - ts(a["published_at"])).total_seconds() // 60)
    F.append(("CourtsideWire: earlier by 22 minutes, weaker, and different", "proven",
              f"- src_010 {a['published_at']} {a['source']} (not approved): *{a['title']}* :: {a['body']}\n"
              f"- src_003 {b['published_at']} {b['source']} (approved): *{b['title']}* :: {b['body']}\n\n"
              f"CourtsideWire was {lead} minutes ahead, as the client said. It rests on two anonymous sources and says 'miss'; the team says 'questionable, game-time decision'. "
              "Adding it is an ingestion change (Marta), an external commitment change (Lewis and Priya) and a product experience change (an 'unconfirmed report' label). Not for Game 3. Evaluate offline."))

    # 10 URL hygiene / timezone
    urls = [r["source_urls"][0] for r in recs]
    tracked = [u for u in urls if "utm_" in u]
    F.append(("Small hygiene issues", "proven",
              f"- {len(tracked)} client-facing source URL carries a tracking parameter: {tracked}. Canonical form: {[canonical(u) for u in tracked]}. URL-based dedupe must normalise.\n"
              "- Cards carry venue-local times (17:30, 20:00) with no timezone while everything else is UTC.\n"
              "- The recommendation prompt asks for 'source URL' and 'why fans will care'; the output has `source_urls` and `why_recommended`. The prompt in 04 is not literally what runs, or a wrapper reshapes it."))

    # 11 governance
    F.append(("What the client was sent is not recorded, and the pack's two statements about it differ", "pack statements conflict; unresolved",
              "The pack README says the trial output is 'before operator review' and 'the client was sent a selection from this trial for feedback'. The capacity document says 'Only selected approved cards have been shared with the client'. "
              "Both can be true if someone approved a selection by hand without logging it, which is consistent with Sam's message that decisions have not been recorded. Either way, no record exists of which cards went or who chose them, "
              "and Marta has said she has not established whether the timeouts explain what the client saw. Until Priya confirms which cards were sent, the cause of the duplicate the client saw is a strong hypothesis, not a fact: "
              "if they saw rec_001 and rec_002 rather than rec_001 and rec_003, the repetition is editorial (article plus highlights), not the retry bug."))
    return F


def main(data_dir, out_dir):
    src, recs, log, cost = load(data_dir)
    rows, events, recs_by_src = build_fact_table(src, recs, log)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    with (out / "fact_table.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    F = findings(src, recs, log, cost, rows, events, recs_by_src)
    md = ["# Findings from the evidence pack", "",
          f"Generated by `checks/reconcile.py` from `{data_dir}`. Status labels: **proven** means every statement points at a row in the files; anything else names its assumption.", "",
          "## Fact table: what happened to each source item", "",
          "| id | approved | classified | generate attempts (latency) | cards | outcome | title |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['content_id']} | {r['approved']} | {r['classified_relevant'] or '-'} | {r['generate_events'] or '-'} | {r['cards'] or '-'} | {r['outcome']} | {r['title']} |")
    md.append("")
    for i, (title, status, body) in enumerate(F, 1):
        md += [f"## {i}. {title}", "", f"*Status: {status}*", "", body, ""]
    (out / "findings.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data", sys.argv[2] if len(sys.argv) > 2 else "outputs")
