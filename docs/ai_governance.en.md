<p align="right">
<a href="./ai_governance.md">繁體中文</a> | English
</p>

# AI Governance and Usage Boundaries

This project may use AI to support analysis and dispatch recommendations. However, AI must not replace emergency commanders, local authorities, or field responders.

## AI Role in the System

| Stage | AI / Algorithm Role | Can It Make Final Decisions? |
|---|---|---|
| Silent disaster zone detection | Help summarize risk factors and generate explanations | No |
| Task transformation | Convert high-risk areas into field-check or rescue tasks | No |
| Volunteer dispatch | Recommend volunteers based on skills, distance, availability, and task needs | No |
| Result explanation | Generate readable dispatch reasons and notes | No |

## What AI Must Not Do

AI must not:

1. Declare disaster severity levels.
2. Issue evacuation orders.
3. Directly dispatch volunteers or rescue workers.
4. Determine individual life-safety status.
5. Replace field command or local government decisions.

## Risks and Mitigation

| Risk | Description | Mitigation |
|---|---|---|
| Data delay | Real-time data may not be updated | Show data timestamps |
| Missing data | Disaster reports may be incomplete | Keep human review |
| AI hallucination | AI may generate unsupported reasons or suggestions | Ground key outputs in rules and data fields |
| Wrong dispatch | Volunteer skills or locations may be inaccurate | Require coordinator confirmation |
| Overreliance | Users may treat suggestions as commands | Clearly label outputs as decision support |

## Fallback Mechanism

If AI service is unavailable, the system should fall back to rule-based logic:

1. Sort by silent risk score.
2. Sort by task priority.
3. Sort by skill match.
4. Sort by distance and availability.
5. Generate a candidate list instead of direct dispatch.

## Human Review Principle

All dispatch recommendations should be reviewed by responsible personnel.  
Human review is required when:

1. The recommended volunteer lacks required skills.
2. The task risk level is `critical`.
3. Source data is outdated.
4. Candidate volunteers are too far away.
5. No candidate fully satisfies the task requirements.
