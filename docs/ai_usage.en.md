# AI Usage

## Principle: AI may summarize and flag; it does not take over disaster decisions

The project uses AI in two constrained locations:

| Component | AI role | Core logic remains | AI may not |
|---|---|---|---|
| Silent-zone API | Ollama summarizes existing queues and reasons. | Explainable `rule_based_mvp` risk scoring. | Change rankings, add/remove villages, declare incidents, or issue evacuation/road orders. |
| Volunteer dispatcher | Optional Ollama anomaly check. | Deterministic matching by skills, distance, urgency, and availability. | Replace matching, hide warnings, or decide real dispatch. |

## Silent-zone AI

Allowed: summarize existing queue fields and explain existing risk reasons.

Not allowed: treat `pending` reports as verified, alter score/level/queue, claim that an incident occurred, or execute operational commands. The rule-based command plan must remain available if Ollama is unavailable.

## Volunteer-dispatch AI

Allowed: flag unusual allocations and prompt coordinators to examine skill gaps, unreasonable distances, long ETA, or high-urgency unassigned tasks.

Not allowed: invent volunteer attributes, remove `warnings` or `unassigned_tasks`, or send dispatch orders without human approval.

## Experimental ML layer

The silent-zone project may retain `silent_risk_nn_score` and training scripts as a replaceable-layer experiment. Current pseudo-labels are not real disaster ground truth. Therefore, do not claim predictive accuracy and do not replace `rule_based_mvp` ranking. Any future model requires genuine labels, validation, calibration, bias checks, versioning, and human-factors evaluation.

## Correct presentation language

Correct: “AI summarizes existing rule-based results and highlights anomalies; humans retain final responsibility.”

Incorrect: “AI predicts disasters, verifies incidents, automatically dispatches volunteers, or rescues people.”
