# Aurora Basketball League content service: Game 3 delivery recommendation

Take-home submission for the Delivery Lead, AI-Enabled Products role at Storyteller.
Candidate: Kwame [surname]. Scenario clock: Thursday 3 September 2026, 12:00 UTC.

This README is the main document. The folders hold the working material it refers to.

| Folder | What is in it |
|---|---|
| `data/` | The evidence pack, unchanged |
| `checks/` | `reconcile.py`, the reconciliation script, and `test_reconcile.py`, hand-derived tests |
| `prompts/` | Current and revised AI instructions, the runner that tests them live, the comparison builder |
| `ops/` | Operator checklist, decision log, Marta's Friday list, event runbook, plan and RACI |
| `outputs/` | Generated results: fact table, findings, prompt before and after, raw prompt runs |
| `ai_log/` | How AI was used, what was changed, rejected and checked |

## 1. Recommendation

**Launch for Game 3 at reduced scope, with a decision gate on Monday 7 September and stop conditions on the night.** Not a full go, and not a no-go.

Reduced scope means:
- Four card types only: results, player availability, schedule or venue changes, and official records or statistics. Previews, statements and fan information sit in a medium lane that is released only when the queue is clear.
- Official league and team feeds plus the approved broadcaster. No CourtsideWire for Game 3.
- The client's manual monitoring continues as the system of record. The feed is an aid, not a replacement, for this one event.
- Two reviewers on the night: Sam until 18:30 UTC, then me alone until 23:00. Volume must fit what one person clears in ten minutes.
- No promotional cards until Product sets the policy.

Why not a full go: the pilot produced duplicates from a retry bug, fabricated a record claim at 0.94 confidence, silently lost the most important item of the day (a player availability update) and threw away a tipoff time change. Review capacity cannot meet forecast volume. None of those are fixed yet.

Why not a no-go: the causes are known and specific. Two of them are small engineering changes that fit in Marta's four hours. The rest are instruction and process changes I can make and test myself. The client keeps a safety net. The Finals are the one chance to prove the service in the window Product cares about.

### Conditions that must be true before we confirm to the client on Monday 7 September
1. Marta has deployed the idempotent queue write (no card from a superseded request) and a retry or visible failure for validation errors.
2. A rerun of the ten-item replay through the deployed pipeline shows one card for src_001 and a card or visible failure for src_003.
3. Sam has source export access and has run two logged review sessions with the checklist.
4. A 20-card labelled set from Monday and Tuesday output (my labels, marked as such) shows no fabricated fact and at most one duplicate.

If any of these fail, we tell the client on Monday that Game 3 runs on manual monitoring, and we target the next game.

### Stop conditions on the night
A factual error reaches the client. Queue dwell exceeds ten minutes for 30 minutes. No reviewer is online. Retries per call exceed 0.25 for 30 minutes or AI spend exceeds EUR 25 in an hour. Any one of these pauses the feed and Priya sends the pre-written message in `ops/event_runbook.md`.

### What would change my recommendation
- To full go: a reconciled 2 September queue showing duplicates confined to the retry storm, plus a clean 20-card run after Friday's deploy, plus Lewis agreeing that medium-lane cards can be released.
- To no-go: Marta's window is lost or only item 1 ships, or the client is unwilling to keep manual monitoring running, or Monday's logged sessions show the slow-review share is far above my 20 percent assumption.
- On CourtsideWire: a four-week offline comparison showing it is earlier and not wrong more often than official feeds would make me propose it as a labelled "unconfirmed report" lane, with Lewis designing the treatment.

## 2. Evidence

Everything below is reproduced by `checks/reconcile.py` and written to `outputs/findings.md`, with the rows quoted. The fact table of what happened to each of the ten source items is in `outputs/fact_table.csv`.

| Finding | Status | Where it comes from |
|---|---|---|
| Duplicate: the timed-out request completed anyway and both responses were written to the queue | proven | log rows for gen_001, attempts 1 and 2 |
| Mensah card upgraded a tied franchise record to a broken league record, two errors, confidence 0.94 | proven | rec_004 vs src_005 |
| Elias Cole availability update lost on a validation failure, never retried, invisible to the operator | proven | log row gen_003 |
| Tipoff change classified "routine", no card | proven | log row cls_004 |
| Sponsor giveaway ranked high as player news, insurance-quote condition dropped | proven | rec_005 vs src_006 |
| Generation latency 7 to 21 seconds against a 15-second timeout | proven | log timestamps |
| 2 September cost: retries per call 0.04, 0.05, then 1.74, cost per call flat, so retries are billed | proven | cost CSV |
| Event cost projection EUR 32 to 84 of AI spend for the six-hour window | estimate | cost CSV, Product's volume estimate |
| 240 cards need about 288 review minutes, a peak hour needs 96 from one person with 60 | arithmetic on an assumption | capacity document, 20 percent slow share assumed |
| Sam leaves 30 minutes before tipoff, so the Delivery Lead is the second operator | proven | capacity document |
| CourtsideWire was 22 minutes earlier, anonymous, and said "miss" where the team said "questionable" | proven | src_010 vs src_003 |
| The client saw drafts marked "before operator review" | proven, cause unknown | README of the pack |

Two things the data does not prove, stated as hypotheses: that the 2 September queue holds hundreds of duplicates from the retry storm, and that the client's complaint refers to earlier pilot output rather than this replay (Jordan wrote 16 minutes after the replay finished). Both are questions in the client update.

## 3. Taking the work forward

The day-by-day plan, the deadlines pulled from each message, and the RACI are in `ops/plan_and_raci.md`. In short:

**What I do personally.** Reconcile the evidence (done, this pack). Send Priya the client update by 15:00 today. Send Marta a ranked, evidence-backed list tonight so she starts at 09:00 without waiting for the 10:00 product decision; every item on it is right under go, reduced scope or no-go (`ops/marta_friday_list.md`). Give Lewis the recommendation and the four decisions he owns by 10:00 Friday. Give Amira the cost analysis and a proposed EUR 100 event allowance with a stop trigger. Write and test the revised instructions (`prompts/`). Build Sam's checklist and decision log and run the first two sessions with Sam. Build the 20-card labelled set. Freeze on Thursday. Cover 16:30 to 23:00 UTC on the night. Run the post-event reconciliation and review the following week.

**What I ask of others.** Marta: items 1 and 2 on her list, export access for Sam, a view on timeout settings, and deploying the revised prompts through the replay path if Product agrees. Sam: use the checklist, log every decision, measure time per card, escalate rather than diagnose. Lewis: agree reduced scope and the Monday gate with Priya, decide the promotional policy and the highlights-as-separate-card rule, approve the prompt change. Priya: send the client update, confirm which cards the client received, align the Wednesday training with reduced scope, hold the fallback message. Amira: agree the allowance and the trigger with Lewis.

**My other two workstreams.** I move my own commitments to cover Friday evening. I do not assume backfill. Preparation work for this account fits in half days because the heavy lifting (reconciliation, prompt tests, checklist) is already done here.

## 4. Practical demonstration

The important next step I took as far as I could: **make the evidence reproducible and make the instructions testable outside production**, because every later decision depends on both.

To repeat with a fresh copy of the pack:

```bash
# 1. Reconcile sources, log and queue. Writes outputs/fact_table.csv and outputs/findings.md.
python3 -I checks/reconcile.py data outputs

# 2. Check the script against hand-counted expectations.
python3 -I checks/test_reconcile.py

# 3. Run current and revised instructions over all ten items, live, through the Claude Code CLI.
python3 -I prompts/run_prompts.py data/01_source_content.json outputs/prompt_runs --model sonnet

# 4. Build the before-and-after comparison with an automatic claim check.
python3 -I prompts/compare_runs.py data/01_source_content.json data/02_trial_recommendations.json outputs/prompt_runs outputs/prompt_before_after.md
```

Step 3 needs a logged-in Claude Code CLI. If you do not have one, the raw outputs it produced are committed in `outputs/prompt_runs/` and the comparison in `outputs/prompt_before_after.md`.

What the demonstration shows:
- The reconciliation finds the duplicate, the lost item, the rejected item, the latency and the cost pattern from the raw files, with no manual reading.
- The automatic claim check flags rec_004 and rec_005 in the pilot output. It also flagged "before Game 3" versus "before Friday" on rec_005, which a human correctly overrules. That is the kind of check that narrows what Sam must read, not one that replaces Sam.
- The revised instructions, run today, produce a correct Mensah card ("ties Waves franchise playoff assists record"), reject the sponsor giveaway as promotional, classify the tipoff change as a high-priority schedule change, keep "questionable" and "sources say", and return an `operator_checks` list instead of a confidence score.

What still needs human judgment: whether a highlights video is a second card, whether promotions ever belong in the feed, what to do with an unconfirmed report, and every approval. The `story_key` the revised prompt emits is a hint for the reviewer, not a reliable deduplication key (the two Game 2 cards produced "game 2 result kings waves" and "game 2 result metro kings"). Deduplication by source and operation ID belongs in engineering.

What is completed: reconciliation, tests, revised instructions tested on ten items, checklist, decision log, Marta's list, runbook, plan, client update, cost analysis.
What remains unresolved: nothing has been run through the production pipeline, the production model is unknown, the slow-review share is assumed, the 2 September queue has not been reconciled, and no labelled set exists yet. Each of those has an owner and a day in the plan.

## 5. First update to the client

For Priya to send to Jordan Reed by 15:00 UTC, Thursday 3 September. Plain paragraphs, no promises we cannot keep.

Hi Jordan,

Thank you for the detail on the Game 2 duplicate and the Mensah claim. Both are real and we have found the causes.

The duplicate came from our processing, not from the content. A request timed out, we retried it, and then both the original and the retry were accepted. We are fixing that tomorrow so a single source item can only ever produce one card.

The Mensah card was wrong twice. Your stats team is right that it was a Waves record, not a league record, and the source also says he tied it rather than broke it. The system has been told to use the source's exact wording for any record or statistic, and our reviewer will check every number against the source before you see a card.

We also found two items that should have reached you and did not: the Elias Cole medical update and the tipoff time change. We are correcting the handling of both.

On Game 3, our honest position is that the service can support your editors at a reduced scope, and we would like to confirm that with you on Monday once tomorrow's fixes are in and tested. Reduced scope means results, player availability, schedule and venue changes and official statistics, from official sources only, with every card reviewed before you see it. We would ask you to keep your normal monitoring running on the night as well, so nothing depends on us alone. If Monday's testing is not clean, we will say so and Game 3 runs on your usual process.

On CourtsideWire, you are right that they were ahead on the Cole story. Their report also differed from the team's official update, so we want to evaluate them properly rather than add them before the Finals. We will come back with a view after Game 3.

Two questions to help us: which cards did your team receive in the sample, and would your editors want a highlights video surfaced separately when the result has already been covered?

Best,
Priya

## 6. How I used AI and how I checked it

Full chronological log in `ai_log/ai_use_log.md`, including the representative prompts and outputs. Summary:

- **Claude Code did the heavy lifting**: reading the pack, writing the reconciliation script, the tests, the prompts, the runner and first drafts of every document in `ops/`. I directed, questioned, reviewed and decided.
- **Checked by construction.** Every finding points at a row in the files. The tests encode hand-counted expectations written before the script ran. Cost arithmetic is shown next to the figures it came from.
- **Checked by an adversary.** A second AI session read the pack cold, with none of our conclusions, and produced its own findings. It agreed with every finding we had and added eleven more, the most important being that Sam leaves before tipoff and that engineering starts before the product decision. Those are now in the plan.
- **Changed.** The first revised prompt put "(zone not stated)" into headlines, which read badly. I moved that to `operator_checks` and re-ran. The first claim check flagged "before Game 3" versus "before Friday" as an error; I kept the flag and documented it as a false positive a reviewer overrules rather than tuning it away.
- **Rejected.** The AI's first instinct, and the obvious one, is that duplicates are a prompt problem. The log disproves it. The fix went to Marta's list, not to the prompt.
- **Limitations found.** Running the current prompt on today's model mostly got things right, so the pilot's errors are partly model-dependent and my prompt test proves the instructions, not the production system. The `story_key` is not a reliable deduplication key. Nothing here has touched the production pipeline.

## 7. Time, assumptions, and what I left unfinished

**Time spent:** approximately [X] hours over [Sunday 1 November and Monday 2 November]. The pack says three to four; I spent more because the demonstration is runnable and tested.

**Assumptions:** 20 percent of cards need slow review; EUR per call is a flat average because the CSV has no token counts; venue local time is UTC+1; Priya sends client messages; the Claude Code CLI stands in for whichever model production uses.

**Deliberately unfinished:** reconciliation of the full 2 September queue (no data); a labelled evaluation set beyond my own ten-item labels (needs Monday and Tuesday output); a CourtsideWire evaluation design; a styled client-facing summary; a dashboard. Each would be a good next step and none changes the recommendation.
