# Service Expectations and Available Capacity

## What the client needs

Two client editors will use the feed during the Finals to decide what to cover on the app and website. They want relevant opportunities with trustworthy summaries and accessible source references. They do not expect every source item to become a card.

During the event, they want important developments surfaced within about ten minutes of appearing in an approved source. This is their requested target, not a measured or contractually agreed service level. A match result, player availability update or change affecting attending fans can matter even when it is not highly engaging content.

The client currently monitors official feeds manually. That process will remain available during the pilot and can cover the event if the new service is not ready. It consumes editor time and they hope to reduce that effort. They do not want to replace it with an equally demanding verification queue.

The account lead has presented Game 3 as the intended first event supported by the service. The client has scheduled training for Wednesday 9 September at 13:00 UTC. No commitment has been made to add CourtsideWire, publish automatically or replace all existing editorial monitoring.

## Pilot observations

The following figures are indicative and come from limited observation:

- Around 1,100 to 1,200 source items arrive per day.
- The queue currently receives around 180 recommendations per day, including repeats and items an editor may not want.
- Sam reviews about 30 to 40 recommendations in a one-hour session, usually starting with high-priority cards. Only selected approved cards have been shared with the client.
- A straightforward review takes roughly 45 to 60 seconds. Comparing multiple sources or checking a questionable claim can take two to three minutes.
- There is no measured end-to-end delay, missed-item rate or reliable record of operator corrections.
- A lack of negative feedback on approved cards does not tell us what was missed or left unreviewed.

## Event planning estimate

The current planning window is Friday 11 September, 17:00 to 23:00 UTC, with tipoff at 19:00 UTC.

Product estimates around 1,500 source items and 240 generated recommendations across that six-hour window, with possible peaks of 80 recommendations in an hour. This is a planning estimate, not a load-test result. Adding CourtsideWire is not included in these figures.

## People and access

- You are responsible for this delivery alongside two existing client workstreams. You can reserve about half of each preparation day and can be available for the six-hour event window by arranging your working day accordingly. Existing client commitments still need a plan; no additional hours or backfill are assumed.
- Sam has one hour each weekday during preparation. On event day, Sam can cover 17:00 to 18:30 UTC. This replaces that day's usual hour. Sam can review recommendations using clear instructions, record decisions and flag concerns, but cannot diagnose model or infrastructure failures independently.
- Marta has four hours on Friday 4 September, 09:00 to 13:00 UTC. There is no dedicated Engineering cover booked for the event. The existing incident route remains available for urgent product failures, but is not a reserved capacity for this pilot.
- Lewis can decide on product priorities and agree launch scope with Priya. Extra staffing, broader coverage or extra budget requires agreement.
- Priya owns the account relationship and can coordinate client expectations and training. You own the delivery recommendation and follow-through.

Sam normally sees only the recommendation queue. Delivery can request the available exports and access needed for a temporary process. Nothing in the exercise assumes that Sam already has those permissions.

## Cost reporting definitions

In `05_cost_summary.csv`, each row covers 00:00 to 23:59:59 UTC on a completed day.

- `source_items`: distinct approved items entering the pilot that day.
- `initial_model_calls`: first classification and generation calls. Not all classified items proceed to generation.
- `retry_model_calls`: additional calls after an initial attempt. These are included in `total_model_calls`.
- `total_model_calls`: initial calls plus retry calls.
- `ai_cost_eur`: billed AI processing, including billable retry attempts.
- `infrastructure_cost_eur`: other pilot processing and queue costs.
- `total_cost_eur`: AI plus infrastructure cost.
- `forecast_cost_eur`: the original pilot budget estimate. It is not an enforced cap.

Call counts alone do not establish cost per useful recommendation: token lengths and completed outputs are not included in this billing extract. The daily data may support a hypothesis, but it does not prove the cause of every increase or the cost of the event.
