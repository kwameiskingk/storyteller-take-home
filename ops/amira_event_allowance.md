# For Amira: what 2 September cost, and a proposed Game 3 allowance

Figures computed by `checks/numbers.py` from `05_cost_summary.csv`.

## What happened on 2 September
| | 1 Sep | 2 Sep | change |
|---|---|---|---|
| Source items | 1,180 | 1,205 | +2% |
| Initial model calls | 1,360 | 1,390 | +2% |
| Retry calls | 63 | 2,412 | 38x |
| Retries per initial call | 0.05 | 1.74 | |
| EUR per call | 0.018 | 0.017 | flat |
| Infrastructure EUR | 4.10 | 6.20 | +51% |
| Total EUR | 29.70 | 71.80 | 2.4x forecast |

Volume did not change. Retries did. Cost per call stayed flat, so retries are billed at full price. At least 804 of 1,390 operations retried at least once. Engineering has seen provider timeouts; the replay log shows the service declaring a timeout at 15 seconds and then accepting the late response as well, which also produced the duplicate the client saw. The infrastructure rise is consistent with extra queue writes but the CSV cannot prove that.

## Game 3 window (Product estimate: 1,500 items, 240 recommendations, 6 hours)
| Scenario | Model calls | AI cost |
|---|---|---|
| Normal retry rate (0.04) | about 1,820 | about EUR 32 |
| 2 September retry rate (1.74) | about 4,760 | about EUR 84 |

Infrastructure is extra; pilot days ran EUR 4 to 6, so a six-hour window at up to five times the hourly volume is likely a few euros. The CSV has no token counts, so per-call cost is an average and these are planning figures.

## Proposal
- Allowance: EUR 100 for the six-hour window. Covers the bad-day scenario with margin.
- Trigger: we cannot see spend live. What we can see, if Marta's 15-minute export ships with attempt numbers, is retries per operation and duplicate cards. Pause if retries per initial call exceed 0.25 over any 30 minutes, or if two duplicate cards appear. Without the export, the only observable signal is duplicate cards in the queue, and that becomes the trigger. "Pause" means approvers stop approving and the editors are told to rely on manual monitoring; Delivery cannot stop processing itself, so AI calls may continue until Engineering is reached through the incident route.
- Overspend: if the pause fires, the client is told to continue manual monitoring and the feed stays off for the night. Spend stops with it.
- The real fix for cost is Marta's item 1 (discard late responses) and a review of the 15-second timeout, which cut retries at source.
