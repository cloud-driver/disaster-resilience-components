# AI Governance, Human Review, and Accountability

## Why governance matters

This is disaster decision support. A bad ranking can divert attention; a poor allocation can create skill mismatch, duplicate deployment, or safety risks. Governance therefore belongs in the system design.

## Operating principles

| Principle | Implementation expectation |
|---|---|
| Explainability | Show score factors, data modes, source status, dispatch score breakdowns, and warnings. |
| Human in the loop | Humans review reports, create tasks, and approve actual dispatch. |
| Least privilege | Separate ordinary queries, report management, pipeline execution, and webhooks with appropriate credentials. |
| Traceability | Keep run IDs, timestamps, source status, review decisions, conversions, and dispatch responses. |
| Uncertainty disclosure | Make sample/batch/unverified/stale/source-failure states visible. |
| Data minimization | Keep only needed dispatch data; hash LINE identifiers and set retention/deletion rules. |
| Safe failure | External/AI/map failures must produce visible warnings, not false success. |

## Required human gates

```text
Public report → human verify/reject
Risk or incident queue → human task definition
Dispatch recommendation → human coordination decision
```

Human intervention is mandatory for non-live or stale data, source failures, pending reports, unassigned tasks, incomplete skill coverage, unusual ETA, trapped/medical/high-risk tasks, or AI text that conflicts with deterministic data.

## Prohibited automation

- Declaring a disaster from a score.
- Using unreviewed reports in formal ranking.
- Sending coercive rescue/evacuation orders automatically.
- Determining road closure, evacuation, shutdown, or life-safety status through model output.
- Publishing personal locations, LINE identities, or sensitive reports to unauthorized users.

## Minimum audit record

```text
request_id / task_id / incident_id
silent-zone run_id
data_mode / freshness / source_status
priority-to-urgency mapping version
volunteer-roster version and availability time
dispatch response / warnings / unassigned tasks
reviewer, timestamp, decision, and rationale
```

## Deployment governance

Use HTTPS, a reverse proxy, segregated secrets, input validation, rate limiting, dependency/security scanning, administrator permissions, retention/deletion processes, and de-identified/consented data for public demonstrations.
