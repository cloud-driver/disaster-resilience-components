# Quick Start

## 0. What this repository can verify today

The parent repository can directly verify an **offline data flow**:

```text
sample_silent_zone_output.json
  → IntegratedTask
  → sample_volunteers.json
  → sample_dispatch_output.json
```

It needs no API key and does not start either child service. It is therefore not evidence of an API-to-API deployment.

## 1. Run the offline integration demo

Requirement: Python 3.10+; the demo uses only the standard library.

macOS / Linux:

```bash
python3 examples/integration_demo.py
```

Windows:

```powershell
python examples\integration_demo.py
```

Expected output:

```text
examples/sample_dispatch_output.json
```

Check that the output contains tasks, candidates, no duplicate volunteer recommendations in one run, and explicit warnings when no candidate or incomplete skill coverage exists.

## 2. Start the silent-zone component

```bash
git clone https://github.com/cloud-driver/silent-disaster-zone-api.git
cd silent-disaster-zone-api

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs`. Check `/health` first. Only a completed, source-healthy `live` result can be used as current human-review support.

## 3. Start the volunteer-dispatch component

```bash
git clone https://github.com/D4rk-N355/volunteer_distributing.git
cd volunteer_distributing

python -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8001
```

Port `8001` avoids conflict with the silent-zone service.

```bash
curl http://127.0.0.1:8001/health
```

## 4. Minimum requirements for production integration

1. Fetch validated risk or verified-incident results plus metadata from the silent-zone API.
2. Keep `silent_watch_queue` and `verified_incident_queue` semantically separate.
3. Transform the result to `IntegratedTask`.
4. Transform `IntegratedTask` to `DispatchRequest`:
   - priority → urgency (1–5)
   - task type → type ID
   - required skills → work type requirements
   - add authorized, current volunteer records
5. Let an accountable coordinator review the output before contact or dispatch.

See [API & data contract](./api_contract.en.md).

## 5. Do not skip before production

Use HTTPS/reverse proxy, protect management endpoints, add audit logging, move in-memory volunteer state to persistent storage, use protected jobs instead of public synchronous refresh, and implement privacy/retention controls.
