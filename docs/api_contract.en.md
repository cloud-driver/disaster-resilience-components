# API and Data Exchange Contract

## Core conclusion

`IntegratedTask` is a **normalized intermediary format** for describing a task generated from a silent-zone result. It is not the current volunteer service’s direct request body.

| Component | Key interface | Current security state |
|---|---|---|
| Silent-zone API | `/silent-risk`, `/reports/*`, `/incidents/verified`, `/advisor/command` | Most endpoints require a short-lived Bearer token; privileged operations also require `REPORT_ADMIN_KEY`. |
| Volunteer dispatcher | `/api/v1/dispatch`, `/api/v1/dispatch/start`, `/api/v1/dispatch/finish`, forms, LINE webhook | Core dispatch exists; production use still needs hardening for external authorization and persistence. |
| Parent repository | `integrated_task.schema.json`, `integrated-flow-api.yaml` | Contracts only; `/integrated-flow/dispatch-recommendations` is not deployed. |

## `IntegratedTask`

Schema: [`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json).

It includes task ID, source component, administrative area, risk context, task type/priority/description, location, and required skills.

## Adapter mapping

| `IntegratedTask` | Dispatcher `DispatchRequest` | Rule |
|---|---|---|
| `task_id` | `tasks[].id` | Direct. |
| `task.task_type` | `tasks[].type_id` | Map to a work type. |
| `task.priority` | `tasks[].urgency` | Explicit configurable mapping, e.g. low=2, medium=3, high=4, urgent=5. |
| `location` | `tasks[].location` | Direct. |
| `required_skills` | `work_types[].required_skills` | Create or merge by work type. |
| task description | `tasks[].job_description` | Preserve human-review and data-status notes. |
| area/risk context | audit metadata / description | Preserve, because it is not a mandatory dispatcher field. |
| volunteer roster | `volunteers[]` | Use authorized, current volunteer data only. |
| incident context | `metadata` | Set incident ID and weighting mode. |

Do not POST `IntegratedTask[]` directly to `/api/v1/dispatch`.

## Minimum validation pipeline

1. Read silent-zone results with `meta`.
2. Flag/reject `sample`, `unverified`, stale, or source-failed data for operational use.
3. Validate every transformed task against the JSON Schema.
4. Build a `DispatchRequest` and call the volunteer service.
5. Persist request, response, `run_id`, mapping version, warnings, and operator.
6. Require human coordinator confirmation before contact or real dispatch.

## Target OpenAPI facade

[`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml) specifies a target:

```text
POST /integrated-flow/dispatch-recommendations
```

It is a future facade contract, **not a currently implemented endpoint**. Its example volunteer schema is also different from the current upstream dispatcher’s model, so an implementation must normalize or explicitly map it.
