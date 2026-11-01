# Current Workflow and Prompt

## Product flow

Approved feed -> source item -> AI relevance decision -> AI recommendation -> operator queue -> operator approval -> client recommendation feed -> editor decides what to publish.

The pilot polls approved feeds every five minutes. New items are stored with a source content ID and URL. A relevance step decides which items should proceed. A second AI step creates the recommendation.

The ranking logic combines recency, model confidence and recognised player or team names. Operators can approve, edit, hold or reject cards. Approval is required before a card reaches the client.

The operator view shows the generated card and source links. It does not currently show items that never reached the queue. There is no routine comparison of the source feed with the recommendation queue.

## What is available

Delivery can export source items and recommendations, edit a draft prompt for testing, and prepare temporary checks outside the production service. Engineering controls live processing and can provide selected run logs.

The attached log is an extract from an exported replay of the supplied approved source items. The older Game 2 articles were intentionally included. The unapproved external item was excluded from this run.

The service uses a 15-second timeout and allows up to three retries after the first request. The log shows selected classification, generation and queue events. We do not have full provider telemetry in this exercise.

There is no agreed evaluation set or launch acceptance criterion. Operators have been reviewing selected output, but their decisions have not been captured consistently.

## AI instructions

The relevance step is currently given this instruction:

```text
You are a basketball editor selecting content opportunities for a professional league's fans.

Decide whether the supplied item is worth surfacing to an editor. Consider timeliness, audience interest and connection to the Finals. Give priority to major player news, performances, results and records. Routine notices and promotional items are usually lower priority.

Return relevant (true or false), category and a short reason.
```

Items selected as relevant proceed to this recommendation instruction:

```text
Create a useful editorial recommendation from the supplied content.

Return category, priority (high, medium or low), a headline, a summary of no more than 35 words, source URL, why fans will care, and confidence from 0 to 1.

Keep the headline engaging and the summary factual. Use only the supplied item. Do not invent facts. If the information is uncertain, preserve that uncertainty.
```

Both steps receive the content ID, title, body, source name, publication time and URL. The classification decision is recorded in the processing log. Recommendations contain references to their input source IDs.

No accuracy measurement has been established for the model confidence field. The attached recommendation output is what the workflow actually produced in this trial, including any departures from these instructions.
