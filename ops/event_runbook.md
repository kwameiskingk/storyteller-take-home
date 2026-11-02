# Game 3 event runbook, Friday 11 September 2026 (all times UTC, venue local = UTC+1)

| Time | Who | What |
|---|---|---|
| 17:00 | Delivery Lead | Cover begins, as agreed in the capacity plan. Confirm feed polling, queue state, decision log open, Priya and Lewis reachable, prompt unchanged since Thursday freeze. Note: the fan zone and doors open at 17:30 venue time, which is 16:30 UTC if the venue is UTC+1 as the pack implies; cards about them will be in the queue when cover starts, so they are reviewed first. |
| 17:00 to 17:15 | Delivery Lead + Sam | Pre-game check inside Sam's agreed window: run the checklist on the queue, agree the story keys already covered. |
| 17:15 to 18:30 | Sam (approver), Delivery Lead (second approver, reconciliation every 15 minutes, escalation) | Review per checklist. |
| 18:30 | Sam hands over | Sam leaves. From here the Delivery Lead is the only approver unless Lewis and Priya have found a second (decision note, item 5). Live lane is high priority only. |
| 19:00 | Tipoff | High-priority lane only (results, availability, schedule and venue changes, official records). Medium lane held unless the queue is empty. |
| ~21:00 | Final result | Expect the peak: result, highlights, reactions. Approve the result card first, mark the story key, reject repeats. |
| 21:00 to 23:00 | Delivery Lead | Post-game. Continue reconciliation. At 22:45 export decision log and reconciliation output. |
| 23:00 | Delivery Lead | Close. Message Priya with counts: cards received, approved, edited, rejected, missed items found by reconciliation, any client-facing error. |

## Stop conditions (pause the client feed, tell Priya to inform the editors to use manual monitoring)
Each one names how it is observed, because there is no live telemetry and no engineer on duty.
- A card with a factual error reached the client. Observed by: client report, or the approver finding an error in a card already approved.
- Cards are waiting more than 10 minutes before approval for 30 consecutive minutes. Observed by: the decision log timestamps against card generated_at.
- No approver online. Observed by: the approver.
- Two duplicate cards from the same source in the queue, or, if Marta's 15-minute export ships, retries per initial call above 0.25 over 30 minutes. Observed by: the queue, or the reconciliation script on the export. This is the cost trigger agreed with Finance; spend itself cannot be seen live.

## Pre-written message if we stop (Priya sends)
"We have paused the recommendation feed for the rest of tonight because [reason]. Your editors should continue with the usual monitoring of official feeds. Nothing already approved needs to be withdrawn [or: please disregard card X]. I will send a full account tomorrow morning."

## Not covered
No engineering cover is booked. The existing incident route applies only to product failures. If processing stops, the feed stops and the stop condition "no reviewer" is replaced by "no feed": same client message.
