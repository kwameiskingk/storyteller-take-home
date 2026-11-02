# Aurora Basketball League content service: Game 3 delivery recommendation

Take-home submission for the Delivery Lead, AI-Enabled Products role at Storyteller.
Candidate: Kwame Mbugua. Scenario clock: Thursday 3 September 2026, 12:00 UTC.

**For the most readable version, open `brief/index.html` in a browser** after downloading or cloning the repository (GitHub does not render HTML files). It carries the same content as this README with section navigation and links to every file. This README is the plain-text version.

| Folder | What is in it |
|---|---|
| `brief/` | `index.html`, the delivery brief |
| `data/` | The evidence pack, unchanged |
| `data_extra/` | Four test cases I wrote, labelled as my own |
| `checks/` | `reconcile.py` joins the pack's sources, processing log and queue and writes the findings; `numbers.py` computes every figure quoted in prose; `event_checks.py` is the generic duplicate, lost-item and dwell check for use on an event export; `test_reconcile.py` holds expected values read from the files |
| `prompts/` | Current and revised AI instructions, the runner that tests them, the comparison builder |
| `ops/` | One document per person: client update and note to Priya, decision note for Lewis, cost note for Amira, Marta's Friday list, Sam's checklist and decision log, event runbook, plan and RACI |
| `outputs/` | Generated results: fact table, findings, numbers, prompt comparison, every saved prompt run |
| `ai_log/` | How AI was used: accepted, changed, checked and rejected |

A note on names used below. The pack numbers the ten source items src_001 to src_010 and the eight pilot cards rec_001 to rec_008. "Marta's items 1 and 2" are the first two entries on her Friday list: stop writing a card from a request already marked timed out, and retry or surface validation failures.

## 1. Recommendation

**Launch for Game 3 at reduced scope. Confirm or withdraw to the client on Monday 7 September against the acceptance criteria below. Pause on the night if any stop condition fires.**

Reduced scope means:
- **Live lane**, approved during the game: results, player availability updates from a team or the league, changes to tipoff, doors, venue or travel, and official records or statistics.
- **Held lane**, released when the live lane is clear: previews and analysis, coach or team statements that confirm no decision, routine fan information such as the fan zone programme, and video or highlights of a result already reported. Promotional items are held until Product sets a policy.
- Official league and team feeds plus the approved broadcaster only. No CourtsideWire for this game.
- Every card approved by a person before the client sees it. The client's own monitoring of official feeds stays on as the system of record for this event.
- Sam approves 17:10 to 18:30 UTC. After 18:30, either a second approver confirmed by Lewis and Priya, or **single-approver mode**: I approve results, availability and schedule or venue changes only, and records join the held lane.

**Why not full scope.** In the ten-item replay the pilot produced a duplicate card from a retry fault, fabricated a record claim at 0.94 confidence, lost the player availability update silently, rejected the tipoff change as routine, and ranked a sponsor competition as high-priority player news. Forecast volume is 240 cards in six hours with peaks of 80 an hour. Sam reviews about 30 to 40 cards an hour and leaves thirty minutes before tipoff. A full launch would put wrong or missing information in front of the editors during the Finals, at a volume nobody can review.

**Why not withdraw.** The causes are specific and each has an owner. The duplicate and the lost item are bounded engineering changes that Marta can size for her Friday window. The record claim, the rejected schedule change and the promotion are instruction and process changes, drafted and tested outside production. The client keeps its safety net. Withdrawing from a fixable problem gives up the one event Product wants to prove the service on.

**Does the volume fit?** Four of the nine approved sample items are live-lane types, 44 percent. Applied to the 80-card peak, about 36 cards an hour reach the approver. At Sam's stated rate of 30 to 40 an hour, that is 53 to 71 minutes of review in a 60-minute hour. One approver is at or over the limit. If the highlights video or routine fan information were live as well, the figure rises to 44 or 53 cards an hour, which is why both are held. Single-approver mode, three of nine, is about 27 cards and 40 to 53 minutes. These shares come from a ten-item sample that the pack says is not representative; Monday's logged session replaces them with a measured figure before the client is told anything. Figures from `checks/numbers.py`.

**The ten-minute target.** The client wants developments surfaced within about ten minutes of appearing in an approved source. Polling alone takes up to five minutes. Generation took 7 to 21 seconds in the replay; the one timeout-and-retry path took 26 seconds, and 36 is the worst case from the observed figures. A quick review is about a minute. That leaves roughly three and a half minutes for a card to wait in the queue. Achievable for one approver who does nothing else. Harder if that person is also reconciling exports and escalating through the result peak, which is the case for single-approver mode.

**CourtsideWire.** The client is right that it was 22 minutes ahead of the official update. It also rested on two anonymous sources and said "expected to miss" where the team said "questionable, game-time decision". One item cannot show whether a source is reliable. Adding it needs an ingestion change from Marta, a change to what Priya has told the client, and a product decision on how an unconfirmed report should look. After Game 3 I would run it in the background for four weeks and record, for every story, how far ahead it was and whether an official source later confirmed, contradicted or never addressed it. If the lead is real and contradictions are rare, I would propose a labelled unconfirmed-report lane, designed with Lewis.

### Acceptance criteria for Monday 7 September (proposed to Lewis, since none exist today)
1. Marta's items 1 and 2 deployed by 13:00 Friday.
2. The ten-item replay rerun by Marta through the deployed pipeline shows one card for src_001 and a card or a visible failure for src_003.
3. Sam has source export access and has completed one logged session with the checklist on Monday.
4. No fabricated fact in Monday's logged session.
5. Either a second approver is confirmed for 18:30 to 23:00, or single-approver mode is agreed and the client is told that records and context cards arrive after the game.

Tuesday's 20-card labelled set is a second checkpoint. A fabricated fact or more than one duplicate withdraws the launch, and the client hears on Tuesday evening, before Wednesday's training.

### Stop conditions on the night
Delivery cannot stop live processing and no engineer is on duty. "Pause" means approvers approve nothing further, so no new card reaches the client, and Priya or someone she names tells the editors to rely on manual monitoring. Each condition names its observer.
- A factual error reaches the client. Observed by client report or by the approver.
- Cards wait more than ten minutes for 30 consecutive minutes. Observed from the decision log, which records the card's generation time and the decision time.
- No approver online.
- Two duplicate cards from one source in the queue, or retries per call above 0.25 over 30 minutes if Marta's export carries attempt counts. This is the trigger proposed to Finance, because spend cannot be seen live.

### What would change my recommendation
- **To full scope:** a clean 20-card set, Monday's session showing a live-lane share at or below the sample figure with Sam at or above 40 cards an hour, and Lewis releasing the held lane.
- **To withdraw:** Marta ships item 1 only, because validation failures would still silently lose availability updates. The client will not keep manual monitoring. Monday's session shows Sam under 30 cards an hour with the checklist. Or no second approver and a measured live-lane share well above 44 percent.

## 2. Evidence

Everything below is reproduced by `checks/reconcile.py` and written to `outputs/findings.md` with the rows quoted. The fact table for the ten source items is `outputs/fact_table.csv`.

| Finding | Status | Source |
|---|---|---|
| The timed-out request completed anyway and both responses were written to the queue, giving two identical cards | proven | log rows gen_001, attempts 1 and 2 |
| Mensah card turned a tied franchise record into a broken league record. Two errors, confidence 0.94 | proven | rec_004 vs src_005 |
| Elias Cole availability update lost on a validation failure, never retried, invisible to the operator | proven | log row gen_003 |
| Tipoff change classified as a routine notice, no card | proven | log row cls_004 |
| Sponsor competition ranked high as player news; the card dropped the insurance-quote condition and moved "before Friday" to "before Game 3" | proven | rec_005 vs src_006 |
| Generation latency 7 to 21 seconds against a 15-second timeout | proven | log timestamps |
| 2 September: retries per call 0.04, 0.05, then 1.74 with flat cost per call, so retries are billed | proven | cost CSV |
| Event AI cost EUR 32 to 84 for the window, depending on retry rate | estimate | cost CSV, Product estimate |
| 240 cards need 360 to 480 review minutes at Sam's stated rate | estimate | capacity document |
| Sam leaves 30 minutes before tipoff | proven | capacity document |
| CourtsideWire 22 minutes earlier, anonymous sourcing, "miss" where the team said "questionable" | proven | src_010 vs src_003 |
| Event hourly item rate about 5x a normal day | proven | cost CSV, Product estimate |
| What the client was sent is unrecorded, and the pack's two statements about it differ | pack conflict | pack README vs capacity document |
| The 2 September queue holds many unreviewed duplicates from the retry storm | hypothesis | no 2 Sep queue data |

Two things follow from the last two rows. The cause of the duplicate the client saw is a strong hypothesis until Priya confirms which cards were sent: if they saw the recap and the highlights video, the repetition is editorial rather than the retry fault. And the venue time zone is inferred from one pair of times in the pack (19:00 UTC, 20:00 local), not stated.

## 3. Taking the work forward

Full plan, the deadlines from each message, and the RACI in `ops/plan_and_raci.md`. The order of communication follows from the remit: the client cannot be offered a changed service before Lewis and Priya agree, and Marta cannot be promised to the client before she has seen the evidence.

| When (UTC) | To | What | File |
|---|---|---|---|
| Thu 15:00 | Priya, then the client | Note to Priya; message for Jordan confirming the faults, giving what we know about causes, committing to a Monday position | `ops/client_update_thursday_1500.md` |
| Thu evening | Marta | Ranked, evidence-backed list, each item right whatever Lewis decides | `ops/marta_friday_list.md` |
| Thu evening | Lewis | Heads-up: reduced-scope recommendation at 10:00 and the six decisions he owns | |
| Thu evening | Amira | Cost analysis, EUR 100 allowance, the observable trigger | `ops/amira_event_allowance.md` |
| Fri 10:00 | Lewis and Priya | Decision note, 30-minute call | `ops/lewis_decision_note.md` |
| Fri 13:00 | Me | Record what Marta shipped; Marta reruns the replay through the deployed path and exports it | |
| Fri afternoon | Sam | Checklist, decision log, export access | `ops/operator_review_checklist.md`, `ops/decision_log_template.csv` |
| Mon evening | Client, via Priya | Confirm or withdraw at reduced scope, against the criteria | |
| Tue evening | Client, via Priya, only if needed | Withdraw if the 20-card set fails | |
| Wed 13:00 | Client editors | Training, with Priya | |
| Thu 10 Sep 12:00 | Everyone | Instruction and configuration freeze | |
| Fri 11 Sep 17:00 to 23:00 | Everyone | Runbook | `ops/event_runbook.md` |

**What I do personally.** The reconciliation and every document in this pack. The 15:00 update. Marta's list tonight. The decision note for Friday. Two supervised sessions with Sam, Monday and Tuesday. The 20-card labelled set on Tuesday. The Thursday freeze. On the night, 17:00 to 23:00: second approver, reconciler and escalation point while Sam is on, then either reconciler and escalation point beside a second approver, or sole approver in single-approver mode. The post-event reconciliation and review the following week.

**What I ask of others.** Marta: items 1 and 2, export access for Sam, a view on the 15-second timeout, a rerun of the replay through the deployed path, and, if Product agrees, deploying the revised instructions, which need a validator and ranking change because the card format changes. Sam: use the checklist, log every decision with a reason code and the card's generation time, escalate rather than diagnose. Lewis: the six decisions in the note. Priya: send the update, find out which cards the client received, align Wednesday's training, name who is reachable on the night. Amira: agree the allowance and the trigger with Lewis.

**My other two client workstreams.** Their Friday 11 September items move to Thursday or the following Monday. Both clients are told on Monday 7 September. No backfill is assumed.

## 4. Practical demonstration

The step I took as far as I could: make the evidence reproducible and the instructions testable outside production.

```bash
# 1. Join sources, log and queue; write the fact table and findings
python3 -I checks/reconcile.py data outputs
# 2. Compute every number quoted in the documents
python3 -I checks/numbers.py data outputs
# 3. Check both against expected values read from the files
python3 -I checks/test_reconcile.py
# 4. Generic event check: duplicates, lost items, dwell, on any export in the pilot schema
python3 -I checks/event_checks.py data/01_source_content.json data/06_trial_run_log.csv data/02_trial_recommendations.json
# 5. Run current and revised instructions over the ten items, and over my four test cases
python3 -I prompts/run_prompts.py data/01_source_content.json outputs/prompt_runs --model sonnet
python3 -I prompts/run_prompts.py data_extra/candidate_test_cases.json outputs/prompt_runs_candidate_cases --model sonnet
# 6. Build the before-and-after comparison with an automatic claim check
python3 -I prompts/compare_runs.py data/01_source_content.json data/02_trial_recommendations.json outputs/prompt_runs outputs/prompt_before_after.md
```

Steps 1 to 4 need only Python. Step 5 needs either a logged-in Claude Code CLI or an Anthropic API key (`--backend api --model <exact model id>`). Every saved run records the exact model id and time, and pins the scenario clock in the message so timeliness is judged against 3 September 2026 rather than the date the test is run. The runs used here are committed in `outputs/`, so the result can be read without running anything.

**What it shows.**
- `reconcile.py` derives the duplicate, the lost item, the rejected item, the latency pattern and the cost pattern from the raw files, quoting the rows. Its findings text is written for this pack. `event_checks.py` is the generic version with no prose: it flags duplicates by source and by operation, lost items, and dwell, and exits non-zero if anything is flagged, so it can gate a 15-minute check on the night.
- The automatic claim check flags both faulty pilot cards. On the promotion card it also flagged "before Game 3" against the source's "before Friday". I first overruled that as a fair paraphrase. It was not: the item was published on Thursday 3 September, so "before Friday" means the next day, and the card had moved a deadline by a week. The check was right and my overrule was wrong; I have left that in the log because it is the point of the check.
- With the scenario clock pinned, the current instructions still rejected the tipoff change as routine, exactly as the pilot did, and gave the Mensah record low priority. On my own test cases they also dropped a closed-entrance notice as "operational". The revised instructions produced a correct Mensah card, rejected the sponsor competition, classified the tipoff change and the entrance closure as high-priority changes, kept "questionable", "ruled out" and "sources say", put the highlights video and the coach statement in the held lane, and returned a list of claims for the approver instead of a confidence score.

**What it does not show.** The current instructions on today's model also get many things right, including Mensah's wording. So the pilot's errors are partly model and pipeline behaviour, and this test shows the revised instructions are better specified; it does not show that production will behave the same. Only Marta's rerun through the deployed path shows that, which is why it is acceptance criterion 2. Outputs also vary between runs, which is why each saved run records its model id and time, and why earlier runs are kept: `outputs/prompt_runs_v1` (revised only, before model ids were recorded) and `outputs/prompt_runs_v2_unpinned` (both variants, before the scenario clock was pinned, where the model judged timeliness against November 2026).

**What still needs human judgment.** Whether a highlights video is ever a separate card. Whether promotions belong in the feed. How an unconfirmed report should look. Every approval. The story key the revised instruction emits is a hint for the approver: the two Game 2 cards received different keys, and the official Cole update and the CourtsideWire report received the same one. Deduplication stays with engineering, on source and operation IDs.

**Completed.** Reconciliation, number checks, tests, generic event check, revised instructions tested on ten pack items and four of my own, operator checklist, decision log, Marta's list, Lewis's decision note, Amira's cost note, runbook, plan, client update.

**Unresolved, and what each changes.** Nothing has run through the production pipeline, so Monday depends on Marta's rerun. The production model is unknown, so the instruction gains are unproven there. The live-lane share and Sam's rate are indicative, so Monday's session decides whether one approver is enough. The 2 September queue is unreconciled, so the duplicate scale is a hypothesis. Which cards the client saw is unknown, so the duplicate's cause is a strong hypothesis. No labelled set exists yet, so Tuesday is a real checkpoint.

## 5. First update to the client

In `ops/client_update_thursday_1500.md`: a short internal note to Priya and the message she can send to Jordan. The message confirms both faults, gives the duplicate's cause as most likely rather than certain, volunteers the two items that never reached the queue, commits only to a Monday position, keeps CourtsideWire open, and asks which cards the client received. It offers no changed service, because Lewis has not decided.

## 6. How I used AI and how I checked it

Full chronological log in `ai_log/ai_use_log.md`, with the representative prompt and output.

**My tool of choice was Claude Code.** It read the pack alongside me, wrote the scripts and tests, drafted the revised instructions, and produced the first draft of every document here. I read the pack myself, set the questions, and required each finding to be proven from the data rather than from the AI's reading. I had every number computed by a script because language models misread numbers. I had the pack scanned for hidden text. I commissioned three separate AI review sessions with no access to our conclusions: a cold adversarial read of the pack, a simulated hiring panel on the first full draft, and a second adversary and panel on the finished version. I decided what to accept, change and reject from each. The recommendation, the lanes, the single-approver mode and the CourtsideWire position are my decisions.

- **Checked.** Every finding cites a row. The tests assert values read from the files before the script existed, so the script is checked against the files rather than against itself. Every figure in prose comes from `checks/numbers.py`. The reviews found, across three rounds: a remit violation in the client update, an impossible Monday gate, unobservable stop conditions, a capacity figure that did not match the lanes in the checklist and the instruction, a prompt harness that judged timeliness against the real date, a finding labelled proven where the pack conflicts, and a paraphrase I had wrongly accepted. All are addressed in this version and listed in the log.
- **Changed.** The client update, twice: first so it precedes Lewis's decision, then so it states the duplicate's cause as likely rather than certain and mentions the two silent losses. The Monday gate. The stop conditions, including what "pause" means without an engineer. The lane definitions, made identical across the checklist, the instruction and the numbers. The capacity arithmetic, moved from my per-card model to Sam's stated rate. The prompt harness, to record model ids and pin the scenario clock.
- **Rejected.** The AI's first framing of the duplicate as a prompt problem; the log shows a retry fault. A reviewer's hypothesis that the client's complaint referred to earlier output, which the pack contradicts; I had accepted it before the next review caught it. The AI's capacity model of 50 cards an hour. One reviewer's view that the ten-minute dwell stop condition is too loose; kept, because the target is a request rather than a measured service level, and a stop that fires on one slow card would pause the feed constantly.
- **Limitations.** The prompt test proves instructions, not production. Outputs vary between runs. The story key is not a deduplication key. The AI wrote 8x where the figure is 5x and 45 percent where it is 44, listed a pack fact as an assumption, overruled a correct automatic flag, and shipped a placeholder in an earlier draft of the log. Each was caught by a script or a review round, which is the argument for running them.

## 7. Time, assumptions, and what I left unfinished

**Time spent.** About three and a half hours of my own focused time across two sittings on 1 and 2 November 2026. Claude Code sessions ran for roughly four and a half hours of wall-clock time over the two days, including unattended prompt runs and the review sessions.

**Assumptions.** Sam's 30 to 40 cards an hour holds with the checklist. Cost per call is a flat average because the CSV has no token counts. Priya sends client messages. The Claude Code CLI with claude-sonnet-5-5 stands in for whichever model production uses. Four of nine sample items as the live-lane share. The venue is UTC+1, inferred from one pair of times.

**Open questions, and what proceeds anyway.** Which cards the client received (Marta's fixes proceed). Whether a second approver exists (single-approver mode is defined). The production model (Friday's rerun answers it). Sam's rate with the checklist (Monday measures it). Whether retries are billed (inferred from flat cost per call; Amira can confirm from the invoice).

**Deliberately unfinished.** Reconciliation of the full 2 September queue, which the pack does not contain. A labelled set beyond ten pack items and four of my own. A CourtsideWire evaluation beyond the outline above. A dashboard.
