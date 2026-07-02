# MVP Limitations, Risks, and Next Steps

## Verified scope

- The silent-zone component can produce village-level rule-based silent-risk output for Hualien County.
- It supports LINE reporting, `pending → verified/rejected` review, verified incidents, and trust metadata.
- It can output JSON, CSV, and GeoJSON.
- The volunteer component can create deterministic dispatch suggestions from skills, distance, urgency, and availability.
- The parent repository’s offline sample demo validates task transformation, candidate ranking, and duplicate-assignment prevention.
- `IntegratedTask` JSON Schema and a target OpenAPI contract are included.

## Claims that must not be exaggerated

| Area | Actual limitation |
|---|---|
| Disaster prediction | Silent risk is not a probability of disaster; the NN experiment has no real ground truth. |
| Real time | External APIs, network, and pipeline duration affect availability. |
| Hydrology | Water Resources Agency water-level integration is incomplete. |
| Road impact | Current road impact is largely rule-feature based. |
| LINE production use | Requires public HTTPS, LINE Developers configuration, and operational management. |
| `refresh=true` | Synchronous and blocking; not safe for untrusted public callers. |
| Volunteer persistence | Event/registration state is in memory and disappears on restart. |
| End-to-end integration | Parent demo does not call live child-service HTTP APIs; adapter/facade is not implemented. |
| External authorization | Volunteer service needs production-grade authorization/management hardening. |
| Roster quality | Outdated locations, skills, or availability reduce recommendation quality. |

## Priority next steps

### P0 — safety and honesty

1. Make every UI/response display live/sample/batch/trust status.
2. Implement the adapter with schema validation and complete conversion/dispatch audit logs.
3. Move volunteer state to durable storage with administrator controls.
4. Put both services behind HTTPS/reverse proxy and protect refresh/admin routes.
5. Implement privacy notice, retention, withdrawal, and deletion workflows.

### P1 — reliability and deployment

1. Use protected scheduled/background jobs instead of public synchronous refresh.
2. Add Docker, lockfiles, health checks, and CI.
3. Add source retry, degradation, and alerting.
4. Version volunteer skills, locations, and availability.
5. Build task-management and review interfaces.

### P2 — data and research quality

1. Integrate more hydrology, road, communications, and field-inspection data.
2. Build genuine labels from historical incidents and field confirmations.
3. Validate/calibrate models and monitor bias.
4. Test ranking stability across places, hazards, and population contexts.
5. Version the task-type and skill ontology.

## Non-negotiable boundaries

Without ground truth and field evaluation, do not claim predictive accuracy. Without source trust and human review, do not turn data into orders. Without an adapter and audit trail, do not claim automatic end-to-end integration. Without security and privacy controls, do not operate large-scale personnel dispatch.
