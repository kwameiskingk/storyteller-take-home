# Candidate Evidence Pack

Start with `00_TASK_BRIEF.md`. The remaining files describe one fictional delivery situation.

## The client and product

The Aurora Basketball League is a professional basketball competition. Its Championship Finals are tied 1-1 between the Harbour City Waves and the Metro Kings. Game 3 takes place at Harbour Arena on Friday 11 September 2026.

Storyteller is piloting a content opportunity service for the league's digital editorial team. It collects articles, official updates and descriptions of video assets from league, team and approved broadcast-partner feeds. AI selects potentially useful developments and produces recommendations for editors.

A recommendation contains a priority, category, suggested headline, short factual summary, source links and a reason for surfacing it. There is also a model-generated confidence score. The trial JSON shows the current output format.

The intended client experience is a reviewed recommendation feed that helps editors decide what to cover on the league's app and website. A human operator must approve a recommendation before the client can see it. Client editors then make the final publishing decision. The service does not automatically create or publish finished Stories.

Editors want useful coverage of results, player availability, schedule changes and other developments that matter to fans. Distinct angles and supporting media can be valuable, but repetitive cards should not crowd out new information. Promotional opportunities may be relevant; the precise editorial policy has not yet been agreed.

## Current point in the exercise

It is Thursday 3 September 2026 at 12:00 UTC. The event is eight calendar days away. All message, log and data times use UTC. Tipoff is 19:00 UTC on 11 September, which is 20:00 local time at the venue.

The feed polls every five minutes. The pilot is still being sampled internally, and the client has only received selected examples. Broader access has not been enabled.

## Files

- `01_source_content.json`: a small, selected input snapshot available at 09:15 UTC on 3 September. It includes older content replayed for a trial and one external item supplied for evaluating a proposed new source.
- `02_trial_recommendations.json`: the resulting recommendation queue from the replay. These are draft outputs before operator review. The client was sent a selection from this trial for feedback.
- `03_recent_messages.md`: client and internal messages received before the exercise starts.
- `04_current_workflow_and_prompt.md`: a short description of the current workflow and its AI instruction.
- `05_cost_summary.csv`: three complete days of pilot costs and usage.
- `06_trial_run_log.csv`: selected processing events from the replay, including items that did not produce a recommendation.
- `07_service_expectations_and_capacity.md`: the client's planned use, indicative volumes, available people and current operating arrangements.

The ten-item replay is a small diagnostic sample. It is not a representative quality evaluation or a load test. The cost summary describes full pilot days, not this replay.

## Using the evidence

All organisations, people and content are fictional. The URLs are identifiers using `example.com`; they are not working articles or media assets. Use the supplied titles, bodies and metadata as the source evidence. No external sports knowledge or internet research is needed.

The external CourtsideWire item is included for comparison. It was not enabled in the pilot ingestion configuration.

We have provided a partial operating snapshot rather than complete production access. Where evidence is insufficient, distinguish your observations from your hypotheses. You can create additional test cases, provided you label them as your own.
