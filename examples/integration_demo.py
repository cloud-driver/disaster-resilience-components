import json
import math
from pathlib import Path
from typing import Dict, List, Any, Set, Optional


BASE_DIR = Path(__file__).resolve().parent


PRIORITY_RANK = {
    "urgent": 4,
    "high": 3,
    "medium": 2,
    "low": 1
}


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


def score_volunteer(task: Dict[str, Any], volunteer: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not volunteer.get("available", False):
        return None

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

    matched_skills = sorted(required_skills.intersection(volunteer_skills))
    missing_skills = sorted(required_skills.difference(volunteer_skills))

    if not matched_skills:
        return None

    skill_match_ratio = len(matched_skills) / len(required_skills)
    skill_score = skill_match_ratio * 100
    distance_penalty = distance * 3

    final_score = skill_score - distance_penalty

    return {
        "volunteer_id": volunteer["volunteer_id"],
        "name": volunteer["name"],
        "matched_skills": matched_skills,
        "missing_required_skills": missing_skills,
        "distance_km": round(distance, 2),
        "score": round(final_score, 2)
    }


def dispatch_task(
    task: Dict[str, Any],
    volunteers: List[Dict[str, Any]],
    assigned_volunteer_ids: Set[str]
) -> Dict[str, Any]:
    candidates = []

    for volunteer in volunteers:
        if volunteer["volunteer_id"] in assigned_volunteer_ids:
            continue

        scored_candidate = score_volunteer(task, volunteer)

        if scored_candidate is not None:
            candidates.append(scored_candidate)

    candidates.sort(key=lambda item: item["score"], reverse=True)

    recommended = candidates[0] if candidates else None

    warning = None
    if recommended is None:
        warning = "No available volunteer matched this task."
    elif recommended["missing_required_skills"]:
        warning = "Recommended volunteer does not cover all required skills. Human review is required."

    return {
        "task_id": task["task_id"],
        "area": task["area"],
        "priority": task["task"]["priority"],
        "required_skills": task["required_skills"],
        "recommended_volunteer": recommended,
        "candidates": candidates,
        "warning": warning
    }


def dispatch_all_tasks(
    tasks: List[Dict[str, Any]],
    volunteers: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
            PRIORITY_RANK.get(task["task"]["priority"], 0),
            task["risk"]["silent_risk_score"]
        ),
        reverse=True
    )

    assigned_volunteer_ids: Set[str] = set()
    results = []

    for task in sorted_tasks:
        result = dispatch_task(task, volunteers, assigned_volunteer_ids)

        recommended = result.get("recommended_volunteer")
        if recommended is not None:
            assigned_volunteer_ids.add(recommended["volunteer_id"])

        results.append(result)

    return results


def main() -> None:
    silent_zone_data = load_json(BASE_DIR / "sample_silent_zone_output.json")
    volunteer_data = load_json(BASE_DIR / "sample_volunteers.json")

    tasks = [risk_to_task(area) for area in silent_zone_data["areas"]]
    dispatch_results = dispatch_all_tasks(tasks, volunteer_data["volunteers"])

    output = {
        "demo_name": "Silent Disaster Zone to Volunteer Dispatch Integration Demo",
        "description": "This demo converts high-risk low-report areas into field-check tasks and recommends suitable volunteers without assigning the same volunteer twice.",
        "notes": [
            "This is a lightweight integration demo.",
            "Final dispatch decisions should be reviewed by human coordinators.",
            "AI or algorithmic recommendations must not replace emergency command decisions."
        ],
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
