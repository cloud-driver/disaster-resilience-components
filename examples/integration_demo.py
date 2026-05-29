import json
import math
from pathlib import Path
from typing import Dict, List, Any


BASE_DIR = Path(__file__).resolve().parent


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius_km = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def risk_to_task(area: Dict[str, Any]) -> Dict[str, Any]:
    risk_score = area["silent_risk_score"]

    if risk_score >= 0.9:
        priority = "urgent"
    elif risk_score >= 0.75:
        priority = "high"
    elif risk_score >= 0.5:
        priority = "medium"
    else:
        priority = "low"

    required_skills = ["field_check"]

    if "高齡人口比例高" in area.get("reasons", []):
        required_skills.append("medical")

    if "鄰近道路可能中斷" in area.get("reasons", []) or "交通可及性較低" in area.get("reasons", []):
        required_skills.append("transport")

    return {
        "task_id": f"TASK-{area['area_id']}",
        "source_component": "silent-disaster-zone-api",
        "area": {
            "county": area["county"],
            "town": area["town"],
            "village": area["village"]
        },
        "risk": {
            "silent_risk_score": area["silent_risk_score"],
            "risk_level": area["risk_level"],
            "reasons": area["reasons"]
        },
        "task": {
            "task_type": "field_check",
            "priority": priority,
            "description": f"請前往{area['county']}{area['town']}{area['village']}確認是否有未通報災情。"
        },
        "location": {
            "lat": area["lat"],
            "lng": area["lng"]
        },
        "required_skills": required_skills
    }


def score_volunteer(task: Dict[str, Any], volunteer: Dict[str, Any]) -> float:
    if not volunteer.get("available", False):
        return -1

    task_lat = task["location"]["lat"]
    task_lng = task["location"]["lng"]

    distance = haversine_km(
        task_lat,
        task_lng,
        volunteer["lat"],
        volunteer["lng"]
    )

    required_skills = set(task["required_skills"])
    volunteer_skills = set(volunteer["skills"])
    matched_skills = len(required_skills.intersection(volunteer_skills))

    skill_score = matched_skills * 50
    distance_penalty = distance * 3

    return skill_score - distance_penalty


def dispatch_task(task: Dict[str, Any], volunteers: List[Dict[str, Any]]) -> Dict[str, Any]:
    candidates = []

    for volunteer in volunteers:
        score = score_volunteer(task, volunteer)

        if score < 0:
            continue

        distance = haversine_km(
            task["location"]["lat"],
            task["location"]["lng"],
            volunteer["lat"],
            volunteer["lng"]
        )

        candidates.append({
            "volunteer_id": volunteer["volunteer_id"],
            "name": volunteer["name"],
            "matched_skills": list(set(task["required_skills"]).intersection(set(volunteer["skills"]))),
            "distance_km": round(distance, 2),
            "score": round(score, 2)
        })

    candidates.sort(key=lambda item: item["score"], reverse=True)

    return {
        "task_id": task["task_id"],
        "area": task["area"],
        "priority": task["task"]["priority"],
        "required_skills": task["required_skills"],
        "recommended_volunteer": candidates[0] if candidates else None,
        "candidates": candidates
    }


def main() -> None:
    silent_zone_data = load_json(BASE_DIR / "sample_silent_zone_output.json")
    volunteer_data = load_json(BASE_DIR / "sample_volunteers.json")

    tasks = [risk_to_task(area) for area in silent_zone_data["areas"]]
    dispatch_results = [
        dispatch_task(task, volunteer_data["volunteers"])
        for task in tasks
    ]

    output = {
        "demo_name": "Silent Disaster Zone to Volunteer Dispatch Integration Demo",
        "description": "This demo converts high-risk low-report areas into field-check tasks and recommends suitable volunteers.",
        "tasks": tasks,
        "dispatch_results": dispatch_results
    }

    output_path = BASE_DIR / "sample_dispatch_output.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nDemo output saved to: {output_path}")


if __name__ == "__main__":
    main()