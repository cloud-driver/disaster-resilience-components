<p align="right">
[繁體中文](ai_usage.md) | English
</p>

# AI Usage

## 1. Role of AI in this project

AI in this project is not used to replace commanders, nor to directly determine whether a disaster has definitely occurred. Its role is **assistive analysis and assistive dispatch**.

The two components use AI differently:

| Component | AI / intelligent role | Final decision-maker? |
|---|---|---|
| Silent Disaster Zone Detection API | Uses rule-based scoring and a neural network scoring layer to generate silent risk scores | No |
| Disaster Volunteer Dispatcher API | Uses a local Ollama LLM for assistive dispatch reasoning, with deterministic local fallback | No |

## 2. AI usage in the Silent Disaster Zone Detection API

### 2.1 Scoring layer

This component first builds an interpretable rule-based score, then uses a neural network scoring layer to generate `silent_risk_score`.

Conceptually:

```text
base_risk_score
= static risk
+ sensor gap
+ realtime event signal

silence_factor
= lower report activity → higher silence factor

silent_risk_score
= high risk × low report activity
```

### 2.2 Why keep the rule-based score?

The `silent_risk_rule_score` is kept so reviewers, users, and commanders can understand the scoring logic instead of seeing only a black-box value.

The AI scoring layer is valuable because:

- It can be replaced by a better model later
- It can be retrained with historical disaster data
- It can be compared against rule-based scores
- Model versions and metadata can be retained for auditability

### 2.3 Current limitation

If the MVP model is trained with pseudo-labels, it must not be presented as a model that accurately predicts real disasters. A more precise statement is:

> The current model verifies the replaceable scoring-layer architecture. Before production deployment, it should be retrained with historical disaster records, field verification results, report-delay data, and expert-labeled priority areas.

## 3. AI usage in the Disaster Volunteer Dispatcher API

### 3.1 Local Ollama inference

The Dispatcher API uses Ollama to run an LLM locally. This design offers several advantages:

- It can run on a local or internal machine
- It reduces the need to send task and volunteer data to external cloud models
- It lowers API costs
- It may preserve local inference capability when network connectivity is unstable

### 3.2 Two-model concept

The MVP can use two model roles:

| Model role | Purpose |
|---|---|
| Dispatch model | Generate assignment suggestions based on tasks, skills, distance, and urgency |
| Debug model | Re-interpret or repair invalid dispatch outputs |

### 3.3 Local algorithm fallback

A disaster-response system cannot assume AI is always available. Therefore, the Dispatcher API must keep a deterministic fallback algorithm.

The fallback can use:

```text
1. Filter volunteers with availability = true
2. Sort tasks by urgency from high to low
3. Prefer volunteers with matching skills
4. Calculate Haversine distance
5. Select nearby and suitable volunteers
6. Return ETA and explanation summary
```

Even if Ollama fails, the system can still return basic assignment recommendations.

## 4. AI boundaries

The project must clearly limit what AI is allowed to do:

1. **AI does not issue evacuation orders**  
   Evacuation, road closure, medical dispatch, and other official commands must remain with authorized agencies.

2. **AI does not claim that a disaster has definitely occurred**  
   A silent risk score means “needs verification,” not “confirmed disaster.”

3. **AI does not fabricate facts**  
   AI must only summarize from input JSON, API outputs, and system data. It must not invent road conditions, casualties, supplies, or sensor readings.

4. **AI outputs must be reviewable**  
   Every AI output should include a reasoning summary so commanders know why the suggestion was made.

5. **AI failure must degrade gracefully**  
   If AI is unreachable, unparseable, or too slow, the system should return to local rules and deterministic algorithms.

## 5. Recommended prompt principles

If an LLM is used to generate a command briefing, use a strongly constrained prompt:

```text
You are a disaster-response command assistant.
Use only the provided JSON data.
Do not claim that a disaster has definitely occurred.
Do not issue official evacuation orders.
Do not invent road conditions, casualties, sensor data, or reports that are not in the data.
Output:
1. Priority areas to verify
2. Reasons
3. Suggested field verification actions
4. Suggested communication actions
5. Data limitations
```

## 6. Data governance and privacy

The Dispatcher API should use de-identified IDs such as:

- `volunteer_id`
- `task_id`
- `incident_id`

Unless absolutely necessary, API input should not include volunteer names, phone numbers, national ID numbers, home addresses, or other personal information. If the system connects to a real volunteer database in the future, personal data should remain in the source system, and this component should only receive necessary de-identified dispatch data.

## 7. Recommended disclosure

The README or presentation should clearly disclose:

- Which parts use AI
- What data AI receives
- How AI output is constrained
- How fallback works when AI fails
- Whether the model uses real disaster labels
- Which outputs are suggestions only and not official commands

This is more convincing than simply saying “we used AI,” and it better matches the reliability and accountability requirements of disaster-response contexts.
