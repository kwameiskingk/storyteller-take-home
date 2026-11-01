# For Marta: evidence and priorities for Friday 4 September, 09:00 to 13:00 UTC

Sent Thursday evening so you can start at 09:00. Everything here is right whether Product decides go, reduced scope or no-go, so nothing waits on the 10:00 decision. Evidence rows are in `outputs/findings.md`; the raw log is `data/06_trial_run_log.csv`.

## 1. Do not write a queue card from a request already marked timed out (highest harm, smallest change)
Evidence: `gen_001` attempt 1 timed out at 09:15:17, retry started 09:15:18, then attempt 1 **completed at 09:15:23 and wrote rec_001**, and attempt 2 wrote rec_003 at 09:15:29. Same operation_id, two cards. Proposed: treat operation_id (or source_content_id plus run) as the idempotency key at queue write; discard any response for an attempt already superseded. Acceptance: replay the ten items, expect one card for src_001.

## 2. Retry, or at least surface, validation failures
Evidence: `gen_003` returned without the summary field at 09:15:20 and was never retried, so the Elias Cole availability update never reached the operator. Proposed: one retry on `validation_failed`; if it fails again, write a placeholder card marked "generation failed, operator please read source" rather than dropping silently. Acceptance: replay, expect a card or a visible failure for src_003.

## 3. Dropped-item visibility for the operator
Evidence: 04 says the operator view cannot show items that never reached the queue and there is no source-to-queue comparison. Proposed, cheapest version: a scheduled export (every 15 minutes during the event) of approved source items with their classification result and generate outcome, which Delivery reconciles with `checks/reconcile.py`. No UI work.

## 4. Export access for Sam
Sam reviews without the source export or logs. Read access to the source export is needed for the checklist to work. Please confirm what access is possible without new infrastructure.

## 5. Timeout and retry settings (discuss, do not change blind)
Evidence: generation latencies in the replay are 7, 10, 11, 11, 11, 12, 14, 15 and 21 seconds against a 15-second timeout. On 2 September retries per initial call went from 0.04 to 1.74 and the day cost 2.4x forecast with the same volume. A longer timeout with a single retry, or a cap on concurrent retries, would cut both cost and duplicates, but I do not know the provider's tail latency. Your call on what is safe.

## 6. Deploy the revised prompts if Product agrees (after 10:00)
Revised relevance and generation instructions are in `prompts/`, tested outside production on the ten items with before-and-after output in `outputs/prompt_before_after.md`. I cannot prove they behave the same in the production pipeline or on the production model. If you can run them through the replay path, that is the test that counts.

## Not asking for
Ingestion redesign, monitoring, CourtsideWire, event-day cover. If anything above does not fit in four hours, items 1 and 2 are the ones that matter for Game 3.
