#!/usr/bin/env python3
"""Run the current and revised prompts over every source item using the Claude Code CLI (`claude -p`).

This is the same two-step workflow as the pilot (relevance, then generation) run outside production,
which is what the brief allows Delivery to do. Outputs land in outputs/prompt_runs/<variant>/<content_id>.json.

Usage: python3 -I prompts/run_prompts.py data/01_source_content.json outputs/prompt_runs [--model sonnet] [--only src_005]
Requires: `claude` CLI logged in. ANTHROPIC_API_KEY is unset for the child so the claude.ai login is used.
"""
import argparse, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VARIANTS = {"current": ("current_relevance.txt", "current_generation.txt"),
            "revised": ("revised_relevance.txt", "revised_generation.txt")}


def ask(system_prompt, item, model):
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    user = ("Source item:\n" + json.dumps({k: item[k] for k in ("content_id", "title", "body", "source", "published_at", "url")}, indent=2)
            + "\n\nRespond with JSON only.")
    out = subprocess.run(["claude", "-p", "--model", model, "--system-prompt", system_prompt, user],
                         capture_output=True, text=True, env=env, timeout=180)
    text = out.stdout.strip()
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else {"_raw": text, "_error": "no json"}
    except json.JSONDecodeError:
        return {"_raw": text, "_error": "bad json"}


def run_item(item, variant, model, out_dir):
    rel_p, gen_p = [(HERE / f).read_text() for f in VARIANTS[variant]]
    result = {"content_id": item["content_id"], "variant": variant, "model": model, "relevance": ask(rel_p, item, model)}
    rel = result["relevance"].get("relevant")
    if rel is True or str(rel).lower() == "true":
        result["generation"] = ask(gen_p, item, model)
    (out_dir / variant / f"{item['content_id']}.json").write_text(json.dumps(result, indent=2))
    print(f"{variant:8}{item['content_id']}: relevant={rel}", flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_json"); ap.add_argument("out_dir")
    ap.add_argument("--model", default="sonnet"); ap.add_argument("--only", default=None)
    ap.add_argument("--variants", default="current,revised"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    items = json.loads(Path(a.source_json).read_text())["items"]
    if a.only:
        items = [i for i in items if i["content_id"] in a.only.split(",")]
    out = Path(a.out_dir)
    jobs = []
    for v in a.variants.split(","):
        (out / v).mkdir(parents=True, exist_ok=True)
        jobs += [(i, v) for i in items]
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda j: run_item(j[0], j[1], a.model, out), jobs))


if __name__ == "__main__":
    main()
