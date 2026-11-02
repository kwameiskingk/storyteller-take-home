# Aurora Basketball League content service: Game 3 delivery recommendation

Take-home submission for the Delivery Lead, AI-Enabled Products role at Storyteller.
Candidate: Kwame Mbugua. Scenario clock: Thursday 3 September 2026, 12:00 UTC.

This README is the main document. **For the most readable version, open `brief/index.html` in a browser** (download or clone the repository first; GitHub does not render HTML files). It carries the same content with section navigation and links to every file. Everything either one refers to is in the folders below, written as the documents I would actually send to each person.

| Folder | What is in it |
|---|---|
| `brief/` | `index.html`, the delivery brief: this document with section navigation and links to every file |
| `data/` | The evidence pack, unchanged |
| `checks/` | `reconcile.py` joins sources, log and queue and writes the findings; `numbers.py` computes every figure quoted in prose; `test_reconcile.py` holds hand-counted expectations |
| `prompts/` | Current and revised AI instructions, the runner that tests them live, the comparison builder |
| `ops/` | Client update, decision note for Lewis, cost note for Amira, Marta's Friday list, operator checklist, decision log, event runbook, plan and RACI |
| `outputs/` | Generated results: fact table, findings, numbers, prompt before and after, raw prompt runs |
| `ai_log/` | How AI was used, what was accepted, changed, checked and rejected |

## 1. Recommendation

**Launch for Game 3 at reduced scope. Confirm or withdraw to the client on Monday 7 September against stated acceptance criteria. Stop conditions on the night.** Not full scope, not a withdrawal.

Reduced scope means:
- A live lane of four card types: results, player availability, schedule or venue changes, and official records or statistics. Previews and statements sit in a medium lane released only when the live lane is clear.
- Official league and team feeds plus the approved broadcaster. No CourtsideWire for Game 3.
- Every card approved by a person before the client sees it. The client's manual monitoring stays on as the system of record for this event.
- No promotional cards until Product sets the policy.
- Sam approves 17:00 to 18:30 UTC. After that I am the only approver unless Lewis and Priya find a second, which I am asking for now.

**Why not full scope.** In the ten-item replay the pilot produced a duplicate from a retry bug, fabricated a record claim at 0.94 confidence, lost the player availability update silently, rejected the tipoff change as routine, and ranked a sponsor competition high. Forecast volume is 240 cards in six hours with peaks of 80 an hour. Sam reviews 30 to 40 an hour.

**Why not withdraw.** The causes are specific. Two are bounded engineering changes that Marta can size for her Friday window. The rest are instructions and process I control. The client keeps a safety net, so a reduced launch risks little and proves the service in the window Product cares about.

**Does the volume fit?** This is the question the recommendation stands or falls on. In the sample, four of nine approved items fall in the live lane, 44 percent. Applied to the 80-card peak, that is about 36 cards an hour reaching the approver, with duplicates removed and promotions filtered. Sam's observed rate is 30 to 40 an hour. So reduced scope sits at the limit of one approver with no slack for hard cases. That is why the second approver is an explicit ask, and why queue dwell is a stop condition rather than a hope. Monday's logged session replaces the sample share with a measured one.

**The ten-minute target.** The client wants developments surfaced within about ten minutes. The poll alone takes up to five. Generation took 7 to 21 seconds in the replay, up to about 36 with one timeout and retry. A quick review is about a minute. That leaves roughly three and a half minutes for a card to wait in the queue. At 36 cards an hour that is achievable for one approver who does nothing else. It is not achievable if the same person is also reconciling and escalating through the result peak.

### Acceptance criteria for Monday 7 September (proposed to Lewis, since none exist today)
1. Marta's items 1 and 2 deployed by 13:00 Friday.
2. The ten-item replay rerun through the deployed pipeline shows one card for src_001 and a card or a visible failure for src_003.
3. Sam has source export access and has completed one logged session with the checklist on Monday.
4. No fabricated fact in Monday's logged session.

Tuesday's 20-card labelled set is a second checkpoint. A fabricated fact or more than one duplicate withdraws the launch, and the client hears Tuesday evening, before Wednesday's training.

### Stop conditions on the night, each with how it is observed
- A factual error reaches the client. Observed by client report or by the approver.
- Cards wait more than ten minutes for 30 consecutive minutes. Observed from decision log timestamps.
- No approver online.
- Two duplicate cards from one source in the queue, or retries per call above 0.25 over 30 minutes if Marta's export ships. There is no live spend telemetry, so this is Finance's trigger.

### What would change my recommendation
- To full scope: a clean 20-card set, Monday's session showing the slow-review share well under my 20 percent assumption, and Lewis releasing the medium lane.
- To withdraw: Marta ships item 1 only. Or the client will not keep manual monitoring. Or Monday's session shows Sam under 30 cards an hour with the checklist. Or no second approver and the measured live-lane share is well above 44 percent.
- On CourtsideWire: a four-week background comparison after Game 3 measuring lead time and contradiction rate against official feeds. If the lead is real and contradictions are rare, I would propose a labelled unconfirmed-report lane, designed with Lewis.

## 2. Evidence

Everything below is reproduced by `checks/reconcile.py` and written to `outputs/findings.md` with the rows quoted. The fact table for the ten source items is `outputs/fact_table.csv`. Every number is computed in `checks/numbers.py`.

| Finding | Status | Source |
|---|---|---|
| Duplicate: the timed-out request completed anyway and both responses were written to the queue | proven | log rows gen_001, attempts 1 and 2 |
| Mensah card: a tied franchise record became a broken league record, two errors, confidence 0.94 | proven | rec_004 vs src_005 |
| Elias Cole availability update lost on a validation failure, never retried, invisible to the operator | proven | log row gen_003 |
| Tipoff change classified routine, no card | proven | log row cls_004 |
| Sponsor competition ranked high as player news, entry condition dropped | proven | rec_005 vs src_006 |
| Generation latency 7 to 21 seconds against a 15-second timeout | proven | log timestamps |
| 2 September: retries per call 0.04, 0.05, then 1.74, cost per call flat, so retries are billed | proven | cost CSV |
| Event AI cost EUR 32 to 84 for the window depending on retry rate | estimate | cost CSV, Product volume estimate |
| 240 cards need about 288 review minutes at an assumed 20 percent slow share | arithmetic on an assumption | capacity document |
| Sam leaves 30 minutes before tipoff | proven | capacity document |
| CourtsideWire 22 minutes earlier, anonymous sourcing, "miss" where the team said "questionable" | proven | src_010 vs src_003 |
| The client received a selection from a queue marked before operator review; who selected it is unrecorded | proven | pack README |
| Event hourly item rate about 5x a normal day | proven | cost CSV, Product estimate |

Hypothesis, labelled as such: if late responses were written to the queue during the 2 September retry storm, that day's queue holds many unreviewed duplicates. The pack has no 2 September queue data.

## 3. Taking the work forward

Full plan, deadlines pulled from each message, and RACI in `ops/plan_and_raci.md`.

**The order of communication matters because of the remit.** The client cannot be offered a changed service before Lewis and Priya agree. Marta cannot be promised to the client before she has seen the evidence. So:

| When (UTC) | To | What | File |
|---|---|---|---|
| Thu 15:00 | Client, via Priya | Faults confirmed, causes found, position on Monday. No new scope, no promises | `ops/client_update_thursday_1500.md` |
| Thu evening | Marta | Ranked, evidence-backed list, right under any launch decision | `ops/marta_friday_list.md` |
| Thu evening | Lewis | Heads-up: reduced-scope recommendation at 10:00 and the six decisions he owns | |
| Thu evening | Amira | Cost analysis and proposed allowance with an observable trigger | `ops/amira_event_allowance.md` |
| Fri 10:00 | Lewis and Priya | Decision note, 30-minute call | `ops/lewis_decision_note.md` |
| Fri 13:00 | Me | Record what Marta shipped. This can change the recommendation | |
| Fri afternoon | Sam | Checklist, decision log, export access | `ops/operator_review_checklist.md`, `ops/decision_log_template.csv` |
| Mon evening | Client, via Priya | Go or withdraw at reduced scope, against the criteria | |
| Wed 13:00 | Client editors | Training, with Priya | |
| Fri 11 Sep | Everyone | Runbook | `ops/event_runbook.md` |

**What I do personally.** The reconciliation and the documents in this pack. The 15:00 client update. Marta's list tonight. The decision note for 10:00 Friday. Sam's checklist and two supervised sessions. The 20-card labelled set on Tuesday. The Thursday freeze. Cover 17:00 to 23:00 on the night as approver, reconciler and escalation point, or as reconciler and escalation point if a second approver is found. The post-event reconciliation and review the following week.

**What I ask of others.** Marta: items 1 and 2, export access for Sam, a view on the timeout, a rerun of the replay through the deployed path, and deploying the revised prompts if Product agrees. Sam: use the checklist, log every decision, measure time per card, escalate rather than diagnose. Lewis: the six decisions in the note. Priya: send the client update, confirm which cards the client received, align Wednesday's training, hold the stop message. Amira: agree the allowance and the trigger with Lewis.

**My other two workstreams.** Their Friday 11 September items move to Thursday or the following Monday. Both clients are told on Monday 7 September. No backfill is assumed. Preparation for this account fits in half days because the heavy lifting is in this pack.

## 4. Practical demonstration

The important next step I took as far as I could: **make the evidence reproducible and make the instructions testable outside production.** Every later decision rests on both.

```bash
# 1. Reconcile sources, log and queue. Writes outputs/fact_table.csv and outputs/findings.md.
python3 -I checks/reconcile.py data outputs

# 2. Compute every number quoted in the documents. Writes outputs/numbers.json.
python3 -I checks/numbers.py data outputs

# 3. Check both against hand-counted expectations.
python3 -I checks/test_reconcile.py

# 4. Run current and revised instructions over all ten items, live, through the Claude Code CLI.
python3 -I prompts/run_prompts.py data/01_source_content.json outputs/prompt_runs --model sonnet

# 5. Build the before-and-after comparison with an automatic claim check.
python3 -I prompts/compare_runs.py data/01_source_content.json data/02_trial_recommendations.json outputs/prompt_runs outputs/prompt_before_after.md
```

Step 4 needs either a logged-in Claude Code CLI (default) or an Anthropic API key (`--backend api --model <exact model id>`). Each saved output records the exact model id and run time. The runs used here are committed in `outputs/prompt_runs/` and the comparison in `outputs/prompt_before_after.md`, so the result can be inspected without running anything.

**What it shows.**
- The reconciliation derives the duplicate, the lost item, the rejected item, the latency and the cost pattern from the raw files, with the rows quoted.
- The automatic claim check flags rec_004 and rec_005 in the pilot output. It also flags "before Game 3" against "before Friday" on rec_005, which a human overrules because Game 3 is Friday. That is what the check is for: narrowing what a person must read, not replacing the person.
- The revised instructions, run today, produce a correct Mensah card, reject the sponsor competition as promotional, classify the tipoff change as a high-priority schedule change, keep "questionable" and "sources say", and return an `operator_checks` list instead of a confidence score. For Mensah the checks read "the record is tied, not broken" and "franchise record, not a league record".

**What it does not show.** The current instructions, run on today's model, also got most things right. So the pilot's errors are partly model and pipeline behaviour, and this test proves the instructions are better specified, not that production will behave the same. Only Marta's rerun through the deployed path proves that, which is why it is acceptance criterion 2.

**What still needs human judgment.** Whether a highlights video is a second card. Whether promotions ever belong in the feed. How an unconfirmed report should look. Every approval. The `story_key` the revised prompt emits is a hint for the approver and nothing more: the two Game 2 cards got different keys, and the official Cole update and the CourtsideWire report got the same one. Deduplication stays with engineering, on source and operation IDs.

**Completed.** Reconciliation, number checks, tests, revised instructions tested on ten items, checklist, decision log, Marta's list, Lewis's decision note, Amira's cost note, runbook, plan, client update.

**Unresolved, and what each changes.** Nothing has run through the production pipeline, so the Monday criteria depend on Marta's rerun, not mine. The production model is unknown, so prompt gains are unproven in production. The slow-review share is assumed, so Monday's session decides whether one approver is enough. The 2 September queue is unreconciled, so the duplicate scale is a hypothesis. No labelled set exists yet, so Tuesday is a real checkpoint, not a formality.

## 5. First update to the client

In `ops/client_update_thursday_1500.md`, with the reasoning for what it does and does not say. It confirms both faults with causes, commits only to a Monday position, keeps CourtsideWire open, and asks which cards the client received. It offers no changed service, because Lewis has not yet decided.

## 6. How I used AI and how I checked it

Full chronological log in `ai_log/ai_use_log.md`, with the representative prompt and output.

**My tool of choice was Claude Code.** It read the pack alongside me, wrote the scripts and tests, drafted the revised instructions, and produced the first draft of every document here. I read the pack myself, set the questions, and required it to prove each finding from the data rather than from its reading. I had every number computed by a script because language models misread numbers. I had the pack scanned for hidden text. I commissioned two separate AI review sessions with no access to our conclusions: a cold adversarial read of the pack, then a simulated hiring panel grading the finished draft. I decided what to accept, change and reject from each. The recommendation, the scope, the second-approver ask and the CourtsideWire position are my decisions.

- **Checked.** Every finding cites a row. Tests encode hand counts written before the script ran. Every figure in prose comes from `checks/numbers.py`. The panel found a remit violation in the client update, an impossible gate, unobservable stop conditions, two factual errors and eight contradictions; all are fixed here and listed in the log.
- **Changed.** The client update, rewritten so it precedes Lewis's decision rather than pre-empting it. The Monday gate, rebuilt around Friday's rerun and Monday's session. Stop conditions, rebuilt around what can be observed. The revised instruction's time-zone rule, moved out of headlines.
- **Rejected.** The AI's first framing of the duplicate as a prompt problem; the log shows a retry bug. A reviewer's hypothesis that the client's complaint referred to earlier output, which contradicts the pack and which I had wrongly accepted before the panel caught it. The AI's capacity model of 50 cards an hour, in favour of Sam's observed 30 to 40.
- **Limitations.** The prompt test proves the instructions, not production. Outputs vary between runs; each saved run records the exact model id and time. The story key is not a deduplication key. The AI wrote 8x where the figure is 5x and 45 percent where it is 44, and listed a pack fact as an assumption; the numbers script and the second review caught all three.

## 7. Time, assumptions, and what I left unfinished

**Time spent:** about three and a half hours of my own time across two sittings on 1 and 2 November 2026, with Claude Code working alongside throughout.

**Assumptions:** 20 percent of cards need slow review. EUR per call is a flat average because the CSV has no token counts. Priya sends client messages. The Claude Code CLI stands in for whichever model production uses. Four of nine sample items as the live-lane share.

**Open questions, and what proceeds anyway:** which cards the client received (Marta's fixes proceed). Whether a second approver exists (scope and stop conditions are set for one). The production model (the rerun on Friday answers it). The slow-review share (Monday measures it).

**Deliberately unfinished:** reconciliation of the full 2 September queue (no data). A labelled set beyond ten items (needs Monday and Tuesday output). A CourtsideWire evaluation design beyond the outline above. A dashboard.
