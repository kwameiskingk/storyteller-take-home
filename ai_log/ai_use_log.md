# AI use log

The brief asks how AI was used and how its contribution was checked, with a representative prompt and output, what was changed or rejected, and limitations. Storyteller's role page adds that the review looks at what the candidate accepted, changed, checked and rejected. This log is written to answer both.

**Tools.** Claude Code (Fable 5.1) as the working partner in a terminal session. The Claude Code CLI, resolving to claude-sonnet-5-5, as the stand-in for the pilot's two AI steps. Four further Claude Code sessions as independent reviewers across three rounds, each given only the files and a brief, never our conclusions. No paid API, no live infrastructure, no credentials shared.

**Working method.** My tool of choice was Claude Code. It read the pack alongside me, wrote the scripts and tests, drafted the instructions and the first draft of every document. I read the pack myself, set the questions, and required each finding to be proven from the data rather than from the AI's reading. Every number in prose is computed by a script. Build, then cold review by a separate session that did not build, then fix, then repeat on the finished version. My standing instructions to the AI were: read everything twice, explain the task in plain English before building, prove each claim from data, say where confidence is low, and do not agree in order to please.

## Chronology

**1. Sunday evening: read and explain.** Candidate asked for the pack to be read twice, the job page checked, and the task explained in plain English before any building. Outcome: a plain-language brief, the correct job title (the live page says Delivery Lead, AI-Enabled Products; the application acknowledgement said Implementation Lead (AI)), and eight suspected findings. Check: the candidate read the files and asked for each finding to be proven from the data.

**2. Prove each finding.** Prompt (abridged): "Prove the duplicate, the false record claim, the silently lost item, the dropped schedule change, the promotional card, the cost spike, the capacity gap and the CourtsideWire difference from the data, not from your reading of it." Outcome: `checks/reconcile.py`. The automatic claim check flagged rec_005 for "before Game 3" when the source said "before Friday". At the time I accepted the AI's view that this was a fair paraphrase because Game 3 is on a Friday. The third review round showed that was wrong: the item was published on Thursday 3 September, so "before Friday" means the next day. The check was right and we were not. Corrected everywhere; see item 13.

**3. First independent review, cold read of the pack.** A second session was given the pack only and asked for every problem with proof, a recommendation, the common mistakes a candidate would make, and anything easy to overlook. Outcome: agreement on the eight findings and eleven additions, including that Sam leaves before tipoff, that Marta's window opens before Lewis decides, that the Mensah card has two errors not one, and that latency sits on the timeout. Adopted. Also adopted, wrongly: a hypothesis that the client's complaint referred to earlier pilot output. See item 9.

**4. Prompt test harness.** `prompts/run_prompts.py` to run both instruction sets over the ten items through the CLI. First version had a syntax error. Fixed and rerun.

**5. Finding that changed the argument.** The current instructions on today's model produced a correct Mensah card, rejected the giveaway and surfaced the tipoff change. So the pilot's errors are partly model and pipeline behaviour. The prompt test proves the instructions are better specified, not that production will behave the same. Marta's rerun through the deployed path became acceptance criterion 2. A later full rerun (Monday morning, with model ids recorded) showed the current relevance step rejecting the Mensah record item that it had accepted the day before, and the revised card step giving a coach statement high priority where its rule says medium. Both are recorded in the saved runs: the first as evidence that the current instructions are unstable, the second as a rough edge the checklist's priority step catches.

**6. Prompt revision v2.** v1 put "(zone not stated)" in headlines. Rule 4 rewritten to send that to `operator_checks`; rule 5 to name the teams the source names, after one headline said "beat opponent". v1 outputs kept in `outputs/prompt_runs_v1/`.

**7. Limitation found: story_key.** Meant to help the approver spot repeats. The article and the video of the same result got different keys. The second review then found the official Cole update and the CourtsideWire report got the same key. Useful hint for a human, useless as a machine key, and dangerous if trusted.

**8. Monday morning: candidate's re-review request.** Before any further building, the candidate asked for everything to be re-read, for a second independent review of the finished draft, and said explicitly: no sycophancy, tell me where I am wrong, explain why rather than just doing. The AI's own re-read found five problems. The second review, briefed as a sceptical hiring panel, found those and more.

**9. Second independent review, panel grading of the first full draft.** Scores: demonstration 5/5, recommendation 4/5, plan 4/5, AI log 4/5, client update 2/5, time spent 2/5. Findings accepted and fixed:
- Remit: the client update promised engineering work and offered reduced scope before Lewis's decision. Rewritten.
- Remit: RACI made Delivery accountable for a production change. Corrected to Marta.
- Remit: pre-game check used 15 minutes of Sam outside the agreed window; runbook started at 16:30 against a 17:00 availability. Both corrected.
- Gate: Monday's confirmation depended on Tuesday's labelled set. Rebuilt.
- Stop conditions on spend and retry rate were unobservable. Rebuilt around what can be seen.
- Contradictions: two Sam sessions by Monday (one), "two reviewers on the night" (two for 90 minutes), highlights rule decided in the checklist while pending with Lewis, fan zone time asserted in UTC against our own timezone rule, fan information in the medium lane against the client's stated need.
- Factual: "8x the normal hourly rate" (5.1x). "Timeouts are structural" overstated against two normal days at 4 to 5 percent retries. Infrastructure cost causation stated as proven. UTC+1 listed as a free assumption when the pack implies it from a stated pair of times.
- The earlier-output hypothesis from review 1 contradicted the pack's plain statement that the client was sent a selection from this trial. Removed. This was AI speculation elevated over a source statement, and it is the failure mode the candidate had asked to watch for.
- Missing: a decision note for Lewis, volume arithmetic under reduced scope, the ten-minute latency budget, the second approver as an explicit ask, acceptance criteria offered as such, the ranking consequence of removing the confidence score. All added.
Findings not accepted: the panel suggested "queue dwell over ten minutes for 30 minutes" is too loose because it already breaches the client's target. Kept, because the target is a request not a measured service level, and a stop condition that fires on a single slow card would pause the feed constantly. Noted in the runbook as a judgment.

**10. Candidate's checks.** The candidate asked whether CourtsideWire was being called untrustworthy on one item; it was, and the wording became "unverified, not evaluable in eight days", with a four-week evaluation design. Asked how volume would be managed; the arithmetic was added. Asked for a scan of the pack for hidden text (zero-width characters, bidirectional overrides, HTML, styling, zip comments, unexpected fields): clean. Asked whether using the Claude Code CLI as the test harness was best practice; the honest answer was that an API call with a pinned model id is the usual standard, so the runner was changed to record the exact model id and run time and to accept an API key as an alternative route. Asked that every number in prose be computed by a script because language models misread numbers: `checks/numbers.py`, which also caught 44 percent where the AI had said 45, and showed the AI's capacity model (50 cards an hour) disagreed with Sam's observed 30 to 40; the observed figure was used.

**11. Documents.** Claude Code drafted the ops documents, the README and the HTML brief. I set the structure, chose the design direction from three options, rewrote the AI-use account in my own words, removed anything I could not defend in an interview, and checked every number against `outputs/numbers.json`.

**12. Third round: adversary and panel on the finished version.** Two further sessions, one briefed as an adversarial reviewer and one as a hiring panel, read the finished submission including the HTML brief and reran the scripts. Both confirmed the demonstration runs clean and reproduces the committed outputs, and both said nothing else must be built. Then they found real problems:
- The capacity figure did not match our own files. The checklist put fan-affecting items high, the card instruction put fan information medium, the numbers script excluded it, and the revised instruction had put the highlights video in the live lane. Counted consistently, one approver was over capacity. Fixed by defining the lanes once and applying the definition in the checklist, the instruction (rule 7 tightened), the numbers script, the brief and the README, then rerunning the instruction to confirm the highlights video and the coach statement now land in the held lane.
- The 288-minute and 96-minute figures still used the 50-cards-an-hour model I had said I rejected. Replaced with Sam's stated rate throughout; the per-card model is kept only as a labelled sensitivity.
- The prompt harness never told the model the scenario date, so it judged a 3 September item "about two months old" against the real November date. My claim that the current instructions were unstable on Mensah rested partly on that. Fixed by pinning the scenario clock in every message and rerunning all items; the unpinned runs are kept in `outputs/prompt_runs_v2_unpinned`. With the clock pinned, the current instruction still rejected the tipoff change as routine, which is the pilot's failure reproduced cleanly.
- The earlier claim that an accepted-then-rejected pair was "recorded in the saved runs" was not true for the current variant; v1 kept only the revised runs. Corrected.
- The client update stated the duplicate's cause as fact while asking which cards the client saw. If they saw the recap plus the highlights video, the repetition is editorial. Marta herself said she had not established it. Rewritten as "most likely", and a note to Priya added, since she asked for the update to her.
- Finding 11 was labelled proven, but the pack's capacity document says only approved cards were shared with the client, which conflicts with the README's "before operator review". Relabelled as a pack conflict, with the consequence for the duplicate's cause spelled out.
- "Pause the feed" had no mechanism. Now defined as approvers approving nothing further plus Priya messaging the editors, and the decision log gained the column needed to measure dwell.
- The revised card format drops the confidence field and adds three, which is a validator and ranking change, not a text edit. Marta's list now says so and offers a text-only fallback.
- Sam's pre-game check was shortened to ten minutes inside the agreed window; the runbook and the plan now agree.
- A literal placeholder (this item) had shipped in the previous draft of the log.
Rejected from this round: the panel suggested the brief should not be called client-ready because it carries a candidate byline and an AI section. Agreed in substance, so the brief is described as a delivery brief for the panel, not as a client document. The adversary suggested the reconciliation script is "a report generator, not a reconciler" because its findings prose is written for this pack. Accepted in part: the join is generic and the prose is not, so a generic `checks/event_checks.py` was added for use on an event export, and the README says which is which.

**13. Candidate-authored test cases.** The pack permits extra test cases if labelled. Four were written (`data_extra/candidate_test_cases.json`): a genuine league record, a player ruled out, a closed entrance affecting attending fans, and a sponsored award that contains news. The current instruction dropped the entrance closure as an operational notice, the same class of failure as the tipoff change. The revised instruction made it high and kept "ruled out" and "local time". Both instructions handled the genuine league record correctly, which matters: the revised wording rule does not suppress real records.

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

A representative working prompt from me to Claude Code, Monday morning (abridged): "Double-check everything before we start building. Anything to do with numbers, build and run a Python script to confirm, because language models misinterpret numbers. Search the pack for hidden text. Run the panel review on the finished version. No sycophancy."

## What the AI got wrong or could not do
- Framed the duplicate as a prompt problem before reading the log.
- Adopted a reviewer's speculation over a pack statement.
- Wrote 8x for 5x, 45 percent for 44 percent, and modelled 50 cards an hour against a stated 30 to 40, then kept using the model after saying it was rejected.
- Wrote a client update that pre-empted a decision the brief reserves for Product and the account lead, then a second one that stated an untraced cause as fact.
- Overruled a correct automatic flag ("before Friday") and presented the overrule as good judgment.
- Built a prompt harness that leaked the real date into timeliness judgments, and drew a conclusion from it.
- Left a placeholder in a shipped draft of this log.
- Could not name the production model, access the 2 September queue, or measure the slow-review share. These are labelled assumptions or open questions.
- Its outputs are non-deterministic. Committed runs are one sample. The automatic claim check exists so a rerun can be checked the same way.
