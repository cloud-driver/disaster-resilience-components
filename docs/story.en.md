# Problem Story and Usage Scenario

## Silence at the start of a disaster is not safety

Emergency operations often see locations where reports were successfully sent. But no report can result from communications loss, blocked roads, sparse sensing, ageing populations, low digital access, or an incident that is still evolving.

The project therefore asks:

> With limited verification capacity, which high-risk and low-information areas should be checked first?

It does not declare that a disaster occurred and does not predict where a disaster will occur.

## Main actors

| Actor | Constraint | Support |
|---|---|---|
| Residents in silent areas | May be unable to call or report. | More likely to appear in a human-confirmation priority list. |
| Local emergency staff | Must prioritize with fragmented information. | Explainable silent-risk scores and data status. |
| Community / village responders | May not know where information blind spots are. | Village-level candidates for proactive confirmation. |
| Volunteer coordinators | Face crowding, mismatch, and duplicate deployment. | Structured tasks, candidates, and warnings. |
| Witnesses | Reports can be incomplete or unreliable. | Reports enter `pending` and require human review. |

## From signal to action

```text
Risk/event data and reports
  ↓
Silent-zone component: risk, observation gaps, verified-report activity
  ↓
A. silent_watch_queue: proactively confirm high-risk, low-information areas
B. verified_incident_queue: evaluate locations with credible known incidents
  ↓
Human task creation
  ↓
IntegratedTask
  ↓
Volunteer matching by skills, distance, availability, urgency
  ↓
Human coordination and final action
```

## What the system does and does not do

| It does | It does not |
|---|---|
| Rank areas for human confirmation. | Declare a disaster. |
| Separate verified incidents from silent-zone prioritization. | Let unverified reports change formal ranking. |
| Provide candidate volunteers, ETA, score breakdown, and warnings. | Issue automatic, irreversible dispatch orders. |
| Use AI for constrained summaries / optional anomaly checks. | Let AI decide evacuation, road closure, or life-safety actions. |

The two components remain independently reusable, which is central to the building-block design.
