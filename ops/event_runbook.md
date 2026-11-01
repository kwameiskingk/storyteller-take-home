# Game 3 event runbook, Friday 11 September 2026 (all times UTC, venue local = UTC+1)

| Time | Who | What |
|---|---|---|
| 16:15 | Delivery Lead | Confirm feed polling, queue empty of stale cards, decision log open, Priya and Lewis reachable. Confirm the prompt has not changed since Thursday freeze. |
| 16:30 | Delivery Lead | Cover begins (doors and fan zone open 16:30 UTC, before the planned window). |
| 16:45 | Delivery Lead + Sam | 15-minute pre-game check: run checklist on whatever is in the queue, agree the story keys already covered. |
| 17:00 to 18:30 | Sam (reviewer), Delivery Lead (second reviewer and escalation) | Review per checklist. Delivery Lead runs the reconciliation export every 15 minutes and watches retry counts. |
| 18:30 | Sam hands over | Sam leaves. Delivery Lead is the sole reviewer from here. Volume must already be cut to what one person clears in 10 minutes. |
| 19:00 | Tipoff | High-priority lane only (results, availability, schedule and venue changes, official records). Medium lane held unless the queue is empty. |
| ~21:00 | Final result | Expect the peak: result, highlights, reactions. Approve the result card first, mark the story key, reject repeats. |
| 21:00 to 23:00 | Delivery Lead | Post-game. Continue reconciliation. At 22:45 export decision log and reconciliation output. |
| 23:00 | Delivery Lead | Close. Message Priya with counts: cards received, approved, edited, rejected, missed items found by reconciliation, any client-facing error. |

## Stop conditions (pause the client feed, tell Priya to inform the editors to use manual monitoring)
- A card with a factual error reached the client.
- Queue dwell above 10 minutes for 30 consecutive minutes.
- No reviewer online.
- Retries per initial call above 0.25 for 30 minutes, or AI spend above EUR 25 in any hour (Finance trigger).

## Pre-written message if we stop (Priya sends)
"We have paused the recommendation feed for the rest of tonight because [reason]. Your editors should continue with the usual monitoring of official feeds. Nothing already approved needs to be withdrawn [or: please disregard card X]. I will send a full account tomorrow morning."

## Not covered
No engineering cover is booked. The existing incident route applies only to product failures. If processing stops, the feed stops and the stop condition "no reviewer" is replaced by "no feed": same client message.
