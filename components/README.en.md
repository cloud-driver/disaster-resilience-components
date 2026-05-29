<p align="right">
<a href="./README.md">繁體中文</a> | English
</p>

# Components

This folder contains local snapshots of the two disaster-response components so reviewers can see the complete submission structure after cloning the main repository.  
However, the **original component repositories remain the primary review entry points**.

---

## Original Component Repositories

| Component | Original Repository | Function |
|---|---|---|
| Silent Disaster Zone Detection API | [cloud-driver/silent-disaster-zone-api](https://github.com/cloud-driver/silent-disaster-zone-api) | Identifies high-risk but low-report areas and outputs JSON / CSV / GeoJSON |
| Disaster Volunteer Dispatcher API | [D4rk-N355/disaster_rescuing](https://github.com/D4rk-N355/disaster_rescuing) | Recommends volunteers based on task needs, skills, location, and availability |

---

## Recommended Review Path

```text
1. Review the original component repo: Silent Disaster Zone Detection API
        ↓
2. Review the original component repo: Disaster Volunteer Dispatcher API
        ↓
3. Return to the main repository and run examples/integration_demo.py
        ↓
4. Review schemas/, openapi/, and docs/ for data contracts and integration design
```

---

## Why Keep Local Snapshots?

The local snapshots do not replace the original repositories.  
They help the main repository provide a complete submission context.

They help reviewers understand that:

1. This project is composed of two components
2. The two components can exist independently
3. The main repository is the integration entry point and demo layer
4. The integration demo shows how the two components can be connected

---

## Folder Structure

```text
components/
├── README.md
├── README.en.md
├── silent-disaster-zone-api/
└── disaster-rescuing/
```

| Folder | Description |
|---|---|
| `silent-disaster-zone-api/` | Local snapshot of the silent disaster zone detection component |
| `disaster-rescuing/` | Local snapshot of the volunteer dispatch component |

---

## Relationship with the Main Repository

The integration demo is located at:

```text
examples/integration_demo.py
```

The demo simulates the following flow:

```text
Silent disaster zone detection result
        ↓
IntegratedTask standard task format
        ↓
Volunteer dispatch logic
        ↓
Dispatch recommendation
```

The `IntegratedTask` data format is defined at:

```text
schemas/integrated_task.schema.json
```

The integration OpenAPI contract is defined at:

```text
openapi/integrated-flow-api.yaml
```

---

## How to Update Local Snapshots

To update the local snapshots, sync them from the original repositories.  
Before committing, make sure not to include `.env`, tokens, API keys, real personal data, or private IP addresses.

Example workflow:

```bash
rm -rf components/silent-disaster-zone-api
rm -rf components/disaster-rescuing

git clone https://github.com/cloud-driver/silent-disaster-zone-api.git /tmp/silent-disaster-zone-api
git clone https://github.com/D4rk-N355/disaster_rescuing.git /tmp/disaster-rescuing

cp -R /tmp/silent-disaster-zone-api components/silent-disaster-zone-api
cp -R /tmp/disaster-rescuing components/disaster-rescuing

rm -rf components/silent-disaster-zone-api/.git
rm -rf components/disaster-rescuing/.git
```

---

## What Must Not Be Committed Here

Do not commit the following content into this folder:

- `.env`
- API keys
- tokens
- passwords
- real volunteer personal data
- real contact information
- private IP addresses
- Tailscale IP addresses
- ngrok URLs
- `__pycache__/`
- `.DS_Store`

This folder should only contain publicly reviewable code, documentation, sample data, and component descriptions.