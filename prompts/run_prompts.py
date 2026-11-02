#!/usr/bin/env python3
"""Run the current and revised instructions over every source item, outside production.

Same two-step shape as the pilot (relevance, then card generation). Two routes:
  --backend cli   uses the Claude Code CLI (`claude -p`) with the account already logged in. Default.
  --backend api   uses the Anthropic API with ANTHROPIC_API_KEY (pip install anthropic).
Each output records the exact model id reported by the route, the run time, and the raw text, so a rerun
can be compared like for like.

Usage: python3 -I prompts/run_prompts.py data/01_source_content.json outputs/prompt_runs [--model sonnet]
                                          [--backend cli|api] [--variants current,revised] [--only src_005]
"""
import argparse, datetime, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
VARIANTS = {"current": ("current_relevance.txt", "current_generation.txt"),
            "revised": ("revised_relevance.txt", "revised_generation.txt")}
ITEM_FIELDS = ("content_id", "title", "body", "source", "published_at", "url")


def user_message(item):
    return "Source item:\n" + json.dumps({k: item[k] for k in ITEM_FIELDS}, indent=2) + "\n\nRespond with JSON only."


def ask_cli(system_prompt, item, model):
    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    out = subprocess.run(["claude", "-p", "--model", model, "--output-format", "json",
                          "--system-prompt", system_prompt, user_message(item)],
                         capture_output=True, text=True, env=env, timeout=180)
    try:
        payload = json.loads(out.stdout[out.stdout.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return out.stdout.strip(), "unknown"
    model_ids = list((payload.get("modelUsage") or {}).keys())
    return payload.get("result", ""), (model_ids[0] if model_ids else model)


def ask_api(system_prompt, item, model):
    import anthropic  # pip install anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(model=model, max_tokens=800, temperature=0, system=system_prompt,
                                 messages=[{"role": "user", "content": user_message(item)}])
    return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text"), msg.model


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {"_raw": text, "_error": "no json"}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"_raw": text, "_error": "bad json"}


def run_item(item, variant, model, backend, out_dir):
    ask = ask_api if backend == "api" else ask_cli
    rel_p, gen_p = [(HERE / f).read_text() for f in VARIANTS[variant]]
    rel_text, model_id = ask(rel_p, item, model)
    result = {"content_id": item["content_id"], "variant": variant, "backend": backend,
              "model_requested": model, "model_id": model_id,
              "run_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "relevance": parse_json(rel_text), "relevance_raw": rel_text}
    rel = result["relevance"].get("relevant")
    if rel is True or str(rel).lower() == "true":
        gen_text, _ = ask(gen_p, item, model)
        result["generation"] = parse_json(gen_text)
        result["generation_raw"] = gen_text
    (out_dir / variant / f"{item['content_id']}.json").write_text(json.dumps(result, indent=2))
    print(f"{variant:8}{item['content_id']}: relevant={rel} model={model_id}", flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_json"); ap.add_argument("out_dir")
    ap.add_argument("--model", default="sonnet", help="CLI alias (sonnet) or exact API model id")
    ap.add_argument("--backend", choices=("cli", "api"), default="cli")
    ap.add_argument("--only", default=None); ap.add_argument("--variants", default="current,revised")
    ap.add_argument("--workers", type=int, default=4)
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
        list(ex.map(lambda j: run_item(j[0], j[1], a.model, a.backend, out), jobs))


if __name__ == "__main__":
    main()
