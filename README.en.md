<p align="right">
[繁體中文](README.md) | English
</p>

# Two-Component Disaster Response Decision Chain

> **Silent Disaster Zone Detection API × Disaster Volunteer Dispatcher API**  
> Identify high-risk areas that may be underreported, then assign verification or response tasks to the most suitable volunteers.

This repository is the **main proposal / integration repository** for the “Disaster-Prevention Building Block Component Innovation Challenge: Civic Tech for a Resilient Taiwan.” It is not a monolithic disaster-management platform. Instead, it presents two reusable API components that can be deployed independently and connected to other disaster-response systems.

## 1. Why do we need both components?

After a disaster, command centers usually see the places where reports already exist: flooded roads, blocked routes, urgent supply needs, or rescue requests.

However, the most dangerous places may be silent. Some villages may have high flood or landslide risk, a high proportion of elderly residents, possible road disruption, unstable connectivity, or weak sensor coverage. Yet they may generate few or no reports because residents cannot report, communication is down, or digital tools are difficult to use.

The first component, **Silent Disaster Zone Detection API**, answers:

> Which areas should receive attention but currently have few or no reports?

Once these areas are found, the next question is operational: who should verify the area, deliver supplies, provide medical help, or perform field checks?

The second component, **Disaster Volunteer Dispatcher API**, answers:

> Which volunteers are most suitable for each verification, patrol, or response task?

Together, the two components form a clear disaster-response decision chain:

```text
Silent Disaster Zone Detection API
Find high-risk, low-report, low-observation villages
        ↓
Generate verification / patrol / response tasks
        ↓
Disaster Volunteer Dispatcher API
Match tasks with volunteers based on task type, skills, location, availability, and urgency
        ↓
Human commander reviews and acts
```

## 2. Components

| Component | Role | Input | Output | Source repository |
|---|---|---|---|---|
| Silent Disaster Zone Detection API | Detect high-risk but underreported “silent disaster zones” | Village boundaries, population, risk maps, rainfall, landslide alerts, road events, reports | `silent_risk.json`, `silent_risk.csv`, `silent_risk.geojson` | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) |
| Disaster Volunteer Dispatcher API | Assign response tasks to suitable volunteers | Tasks, volunteers, skills, locations, availability, urgency | Assignment list, ETA, AI / algorithm reasoning summary | [D4rk-N355/disaster_rescuing](https://github.com/D4rk-N355/disaster_rescuing) |

## 3. Recommended repository structure

```text
disaster-resilience-components/
├── README.md
├── README.en.md
├── docs/
│   ├── story.md
│   ├── story.en.md
│   ├── architecture.md
│   ├── architecture.en.md
│   ├── api_contract.md
│   ├── api_contract.en.md
│   ├── ai_usage.md
│   ├── ai_usage.en.md
│   ├── limitations.md
│   └── limitations.en.md
└── components/
    ├── silent-disaster-zone-api/
    └── disaster_rescuing/
```

> We recommend copying the two existing repositories into `components/`, or keeping the original repository links in the README. This preserves the “building block” nature of the work better than merging both backends into one codebase.

## 4. Integration flow

1. **Data enters the Silent Disaster Zone Detection API**  
   The system combines static risk data and realtime event signals, such as village boundaries, population, elderly ratio, flood potential, landslide data, rainfall, road events, and report records.

2. **High-priority areas are returned**  
   The API outputs village-level silent risk scores, risk levels, explanation strings, and a GeoJSON layer.

3. **Areas are converted into verification or response tasks**  
   High-risk but low-report areas can be converted into tasks such as “verify road accessibility,” “check vulnerable households,” or “confirm supply needs.”

4. **Tasks are sent to the Volunteer Dispatcher API**  
   The dispatcher API uses task type, volunteer skills, volunteer locations, availability, and urgency to recommend assignments.

5. **Humans make the final decision**  
   AI and algorithms provide decision support only. They do not issue evacuation orders or replace official command authority.

## 5. Documentation

| Document | Traditional Chinese | English |
|---|---|---|
| Story and problem definition | [docs/story.md](docs/story.md) | [docs/story.en.md](docs/story.en.md) |
| Architecture | [docs/architecture.md](docs/architecture.md) | [docs/architecture.en.md](docs/architecture.en.md) |
| API contract | [docs/api_contract.md](docs/api_contract.md) | [docs/api_contract.en.md](docs/api_contract.en.md) |
| AI usage | [docs/ai_usage.md](docs/ai_usage.md) | [docs/ai_usage.en.md](docs/ai_usage.en.md) |
| Limitations and risks | [docs/limitations.md](docs/limitations.md) | [docs/limitations.en.md](docs/limitations.en.md) |

## 6. MVP scope

The current MVP focuses on:

- Village-level silent disaster zone detection in Hualien County
- Village risk scores and GeoJSON output
- Standardized JSON input for tasks and volunteers
- Local Ollama-based AI dispatch suggestions
- Deterministic fallback dispatch when AI is unavailable
- FastAPI / Swagger documentation

## 7. Core value

The project is not trying to build a large all-in-one platform. It separates the response workflow into two reusable components:

1. **See the overlooked areas**: Avoid relying only on high-report hotspots and missing high-risk silent areas.
2. **Send the right people to the right places**: Match verification, patrol, logistics, medical, and administrative tasks with suitable responders faster.

## 8. Boundaries of use

The risk scores and dispatch assignments are **decision-support outputs**. They are not official disaster confirmations and not evacuation orders. Final response decisions must remain with authorized government agencies, field commanders, or qualified professionals.
