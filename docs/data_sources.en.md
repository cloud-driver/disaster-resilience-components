<p align="right">
<a href="./data_sources.md">繁體中文</a> | English
</p>

# Data Sources and Integration Plan

This project currently uses sample data to validate the dual-component workflow. In real deployment, it can integrate public disaster data, village-level data, road status data, disaster reports, and volunteer data.

## Planned Data Sources

| Data Type | Purpose | MVP Usage | Production Integration |
|---|---|---|---|
| Village boundary and administrative data | Define the analysis unit and map risk scores to villages | Sample village data | Government open data or GIS datasets |
| Rainfall, water level, flood, or debris-flow risk data | Estimate regional disaster risk | Simulated risk fields | Real-time observation or disaster-prevention open data |
| Disaster report data | Detect areas with unexpectedly low reporting | Sample report count | Reporting systems, LINE Bot, forms, or APIs |
| Road status data | Estimate accessibility and rescue difficulty | Sample road status | Road closure, bridge, or transportation interruption data |
| Population and elderly ratio data | Identify vulnerable areas and proactive field-check needs | Sample demographic indicators | Population statistics or village-level datasets |
| Volunteer data | Match tasks with suitable volunteers | `examples/sample_volunteers.json` | Volunteer platforms, local agencies, or disaster-response groups |

## MVP Data

The repository currently provides:

- `examples/sample_silent_zone_output.json`
- `examples/sample_volunteers.json`
- `examples/sample_dispatch_output.json`

These files are used to validate the data flow and do not represent real disaster results.

## Deployment Notes

1. Data licenses and update frequency must be verified.
2. Real-time data may contain delay, missing values, or inconsistent formats.
3. Volunteer data involves personal information and must follow consent and data minimization principles.
4. System output should support decision-making, not replace emergency command or field judgment.
