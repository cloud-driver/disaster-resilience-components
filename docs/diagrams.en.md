# System Diagrams

## 1. End-to-end data flow

```mermaid
flowchart TD
  A[Static risk, village boundaries, population features] --> D[Cleaning and spatial normalization]
  B[Rainfall, alerts, road/event signals] --> D
  C[LINE / manual / API reports] --> E[pending]
  E --> F[Human review]
  F -->|verified| G[Verified-report features]
  F -->|rejected| H[Review record only]
  D --> I[Risk and observation features]
  G --> J[Formal rule-based scoring]
  I --> J
  J --> K[silent_watch_queue]
  G --> L[verified_incident_queue]
  K --> M[Human confirmation]
  L --> M
  M --> N[IntegratedTask]
  N --> O[Adapter]
  P[Volunteer roster / forms / LINE registration] --> Q[Volunteer Dispatch API]
  O --> Q
  Q --> R[Candidates, ETA, score breakdown, warnings]
  R --> S[Human coordinator decision]
```

## 2. Report lifecycle

```mermaid
stateDiagram-v2
  [*] --> pending: LINE / Manual / API report
  pending --> verified: Human review accepted
  pending --> rejected: Human review rejected
  verified --> report_features: 6h / 24h features
  verified --> incident_queue: Credible incident snapshot
  rejected --> [*]
```

## 3. The two queues

```mermaid
flowchart LR
  A[Silent risk result] --> B[silent_watch_queue]
  C[Human-verified report] --> D[verified_incident_queue]
  B --> E[Question: where needs proactive confirmation?]
  D --> F[Question: where has a credible incident needing review?]
  E --> G[Human task creation]
  F --> G
```

The queues must not be conflated. A silent-watch priority is not a disaster declaration; a verified incident is not “less important” merely because it is no longer silent.

## 4. What the current local demo actually does

```mermaid
flowchart LR
  A[examples/sample_silent_zone_output.json] --> B[risk_to_task]
  B --> C[IntegratedTask-like local dict]
  D[examples/sample_volunteers.json] --> E[local scoring]
  C --> E
  E --> F[examples/sample_dispatch_output.json]
```

The current demo uses local sample JSON and embedded Python logic; it does not invoke child-service HTTP endpoints.

## 5. Target API-to-API adapter

```mermaid
sequenceDiagram
  participant SZ as Silent Zone API
  participant AD as Integration Adapter
  participant VD as Volunteer Dispatch API
  participant CO as Human Coordinator

  CO->>SZ: Read validated risk/incident results
  SZ-->>AD: Result + metadata + queue
  AD->>AD: Build and validate IntegratedTask
  AD->>AD: Map priority→urgency and skills→work_types
  AD->>VD: POST /api/v1/dispatch
  VD-->>AD: DispatchResponse
  AD-->>CO: Candidates, ETA, warnings, data status
  CO->>CO: Human confirmation before real action
```
