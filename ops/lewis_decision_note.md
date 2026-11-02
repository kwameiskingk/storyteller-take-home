# Decision note for Lewis (and Priya), Friday 4 September, 10:00 UTC

One page. What I recommend, what I need you to decide, and what happens under each alternative. Evidence is in `outputs/findings.md`; numbers in `outputs/numbers.json`.

## Recommendation
Launch for Game 3 at reduced scope, confirm or withdraw to the client on Monday 7 September, with stop conditions on the night. Not full scope, not a withdrawal.

Reduced scope: four card types in a live lane (results, player availability, schedule or venue changes, official records and statistics), official league and team feeds plus the approved broadcaster, every card operator-approved, client manual monitoring kept running, no promotional cards, no CourtsideWire.

## Why not full scope
In the ten-item replay: one duplicate from a retry bug, one fabricated record claim at 0.94 confidence, the player availability update lost silently, the tipoff change rejected as routine, a sponsor competition ranked high. Forecast volume is 240 cards in six hours with peaks of 80 an hour; the operator reviews 30 to 40 an hour and leaves at 18:30 UTC, before tipoff.

## Why not withdraw
Causes are specific. Two are bounded engineering changes that Marta can size for Friday (her list, items 1 and 2). The rest are instructions and process I control. The client keeps its manual process as the safety net, so a reduced launch risks little and proves the service in the window you care about.

## Decisions I need from you
| # | Decision | My recommendation | If you decide otherwise |
|---|---|---|---|
| 1 | Scope and date: reduced scope for Game 3, confirmed to the client Monday 7 Sep, with Priya | Agree | Full scope: I cannot stand behind the error rate or the review capacity. Withdraw: client runs manual, we target the next game and lose the Finals proof. |
| 2 | Acceptance criteria for Monday's confirmation (none exist today) | Adopt the four conditions below as the pilot's first acceptance criteria | Without criteria, Monday's call is opinion. |
| 3 | Promotional content and highlights policy | Promotional items held, not shown, until you set policy. Highlights video is a separate card only when it adds media the result card lacks, and is labelled as video. | If promotions are in scope, they go to the medium lane at the lowest priority with a sponsor label. |
| 4 | Confidence score and ranking | Replace the model confidence field with an operator checklist on the card. Ranking then uses recency and category priority only. | Keeping confidence keeps an unmeasured number in the ranking; the 0.94 fabricated card ranked above correct ones. |
| 5 | Second approver after 18:30 UTC, and who is reachable for the client on the night | Ask: can anyone on Product or the account team approve cards from 18:30 to 23:00? And can Priya, or someone she names, be reachable to message the editors if we pause? I reconcile and escalate; the second person approves. | If no second approver: from 18:30 the feed runs in single-approver mode, live lane limited to results, availability and schedule or venue changes (about 27 cards in the peak hour, 40 to 53 minutes of review at Sam's rate); records and everything else are held. The result peak around 21:00 is where this bites. |
| 6 | Event allowance (with Amira) | EUR 100 for the window, with a pause if duplicate cards appear or, if Marta's export carries attempt counts, retries per call exceed 0.25 over 30 minutes | A lower allowance needs a smaller window or fewer sources. |

## Acceptance criteria for Monday (proposed)
1. Marta's items 1 and 2 deployed by 13:00 Friday. If only item 1 ships, see below.
2. Ten-item replay rerun by Marta through the deployed pipeline: one card for src_001, a card or visible failure for src_003.
3. Sam has source export access and one logged session with the checklist on Monday.
4. No fabricated fact in Monday's logged session.
5. Either a second approver is confirmed for 18:30 to 23:00, or we agree single-approver mode after 18:30 and Priya tells the client that records and context cards will arrive after the game.

Tuesday's 20-card labelled set is a second checkpoint; if it shows a fabricated fact or more than one duplicate, we withdraw and tell the client Tuesday evening, still before Wednesday's training.

## What changes my recommendation
- To full scope: a clean 20-card set and Monday's logged session showing the slow-review share well under my 20 percent assumption.
- To withdraw: Marta ships item 1 only (validation failures would still silently lose availability updates, the category the client cares most about), or the client will not keep manual monitoring, or Monday's session shows Sam under 30 cards an hour with the checklist, or Monday's measured live-lane share is well above the 44 percent sample figure with no second approver.

## What I am doing while you decide
Marta has her list (decision-independent). Sam's checklist and decision log are ready. The revised instructions are tested on the ten items outside production. The client update went at 15:00 yesterday and commits only to Monday.
