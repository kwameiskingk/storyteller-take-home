#!/usr/bin/env python3
"""Compare current vs revised prompt runs against the source bodies and the pilot's own output.
Usage: python3 -I prompts/compare_runs.py data/01_source_content.json data/02_trial_recommendations.json outputs/prompt_runs outputs/prompt_before_after.md
"""
import json, re, sys
from pathlib import Path

STRONG = ["broke", "break", "sets new", "new league", "league record", "record-breaking"]

def check(card, item):
    """Return list of flags: facts in the card not in the source."""
    if not card or "_error" in card: return ["no card / bad json"]
    body = (item["title"] + " " + item["body"]).lower()
    text = (str(card.get("headline", "")) + " " + str(card.get("summary", ""))).lower()
    flags = []
    nums = sorted(set(re.findall(r"\b\d+\b", text)) - set(re.findall(r"\b\d+\b", body)))
    if nums: flags.append(f"numbers not in source {nums}")
    for s in STRONG:
        if s in text and s not in body: flags.append(f"'{s}' not in source")
    if "quote" in body and "quote" not in text: flags.append("insurance-quote condition dropped")
    if "questionable" in body and "questionable" not in text: flags.append("'questionable' softened or dropped")
    if "sources" in body and "unconfirmed" not in text and "sources" not in text and "report" not in text: flags.append("anonymous sourcing not signalled")
    return flags

def main(src_p, recs_p, runs, out_p):
    items = {i["content_id"]: i for i in json.loads(Path(src_p).read_text())["items"]}
    pilot = {}
    for r in json.loads(Path(recs_p).read_text())["recommendations"]:
        pilot.setdefault(r["source_content_ids"][0], r)
    runs = Path(runs)
    md = ["# Prompt test: current vs revised instructions, run live on the ten pack items", "",
          "Run with `prompts/run_prompts.py` through the Claude Code CLI (model alias `sonnet`). The pilot's production model is not named in the pack, "
          "so this tests the **instructions**, not the production system. Pilot column = what the real pilot produced (02_trial_recommendations.json).", "",
          "| item | pilot | current prompt (today) | revised prompt (today) |", "|---|---|---|---|"]
    detail = []
    for cid, item in items.items():
        cells = []
        p = pilot.get(cid)
        cells.append(f"{p['priority']} / {p['category']}<br>*{p['headline']}*" if p else ("not run (unapproved)" if not item["approved_for_pilot"] else "**no card**"))
        for v in ("current", "revised"):
            f = runs / v / f"{cid}.json"
            if not f.exists(): cells.append("not run"); continue
            d = json.loads(f.read_text()); rel = d["relevance"]; g = d.get("generation")
            if not g:
                cells.append(f"not relevant: {rel.get('category','')}<br>{rel.get('reason','')[:90]}")
                continue
            flags = check(g, item)
            cells.append(f"{g.get('priority')} / {g.get('category')}<br>*{g.get('headline')}*<br>" + ("**flags:** " + "; ".join(flags) if flags else "no unsupported claims"))
            detail.append((cid, v, rel, g, flags))
        md.append(f"| {cid} *{item['title'][:45]}* | " + " | ".join(cells) + " |")
    md += ["", "## Full outputs with checks", ""]
    for cid, v, rel, g, flags in detail:
        md += [f"### {cid} · {v}", "", f"Source: *{items[cid]['title']}* — {items[cid]['body']}", "", "```json", json.dumps({"relevance": rel, "generation": g}, indent=2), "```", "",
               ("**Automatic claim check:** " + "; ".join(flags)) if flags else "**Automatic claim check:** clean", ""]
    Path(out_p).write_text("\n".join(md)); print("\n".join(md[:16]))

if __name__ == "__main__":
    main(*sys.argv[1:5])
