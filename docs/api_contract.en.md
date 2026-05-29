<p align="right">
<a href="./api_contract.md">繁體中文</a> | English
</p>

# API Contract

This document defines the input, output, and data exchange format between the two components. Actual fields should follow each component repository’s OpenAPI / Swagger documentation. This file explains how the two components are connected in the main proposal repository.

## 1. Component A: Silent Disaster Zone Detection API

### 1.1 Purpose

Return village-level silent risk data for maps, dashboards, task generators, or dispatch systems.

### 1.2 Main endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API and output availability |
| GET | `/model/info` | Return metadata for the neural network scoring layer |
| GET | `/silent-risk/top?limit=5` | Return the top N villages with the highest silent risk |
| GET | `/silent-risk/top?limit=5&refresh=true` | Fetch realtime data and recompute risk, for development or demo use |
| GET | `/silent-risk/{village_id}` | Query silent risk for a single village |
| GET | `/silent-risk.geojson` | Return a GeoJSON layer for map display |

### 1.3 Example response: `GET /silent-risk/top`

```json
{
  "status": "success",
  "data": [
    {
      "village_id": "10015020001",
      "county_name": "花蓮縣",
      "town_name": "鳳林鎮",
      "village_name": "鳳仁里",
      "silent_risk_score": 0.392821,
      "silent_risk_level": "medium",
      "silent_reason": "High static risk; sensor coverage gap; no reports in the last 6 and 24 hours",
      "silent_risk_rule_score": 0.41,
      "silent_risk_nn_score": 0.39,
      "static_risk_score": 0.61,
      "sensor_gap_score": 0.61,
      "realtime_event_score": 0.0,
      "report_count_6h": 0,
      "report_count_24h": 0
    }
  ]
}
```

### 1.4 Field description

| Field | Type | Description |
|---|---|---|
| `village_id` | string | Village identifier |
| `county_name` | string | County name |
| `town_name` | string | Township / district name |
| `village_name` | string | Village name |
| `silent_risk_score` | number | Final silent risk score |
| `silent_risk_level` | string | Risk level, such as `low`, `medium`, `high` |
| `silent_reason` | string | Human-readable explanation summary |
| `silent_risk_rule_score` | number | Rule-based baseline score |
| `silent_risk_nn_score` | number | Neural network scoring layer score |
| `static_risk_score` | number | Static risk score |
| `sensor_gap_score` | number | Sensor or observation coverage gap score |
| `realtime_event_score` | number | Realtime event signal score |
| `report_count_6h` | integer | Number of reports in the last 6 hours |
| `report_count_24h` | integer | Number of reports in the last 24 hours |

## 2. Component B: Disaster Volunteer Dispatcher API

### 2.1 Purpose

Receive task and volunteer data and return recommended assignments.

### 2.2 Main endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Basic API status message |
| GET | `/health` | Check API and Ollama service status |
| POST | `/api/v1/dispatch/v1` | Create a dispatch plan |

### 2.3 Request format: `POST /api/v1/dispatch/v1`

```json
{
  "metadata": {
    "incident_id": "mataian-2025-001",
    "priority_weighting": "balanced"
  },
  "work_types": [
    {
      "type_id": "FieldCheck",
      "required_skills": ["FirstAid", "LocalGuide"]
    },
    {
      "type_id": "Logistics",
      "required_skills": ["HeavyLifting"]
    }
  ],
  "volunteers": [
    {
      "id": "vol_01",
      "skills": ["FirstAid", "LocalGuide"],
      "location": {
        "lat": 23.654,
        "lng": 121.432
      },
      "availability": true
    },
    {
      "id": "vol_02",
      "skills": ["HeavyLifting"],
      "location": {
        "lat": 23.660,
        "lng": 121.440
      },
      "availability": true
    }
  ],
  "tasks": [
    {
      "id": "task_check_10015020001",
      "type_id": "FieldCheck",
      "location": {
        "lat": 23.656,
        "lng": 121.435
      },
      "urgency": 4
    }
  ]
}
```

### 2.4 Request field description

| Field | Type | Description |
|---|---|---|
| `metadata.incident_id` | string | Disaster incident or dispatch batch identifier |
| `metadata.priority_weighting` | string | Dispatch weighting mode: `balanced`, `speed`, `expertise` |
| `work_types[].type_id` | string | Task type identifier |
| `work_types[].required_skills` | string[] | Skill tags required for the task type |
| `volunteers[].id` | string | De-identified volunteer ID |
| `volunteers[].skills` | string[] | Volunteer skill tags |
| `volunteers[].location.lat` | number | Latitude |
| `volunteers[].location.lng` | number | Longitude |
| `volunteers[].availability` | boolean | Whether the volunteer is available |
| `tasks[].id` | string | Task ID |
| `tasks[].type_id` | string | Task type |
| `tasks[].location.lat` | number | Task latitude |
| `tasks[].location.lng` | number | Task longitude |
| `tasks[].urgency` | integer | Urgency level, from 1 to 5 |

### 2.5 Response format

```json
{
  "status": "success",
  "dispatch_id": "uuid-xxx",
  "assignments": [
    {
      "task_id": "task_check_10015020001",
      "assigned_volunteers": ["vol_01"],
      "eta_minutes": 15,
      "reasoning_summary": "[Ollama-dispatch] Assigned vol_01 because the volunteer has FirstAid and LocalGuide skills and is close to the task location."
    }
  ]
}
```

### 2.6 Response field description

| Field | Type | Description |
|---|---|---|
| `status` | string | Execution status |
| `dispatch_id` | string | Dispatch batch ID |
| `assignments[].task_id` | string | Task ID |
| `assignments[].assigned_volunteers` | string[] | Assigned volunteer IDs |
| `assignments[].eta_minutes` | integer | Estimated time of arrival in minutes |
| `assignments[].reasoning_summary` | string | Summary from AI or local algorithm |

## 3. Transformation contract between components

The output of the Silent Disaster Zone Detection API should not be treated as a direct dispatch order. A task-generation layer is needed in between.

### 3.1 MVP transformation rules

| Silent risk output | Task input |
|---|---|
| `village_id` | `task.id = task_check_{village_id}` |
| `silent_risk_level = high` | `urgency = 5` |
| `silent_risk_level = medium` | `urgency = 4` |
| `silent_risk_level = low` | `urgency = 2` |
| Keywords in `silent_reason`, such as road, communication, vulnerable residents | May affect `type_id` |
| GeoJSON centroid or village center | `task.location` |

### 3.2 Suggested task types

| type_id | Description | Suggested required skills |
|---|---|---|
| `FieldCheck` | Field verification | LocalGuide, FirstAid |
| `RoadCheck` | Road accessibility check | LocalGuide, Driving |
| `MedicalCheck` | Vulnerable or injured resident check | FirstAid, EMT |
| `Logistics` | Supply transport | HeavyLifting, Logistics |
| `CommunicationCheck` | Communication and contact verification | Radio, LocalGuide |

## 4. Error-handling recommendations

| Situation | Recommended behavior |
|---|---|
| Silent API has no output | Use sample output or report that data is not ready |
| Realtime data source fails | Keep the latest successful snapshot and mark data time |
| Dispatcher API has no available volunteers | Return empty `assigned_volunteers` and require manual assignment |
| Ollama is unreachable | Use deterministic local fallback algorithm |
| AI response cannot be parsed | Use debug model or local fallback algorithm |
| Task location lacks coordinates | Do not auto-dispatch; request manual coordinates |
