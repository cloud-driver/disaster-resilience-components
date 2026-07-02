<p align="right">
<a href="./README.md">繁體中文</a> | English
</p>

# Making Silent Areas Visible: Silent Disaster Zone Detection × Volunteer Dispatch Components

> Move from “respond only where people report” to “identify high-risk, low-observation, low-reporting areas and turn them into reviewable human tasks.”

This repository is the integration and submission entry point for the Disaster Resilience Components competition. It is **not** a replacement for an emergency command platform. It documents two independently reusable API components, their data contract, an offline integration demo, and operational boundaries.

## Review in this order

| Order | Component / document | Purpose |
|---|---|---|
| 1 | [Silent Disaster Zone Detection API](https://github.com/cloud-driver/silent-disaster-zone-api) | Ranks Hualien village-level areas that merit proactive human confirmation; includes LINE public reporting, human review, verified incidents, and data-trust metadata. |
| 2 | [Disaster Volunteer Dispatcher API](https://github.com/D4rk-N355/volunteer_distributing) | Produces reviewable volunteer candidates from task urgency, skills, location, and availability. |
| 3 | [`examples/integration_demo.py`](./examples/integration_demo.py) | Validates the data transformation chain from risk result to normalized task to volunteer recommendation using bundled sample data. |

> **Current-state boundary:** `integration_demo.py` is an offline, fixture-based data integration demo. It does not call either child service over HTTP and is not evidence of a production cross-service deployment. A production connector requires the adapter described in [API & data contract](./docs/api_contract.en.md).

## Problem and response

During disasters, systems typically see places that already have reports. Yet areas affected by communications loss, blocked roads, sparse sensing, higher ageing ratios, or low digital reporting capacity may have little or no signal.

This project does not declare that a disaster has occurred, and it does not predict where one will occur. It creates a **human review priority**:

```text
Static risk + real-time event signals + observation gap + verified-report activity
                                  ↓
                 silent-risk ranking for proactive confirmation
                                  ↓
                      normalized IntegratedTask
                                  ↓
       volunteer candidate matching by skills / distance / availability
                                  ↓
                    accountable human review and dispatch
```

## Component design

| Component | Input | Process | Output | Independent use? |
|---|---|---|---|---|
| Silent-zone detection | village boundaries, static risk, sensor/event signals, verified reports | rule-based risk and silence scoring; separates silent-watch and verified-incident queues | JSON, CSV, GeoJSON, metadata, priority candidates | Yes |
| Task transformation contract | risk result | describes field-check/support tasks, location, priority, and skills in `IntegratedTask` | JSON Schema / OpenAPI contract | Yes |
| Volunteer dispatch | tasks, work types, volunteer skills/location/availability | deterministic matching, distance and urgency weighting, optional AI anomaly check | candidates, ETA, score breakdown, unassigned tasks, warnings | Yes |

## Runnable integration demo

```bash
python3 examples/integration_demo.py
```

On Windows:

```powershell
python examples\integration_demo.py
```

The demo reads `examples/sample_silent_zone_output.json` and `examples/sample_volunteers.json`, then writes `examples/sample_dispatch_output.json`. It validates task transformation, candidate ranking, duplicate-assignment prevention, and human-review warnings.

## Documentation

| Document | Focus |
|---|---|
| [Quick start](./docs/quickstart.en.md) | Run the offline demo and start each child component separately. |
| [Story and scenario](./docs/story.en.md) | Personas, the information gap, and system boundaries. |
| [Architecture](./docs/architecture.en.md) | Component boundaries, data ownership, and current vs. target integration. |
| [Diagrams](./docs/diagrams.en.md) | Data flow, two queues, and deployment boundary. |
| [API & data contract](./docs/api_contract.en.md) | Actual child APIs, `IntegratedTask`, and adapter requirements. |
| [Data sources](./docs/data_sources.en.md) | Static, live, report, and volunteer data with quality disclosure. |
| [AI usage](./docs/ai_usage.en.md) | Where AI may and may not be used. |
| [AI governance](./docs/ai_governance.en.md) | Human review, safety, accountability, and auditability. |
| [Limitations](./docs/limitations.en.md) | MVP limitations and next steps. |
| [Submission checklist](./SUBMISSION_CHECKLIST.en.md) | Final competition and demo checks. |

## Local snapshots and source repositories

| Item | Local snapshot | Source repository | Note |
|---|---|---|---|
| Silent-zone component | [`components/silent-disaster-zone-api/`](./components/silent-disaster-zone-api/) | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | Snapshot supports offline review; upstream repository is the implementation source of truth. |
| Volunteer-dispatch component | [`components/disaster-rescuing/`](./components/disaster-rescuing/) | [D4rk-N355/volunteer_distributing](https://github.com/D4rk-N355/volunteer_distributing) | The local folder keeps the legacy name `disaster-rescuing`; the active upstream repository is `volunteer_distributing`. |

## Safety statement

- `silent_risk_score` means a priority for proactive human confirmation, **not** a disaster declaration.
- A `pending` public report must not affect the formal ranking until it is human-reviewed as `verified`.
- Dispatch output is a candidate recommendation, not an automatic dispatch order.
- AI may not issue evacuation, road-closure, emergency-status, or life-safety decisions.
- Production use needs explicit consent, data retention, HTTPS, access control, and audit measures.

See the root `LICENSE` for licensing. Do not commit secrets, API keys, LINE identifiers, raw public reports, or other personal data.
