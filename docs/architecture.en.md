<p align="right">
[繁體中文](architecture.md) | English
</p>

# Architecture

## 1. Architectural positioning

This project uses a “main integration repository + two independent API components” design.

```text
Main integration repository
Explains the story, architecture, API contract, AI usage, and limitations
        │
        ├── Component A: Silent Disaster Zone Detection API
        │       Detects high-risk but underreported silent disaster zones
        │
        └── Component B: Disaster Volunteer Dispatcher API
                Generates assignment recommendations from tasks and volunteer data
```

The two components have clear boundaries and should not be forced into a single backend. Keeping them independent allows other disaster-response systems to adopt only one component, or connect both into a complete response decision chain.

## 2. High-level data flow

```text
[Open data / realtime data / report data]
        ↓
[Silent Disaster Zone Detection API]
        ↓
[High-risk low-report area list + GeoJSON]
        ↓
[Task generator: patrol, verification, rescue, supplies]
        ↓
[Disaster Volunteer Dispatcher API]
        ↓
[Assignment suggestions: task ID, volunteer ID, ETA, reason]
        ↓
[Human commander review]
        ↓
[Field feedback / task results]
        ↓
[Feedback returns as report data and model-improvement data]
```

## 3. Component A: Silent Disaster Zone Detection API

### 3.1 Role

This component generates village-level silent risk scores. It combines disaster risk with reporting gaps to find places that should be verified but currently have few reports or weak observation coverage.

### 3.2 Input data

| Type | Format | Purpose |
|---|---|---|
| Village boundaries | GeoJSON / Shapefile | Define spatial analysis units |
| Population and age structure | CSV | Estimate vulnerability, such as elderly ratio |
| Flood potential | GeoJSON / Shapefile | Build static disaster risk |
| Debris-flow data | GeoJSON / Shapefile / API snapshot | Build mountain-area hazard signals |
| Realtime rainfall | JSON API snapshot | Build realtime event signals |
| Road events | JSON API snapshot | Estimate possible access disruption |
| Disaster reports | JSON | Calculate recent report counts and reporting gaps |

### 3.3 Processing logic

```text
Static risk features
    = village boundary + population + flood potential + debris flow data

Realtime event features
    = rainfall + landslide alert + road events

Report features
    = report count in recent time windows

Silent risk score
    = high risk signal × low report activity / observation gap
```

### 3.4 Output

| Output | Format | Description |
|---|---|---|
| `silent_risk.json` | JSON | Data for API queries |
| `silent_risk.csv` | CSV | Manual inspection and table analysis |
| `silent_risk.geojson` | GeoJSON | Map layer for dashboards |

## 4. Component B: Disaster Volunteer Dispatcher API

### 4.1 Role

This component receives task and volunteer data and generates assignment recommendations. Its purpose is not to replace commanders, but to reduce the burden of manually comparing skills, distance, availability, and urgency.

### 4.2 Input data

| Type | Fields | Purpose |
|---|---|---|
| metadata | incident_id, priority_weighting | Set incident and dispatch mode |
| work_types | type_id, required_skills | Define task types and required skills |
| volunteers | id, skills, location, availability | Describe available volunteers |
| tasks | id, type_id, location, urgency | Describe pending tasks |

### 4.3 Processing logic

```text
Receive task and volunteer data
        ↓
Filter available volunteers
        ↓
Sort tasks by urgency
        ↓
Calculate distance between volunteers and tasks
        ↓
Use Ollama dispatch model to generate suggestions
        ↓
If AI output is invalid, use debug model or local algorithm
        ↓
Return assignment list
```

### 4.4 Fallback design

If Ollama is unreachable, the model is missing, inference times out, or the AI response cannot be parsed, the system falls back to a local deterministic algorithm:

```text
Available volunteers → skill / distance priority → nearest or most suitable volunteer → ETA → assignment result
```

This matters because disaster scenarios cannot assume that AI services are always available.

## 5. Integration between the two components

### 5.1 Conceptual integration

The output of the Silent Disaster Zone Detection API can be converted into task input for the Dispatcher API.

For example:

```json
{
  "village_id": "10015020001",
  "county_name": "花蓮縣",
  "town_name": "鳳林鎮",
  "village_name": "鳳仁里",
  "silent_risk_score": 0.392821,
  "silent_risk_level": "medium",
  "silent_reason": "High static risk; sensor coverage gap; no reports in the last 6 hours"
}
```

Can be converted into:

```json
{
  "id": "task_check_10015020001",
  "type_id": "FieldCheck",
  "location": {
    "lat": 23.75,
    "lng": 121.45
  },
  "urgency": 4
}
```

### 5.2 Implementation recommendation

For the MVP, a simple converter can be used:

```text
silent_risk_level = high   → urgency = 5
silent_risk_level = medium → urgency = 4
silent_risk_level = low    → urgency = 2
```

A future version can add more rules:

- High elderly ratio → prefer volunteers with first-aid or care experience
- Clear road event → change task type to RoadCheck
- Strong debris-flow signal → change task type to HazardVerification
- Possible communication outage → prioritize village chief, fire station, or nearby volunteers

## 6. Deployment recommendation

### 6.1 MVP deployment

```text
Local Machine
├── FastAPI: Silent Disaster Zone Detection API
├── FastAPI: Disaster Volunteer Dispatcher API
└── Ollama: Local LLM runtime
```

### 6.2 Demo deployment

```text
Browser / Swagger UI
        ↓
FastAPI services
        ↓
Sample outputs / mock data
        ↓
Optional local Ollama
```

### 6.3 Future deployment

```text
Dashboard / LINE Bot / Google Chat
        ↓
API Gateway
        ↓
Silent Disaster Zone Detection API
        ↓
Task Generator
        ↓
Volunteer Dispatcher API
        ↓
Incident Management System
```

## 7. Architecture principles

1. **Clear component boundaries**: detection and dispatch are separate.
2. **Standardized data formats**: JSON, CSV, and GeoJSON.
3. **Independent operation**: each API can be called by other systems.
4. **Human review**: AI does not make final disaster decisions.
5. **Graceful degradation**: basic functionality remains available when AI is unavailable.
