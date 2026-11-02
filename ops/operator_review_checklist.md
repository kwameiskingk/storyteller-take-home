# Operator review checklist (Sam, and whoever covers after 18:30 UTC)

Purpose: approve only cards an editor can trust without re-verifying, in under a minute each. Log every decision.

## Before the session
1. Open the queue, the source export and the decision log side by side. If you do not have the source export, stop and tell the Delivery Lead. Do not review from the card alone.
2. Sort by priority, then by published time (newest first).

## For every card (target 45 to 60 seconds)
1. **Open the source link.** Read the title and the first two sentences.
2. **Same story?** Look at the `story_key` and the source. If a card for the same event is already approved:
   - Same facts, same media: reject, reason `DUP`.
   - Different media (article vs video): hold, reason `DUP`, note "media variant". Product is deciding whether highlights videos become separate cards. Until then they wait.
   - Same story key but a different claim (for example an official update and an unconfirmed report): these are not duplicates. Review each on its own.
3. **Numbers and records.** Every number in the card must appear in the source. Every record or stat claim must use the source's own scope (franchise, team, league) and verb (ties, breaks). If anything is upgraded or missing: edit to match the source, reason `FACT`.
4. **Conditions and uncertainty.** "Questionable", "expected", "sources say", entry conditions and "terms apply" must survive into the card. If dropped: edit, reason `COND`.
5. **Times.** A time with no zone gets "local" added only if the source says local. Otherwise leave and flag `TIME`.
6. **Promotions.** Sponsor competitions and commercial offers: hold, reason `PROMO`, until Product confirms the editorial policy. Do not approve.
7. **Priority and lane.** Live lane, high: a result (the article or official statement), a player availability update from the team or league, a change to tipoff, doors, venue or travel, an official record or statistic. Held lane, medium: coach or team statements with no decision, previews and analysis, routine fan information such as the fan zone programme, and a video or highlights package of a result already reported. If the card disagrees, change it, reason `PRIO`. In single-approver mode (after 18:30 unless a second approver is confirmed) only results, availability and schedule or venue changes are live; records are held.
8. Decide: approve, edit then approve, hold, reject. Write the row in the decision log before moving on, including the card's `generated_at` time so queue dwell can be measured.

## Escalate immediately (message the Delivery Lead, do not wait)
- The same source produces two cards within a few minutes (possible retry duplicate).
- A card makes a claim the source does not contain.
- A card refers to an item you cannot find in the source export.
- You suspect an important item is missing from the queue (for example a result or injury update you saw on the official feed).
- The queue grows faster than you can clear it for 15 minutes.

## Reason codes
`DUP` repeat, `FACT` unsupported or upgraded fact, `COND` dropped condition or uncertainty, `TIME` time or zone issue, `PROMO` promotional policy pending, `PRIO` priority changed, `OK` approved unchanged, `OTHER` free text required.
