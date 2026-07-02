# Data Sources, Modes, and Trust

## Data must be traceable, not merely abundant

Risk ranking is only decision support. Each output needs to show its source, generation time, failures, and whether it is live, batch, sample, or unverified.

## Silent-zone data categories

| Category | Examples | Use | Caution |
|---|---|---|---|
| Spatial base | village boundaries | Spatial aggregation | Track administrative-boundary versions. |
| Static risk | flood/landslide potential, population/age features | Static risk score and explanations | Static data is not live incident evidence. |
| Live signals | rainfall, alerts, road/event feeds | Live event/sensor features | Source failure/latency must be exposed. |
| Observation gaps | coverage/observability data | Sensor-gap score | A gap means uncertainty, not proof of harm. |
| Reports | LINE, manual, API | Verified reports build features/incidents | `pending` never enters formal ranking. |
| Volunteer data | skills, location, availability | Dispatch matching | Personal data; minimize and govern it. |

## `data_mode`

| Mode | Meaning | Allowed use | Prohibited claim |
|---|---|---|---|
| `live` | A same-run live pipeline completed. | Current human-review support. | Not an official disaster declaration. |
| `batch` | Batch output. | Analysis, retrospective review. | Not real time. |
| `sample` | Bundled fixture. | Demo/UI/schema validation. | Not current or real incident data. |
| `unverified` | Output exists without a trusted manifest. | Manual inspection first. | Not operational decision input. |

Also inspect `generated_at`, `generated_age_seconds`, `freshness`, `source_status`, `has_source_issues`, `run_id`, `scoring_mode`, and `model_status`.

## Report lifecycle

```text
LINE / Manual / API
        ↓
     pending
     ├── verified → 6h/24h features + verified_incident_queue
     └── rejected → review record, excluded from formal analysis
```

LINE user IDs should be HMAC-hashed; unnecessary identifiers, full addresses, and sensitive data should not be retained.

## Volunteer-data governance

Collect only what dispatch needs: skills, availability, enough location data for distance estimates, and a minimal notification identifier when justified. Production use needs consent/notice, retention and deletion policies, access logging, database protection, and a minimal-retention rule for original addresses.
