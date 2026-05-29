<p align="right">
<a href="./story.md">繁體中文</a> | English
</p>

# Story and Problem Definition

## 1. The most dangerous signal in a disaster may be silence

After a major disaster, command centers receive many reports: flooding, road closures, supply shortages, trapped residents, and medical needs. These reports form a visible “hotspot map.”

However, areas with many reports are not necessarily the only dangerous areas. The real blind spots are places that are **high-risk but silent**.

For example, a village may have:

- High flood or landslide potential
- A high proportion of elderly residents
- Possible road disruption nearby
- Rising rainfall or landslide alert signals
- Weak sensor coverage
- Few or no reports in the last 6 or 24 hours

Such a place should not be treated as “safe” simply because no one reported anything. A more careful assumption is:

> It may not be safe. It may simply be unseen.

## 2. Component 1: Identify overlooked areas

The role of the **Silent Disaster Zone Detection API** is to identify:

> Villages with high risk, low reporting activity, and low observation coverage.

It does not claim that a disaster has definitely happened. Instead, it outputs areas that deserve priority verification.

The value of this component is to move disaster response beyond “only looking at reported hotspots” and help commanders proactively see areas that may otherwise be ignored.

## 3. Component 2: Assign tasks to suitable people

After high-priority areas are identified, the next question is operational:

- Who should verify the area?
- Who has medical skills?
- Who can handle logistics?
- Who is closest?
- Who is currently available?
- Which task is most urgent?

The role of the **Disaster Volunteer Dispatcher API** is to match response tasks with available volunteers.

It receives task and volunteer data, then uses skills, distance, availability, and urgency to recommend assignments. If the local AI model is available, the system uses Ollama for assistive reasoning. If AI is unavailable, it falls back to a deterministic local algorithm so basic dispatch capability remains available.

## 4. Why do both components need to exist together?

If we only have the Silent Disaster Zone Detection API, the system can answer “where should we pay attention,” but not “who should go.”

If we only have the Volunteer Dispatcher API, the system can only process tasks that have already been created. It may still miss high-risk areas that generated no reports.

Together, they form a more complete response chain:

```text
Detect overlooked high-risk areas
        ↓
Create verification or response tasks
        ↓
Match suitable volunteers
        ↓
Human commander reviews and dispatches
        ↓
Field feedback flows back as data
```

## 5. Typical scenario

### Scenario: Reporting gaps after heavy rainfall in Hualien

After heavy rainfall, some villages generate many reports, so the command center naturally focuses on those hotspots. But the system identifies another village with the following conditions:

- High static disaster risk
- Weak sensor coverage
- No reports in the last 6 hours
- No reports in the last 24 hours
- Nearby rainfall or road event signals

The Silent Disaster Zone Detection API marks it as a priority verification area. The system then creates a task:

```text
Task: Verify road accessibility and vulnerable households
Type: FieldCheck
Urgency: 4 / 5
Location: Village center or nearby risk coordinate
```

This task is sent to the Disaster Volunteer Dispatcher API. The system selects available volunteers who are nearby and have relevant first-aid or field-check experience, then returns recommended assignments and estimated arrival time.

Finally, the field commander reviews the suggestion and decides whether to dispatch.

## 6. One-sentence version

> We are not building a full disaster-response platform. We are building two reusable components: one helps systems see “silent but potentially dangerous areas,” and the other assigns verification or response tasks to the most suitable people.
