<p align="right">
<a href="./README.md">繁體中文</a> | English
</p>

# Integration Documentation

This folder explains how the parent repository places the Silent Disaster Zone Detection and Volunteer Dispatch components in one reviewable decision-support chain.

## Suggested reading order

1. [Quick start](./quickstart.en.md) — run the offline fixture demo, then optionally start each upstream component.
2. [Story and scenario](./story.en.md) — understand the information gap being addressed.
3. [Architecture](./architecture.en.md) — inspect component boundaries and current integration status.
4. [Diagrams](./diagrams.en.md) — inspect data flow, two queues, and human review points.
5. [API & data contract](./api_contract.en.md) — inspect actual APIs, `IntegratedTask`, and the required adapter.
6. [Data sources](./data_sources.en.md) — inspect data modes, trust metadata, and limitations.
7. [AI usage](./ai_usage.en.md) and [AI governance](./ai_governance.en.md) — inspect AI boundaries.
8. [Limitations](./limitations.en.md) — inspect what the MVP does not yet prove.

## Most important current-state statement

- `examples/integration_demo.py` is an **offline fixture demo** for data transformation and candidate ranking.
- `openapi/integrated-flow-api.yaml` is a **target integration contract**, not a currently deployed endpoint.
- The two child components can run independently, but production integration still requires an adapter that converts `IntegratedTask` into the volunteer service’s `DispatchRequest`.
- Sample, batch, stale, or unverified data must never be presented as live incident information or automated rescue output.

Return to the [repository home](../README.en.md).
