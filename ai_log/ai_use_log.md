# AI use log

Tools: Claude Code (Fable 5.1) as the working partner, Claude Code CLI with the `sonnet` model alias as the stand-in for the pilot's two AI steps, a second Claude Code session as an adversarial reviewer. No paid API, no live infrastructure, no credentials shared.

## Chronology

**1. Read the pack, explain the task in plain English.** I asked Claude to read every file twice and tell me what was being asked. I asked it to also check the job description on getstoryteller.com. Outcome: a plain-language brief and a first list of eight suspected findings. Check: I read the files myself and confirmed each finding was in the data before accepting it.

**2. Prove each finding from the raw files.** Prompt to Claude (abridged): "I want you to prove the duplicate, the false record claim, the silently lost item, the dropped schedule change, the promotional card, the cost spike, the capacity gap and the CourtsideWire difference from the data, not from your reading of it." Outcome: `checks/reconcile.py` and its output. Changed: the first automatic claim check flagged rec_005 for "before Game 3" when the source said "before Friday". Game 3 is Friday. Kept the flag, documented it as a false positive a reviewer overrules.

**3. Adversarial review, cold.** A second session was given only the pack and asked for every problem with proof, a launch recommendation, the common mistakes a candidate would make, and anything easy to overlook. It was not given our conclusions. Outcome: agreement on all eight findings plus eleven additions: Sam leaves before tipoff; Marta's window opens before Lewis decides; latency sits on the timeout; the Mensah card has two errors not one; the giveaway card dropped the insurance-quote condition; the client saw drafts marked before operator review; the complaint timeline is implausibly tight; the planning window misses doors and fan zone; cards carry local times with no zone; a client-facing URL carries a tracking parameter; most of the pilot queue was never reviewed. All adopted. Disagreement: none material. It proposed stricter kill criteria and a EUR 100 allowance with a trigger, which I adopted over my looser version.

**4. Prompt test harness.** Claude wrote `prompts/run_prompts.py` to run both instruction sets over the ten items through the CLI. First run failed on a syntax error, fixed, rerun. Outcome in `outputs/prompt_runs/` and `outputs/prompt_before_after.md`.

**5. Finding that changed my view.** The *current* prompt, run on today's model, produced a correct Mensah card, rejected the giveaway and surfaced the tipoff change. So the pilot's errors are partly model and pipeline behaviour, not just wording. My prompt test proves the instructions are better specified; it does not prove the production system will behave the same. That is why Marta's list asks her to run the revised prompts through the replay path, and why the Monday gate depends on that run, not on mine.

**6. Prompt revision v2.** The first revised generation prompt put "(zone not stated)" in headlines ("Game 3 fan zone opens at 17:30 (zone not stated)"). Rewrote rule 4 to send that to `operator_checks` and rule 5 to name the teams the source names, because one headline had said "beat opponent". Reran src_002 and src_007. v1 outputs kept in `outputs/prompt_runs_v1/`.

**7. Limitation found.** The `story_key` field meant to help Sam spot repeats came back as "game 2 result kings waves" for the article and "game 2 result metro kings" for the video. Useful hint for a human, useless as a machine key. Deduplication stays with engineering.

**8. Documents.** Claude drafted the checklist, decision log, Marta's list, runbook, plan and RACI, and the README. I edited for voice, removed anything I could not stand behind in an interview, and checked every number against `outputs/findings.md`.

## Representative prompt and output

Revised generation instruction (`prompts/revised_generation.txt`) applied to src_005:

Input: "Tayo Mensah ties Waves playoff assists record. Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17."

Output:
```json
{
  "category": "Player records",
  "priority": "high",
  "headline": "Mensah ties Waves franchise playoff assists record with 12",
  "summary": "Tayo Mensah recorded 12 assists in Game 2, tying the Harbour City Waves' franchise record for assists in a playoff game. The Aurora Basketball League playoff record is 17.",
  "operator_checks": [
    "Tayo Mensah recorded 12 assists",
    "The assists came in Game 2",
    "The record is tied, not broken",
    "The record is the Harbour City Waves' franchise record, not a league record",
    "The record covers assists in a playoff game",
    "The Aurora Basketball League playoff record is 17"
  ]
}
```
Pilot output for the same item: "Mensah sets new league playoff assists record / Tayo Mensah broke the Aurora Basketball League playoff record with 12 assists in Game 2." confidence 0.94.

## What the AI got wrong or could not do
- Confident first framing of the duplicate as a prompt issue before the log was read. Corrected by the data.
- A syntax error in the first runner.
- Could not name the production model, access the 2 September queue, or measure the slow-review share. Those are labelled assumptions or open questions.
- Its outputs are non-deterministic. The committed runs are one sample; a rerun will differ in wording. The automatic claim check exists so that a rerun can be checked the same way.
