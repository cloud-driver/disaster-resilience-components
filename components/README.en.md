<p align="right">
<a href="./README.md">繁體中文</a> | English
</p>

# Component Snapshot Guide

This folder keeps local **review snapshots** of two disaster-resilience components so that reviewers can inspect core code, sample data, and documentation after cloning only the parent repository. These are not submodules and do not update automatically. When a snapshot conflicts with upstream code, the current upstream repository and Swagger documentation are authoritative.

| Local snapshot | Upstream implementation | Component role | Current fact to retain |
|---|---|---|---|
| [`silent-disaster-zone-api/`](./silent-disaster-zone-api/) | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | Identifies high-risk, low-observation, low-reporting areas; includes LINE reporting, human review, verified incidents, and command support. | Formal ranking is explainable and rule-based; AI is restricted to summaries. |
| [`disaster-rescuing/`](./disaster-rescuing/) | [D4rk-N355/volunteer_distributing](https://github.com/D4rk-N355/volunteer_distributing) | Produces volunteer candidates and dispatch suggestions from tasks, skills, distance, and availability. | The local folder keeps a legacy name; the active upstream repository is `volunteer_distributing`. |

## Review rules

1. **Upstream is the source of truth.**Snapshots are for offline review; check the upstream README, Swagger, and source code for current endpoints, environment variables, and security behavior.
2. **Documentation is not evidence of deployment.**The parent repository’s `examples/integration_demo.py` is a fixture-based offline verification, not an API-to-API integration test.
3. **Preserve current contract differences.**`IntegratedTask` is the parent repository’s normalized exchange format. The current volunteer service accepts `DispatchRequest`; an adapter is required.
4. **Do not commit sensitive data.**Never include `.env`, tokens, API keys, LINE identifiers, raw reports, or personal data.

Suggested order: silent-zone README → volunteer README → parent API contract → integration demo → `IntegratedTask` schema.
