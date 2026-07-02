# Submission and Demo Checklist

Use this checklist to keep documentation aligned with the code that can actually be verified. Do not add unsupported claims merely to make the project look more complete.

## Documentation consistency

- [ ] The current volunteer-dispatch source repository is `https://github.com/D4rk-N355/volunteer_distributing`.
- [ ] References to `components/disaster-rescuing/` explain that it is a legacy local snapshot folder name.
- [ ] The offline fixture demo in this repository is clearly distinguished from a future production API-to-API adapter.
- [ ] `openapi/integrated-flow-api.yaml` is described as a target integration contract/facade, not a deployed endpoint.
- [ ] Current Swagger and source code in each child repository take precedence over older snapshot documentation.

## MVP and feasibility

- [ ] `python3 examples/integration_demo.py` runs and writes `examples/sample_dispatch_output.json`.
- [ ] The demo shows risk input, task conversion, volunteer candidates, duplicate-assignment prevention, and warnings.
- [ ] Sample data is described as data-flow validation only, never as live incident data.
- [ ] The silent-zone MVP scope is Hualien County at village level.
- [ ] The volunteer service’s event and registration state is currently in memory and disappears after restart.

## Safety, privacy, and governance

- [ ] Do not claim disaster prediction, automatic rescue, or guaranteed response.
- [ ] `silent_risk_score` is documented as a human-confirmation priority, not a disaster declaration.
- [ ] Silent-zone AI only summarizes existing rule-based results and cannot change rankings or issue orders.
- [ ] Volunteer-dispatch AI is optional anomaly checking and cannot replace deterministic dispatch.
- [ ] Human coordinators retain final authority for any dispatch.
- [ ] No secrets, tokens, raw LINE identifiers, or raw public reports are committed.
