# Plan: Thursday 3 September 12:00 UTC to the week after Game 3

Scenario clock: it is Thursday 3 September, 12:00 UTC. The Delivery Lead has about half of each preparation day for this account and two other client workstreams. No extra people, hours, access or budget are assumed.

## Deadlines received
| When (UTC) | Who | What they need |
|---|---|---|
| Thu 3 Sep 15:00 | Priya | Substantive update for the client |
| Thu 3 Sep evening | Marta | Evidence and priorities before her 09:00 start |
| Fri 4 Sep 10:00 | Lewis | Launch position, scope change, decisions he must make |
| Fri 4 Sep | Amira | Event allowance and overspend plan, reviewed with Product |
| Fri 4 Sep 09:00 to 13:00 | Marta | Only engineering window before the event |
| Mon 7 Sep | Client via Priya | Final go / reduced / no-go, so Wednesday training and the manual fallback can be planned |
| Wed 9 Sep 13:00 | Client | Editor training |
| Fri 11 Sep 17:00 to 23:00 | Everyone | Event window (doors 16:30 UTC, tipoff 19:00 UTC) |

## Day by day
**Thu 3 Sep, afternoon (this submission is the output).** Reconcile the evidence. Draft the client update for Priya by 15:00. Send Marta the prioritised list. Send Lewis a heads-up that the recommendation will be reduced scope with the decisions he owns. Send Amira the cost analysis and proposed allowance. Ask Priya which cards the client actually received.

**Fri 4 Sep.** 09:00 Marta starts on items 1 and 2. 10:00 recommendation to Lewis, agree scope and the Monday decision date with Priya. Amira and Lewis review the allowance. 13:00 Marta's window closes: record what shipped. Afternoon: rerun the ten-item replay through whatever Marta deployed; label results. Give Sam the checklist and decision log, arrange export access.

**Mon 7 Sep.** Sam's hour: supervised review of the day's queue with the checklist and log, measuring time per card and the slow share (replaces my 20 percent assumption). Delivery Lead: reconciliation of Monday's queue against sources. Decision confirmed to the client via Priya by end of day.

**Tue 8 Sep.** Sam's hour: second logged session. Delivery Lead: build a 20-card labelled set from Monday and Tuesday output (own labels, marked as such). Count duplicates, unsupported claims, missed items. If any fabricated fact or more than one duplicate: trigger the pre-launch kill criterion and tell Lewis and Priya.

**Wed 9 Sep.** 13:00 client training, with Priya. Show the editors the reduced-scope lane, what a card looks like, how to report a bad card. Sam's hour: logged review.

**Thu 10 Sep.** Prompt and configuration freeze by 12:00. Dry run of the runbook with Sam for 30 minutes. Pre-write the stop message. Confirm the other two client workstreams have cover arrangements for Friday afternoon and evening (I move my own commitments, nobody else's).

**Fri 11 Sep.** Runbook.

**Week after.** Monday: reconcile the full event queue, decision log and cost. Tuesday: review with Lewis and Priya, then the client. Decide on CourtsideWire evaluation, promotional policy, confidence field, and whether the second operator need becomes a staffing request. Turn the decision log into the first evaluation set.

## RACI
R = does the work, A = owns the decision, C = consulted, I = informed.

| Task | Delivery Lead | Marta | Sam | Lewis | Priya | Amira |
|---|---|---|---|---|---|---|
| Launch recommendation and evidence | R/A | C | C | I | I | I |
| Change external launch scope or date | R (recommends) | | | A | A | I |
| Idempotent queue write, validation retry | A (priority) | R | | I | | |
| Operator checklist, decision log | R/A | | C | I | | |
| Export access for Sam | R (requests) | A | I | | | |
| Revised prompts (test outside production) | R/A | C | | C | | |
| Deploy prompts to production | R (asks) | R (deploys) | | A | | |
| Promotional policy, highlights-as-card rule | R (proposes) | | C | A | C | |
| Event allowance and stop trigger | R (proposes) | | | A | | A |
| Client update and training | R (drafts) | | | C | A | |
| CourtsideWire evaluation (after Game 3) | R | C | | A | A | |
| Event-day review | R | | R (to 18:30) | I | I | |
