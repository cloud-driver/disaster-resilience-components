<p align="right">
<a href="./README.md">繁體中文</a> | English
</p>

# Documentation Guide
This folder contains the design documents, technical specifications, and reviewer guide for **Disaster Resilience Components**.

This project is developed by **Islewise Tech**.
Its goal is to build reusable, independently operable, and composable disaster-resilience API components based on a modular “building block” design.

The main repository integrates two core components:

1. **Silent Disaster Zone API**
   Detects high-risk but low-reporting areas and outputs locations that require proactive field verification.

2. **Volunteer Dispatch API**
   Recommends suitable disaster-response volunteers based on task requirements, skills, location, and availability.

The two components can be used independently or connected as one disaster-response decision-support workflow:

```text
Public risk data / incident reports / road status / village-level data
        ↓
Silent Disaster Zone API
        ↓
High-risk low-reporting areas
        ↓
Task transformation
        ↓
Volunteer Dispatch API
        ↓
Volunteer recommendations and dispatch suggestions
```

---

## Reviewer Quick Path

If review time is limited, we recommend reading the documents in the following order:

| Step | File / Directory                                                                   | Purpose                                                                      |
| ---- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1    | [`../README.en.md`](../README.en.md)                                               | Understand the problem, solution, component design, and overall value        |
| 2    | [`quickstart.md`](./quickstart.md)                                                 | Run the MVP demo quickly                                                     |
| 3    | [`diagrams.md`](./diagrams.md)                                                     | Review the system flow, data flow, and component boundaries                  |
| 4    | [`architecture.md`](./architecture.md)                                             | Understand the architecture, module responsibilities, and integration design |
| 5    | [`api_contract.md`](./api_contract.md)                                             | Review Input / Process / Output and API contracts                            |
| 6    | [`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json) | Review the shared JSON Schema for integrated tasks                           |
| 7    | [`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml)       | Review the OpenAPI / Swagger specification                                   |
| 8    | [`data_sources.md`](./data_sources.md)                                             | Review real-world disaster-data sources that can be connected in production  |
| 9    | [`ai_usage.md`](./ai_usage.md)                                                     | Understand how AI is used in the project                                     |
| 10   | [`ai_governance.md`](./ai_governance.md)                                           | Review AI risks, limitations, human review, and governance principles        |
| 11   | [`../components/README.en.md`](../components/README.en.md)                         | Review the two component repositories and their roles                        |
| 12   | [`../examples/integration_demo.py`](../examples/integration_demo.py)               | Review the executable integration demo                                       |

---

## Document Index

### [`quickstart.md`](./quickstart.md)

Provides the shortest path to verify the MVP data flow.

It covers:

* How to run the integration demo
* Demo input and output
* How to verify the connection between the two components
* How to interpret sample data versus real deployment data

---

### [`architecture.md`](./architecture.md)

Explains the overall technical architecture and component boundaries.

It covers:

* Two-component architecture
* Responsibility of each component
* Data-flow design
* Independent deployment and integrated usage
* Future integration with external disaster-response systems

---

### [`diagrams.md`](./diagrams.md)

Provides diagrams for quickly understanding how the project works.

It covers:

* Overall system flow
* Data flow between components
* Transformation from Silent Disaster Zone API output to Volunteer Dispatch API input
* Human-in-the-loop review points

---

### [`api_contract.md`](./api_contract.md)

Defines the API contracts of the two components and the integrated workflow.

It covers:

* Endpoint descriptions
* Request / response formats
* Input / Process / Output definitions
* Data exchange between components
* Standardized JSON data formats

---

### [`data_sources.md`](./data_sources.md)

Explains the real-world disaster-data sources that can be connected in a production deployment.

It covers:

* Disaster-risk data
* Village-level and population data
* Road-disruption and traffic data
* Incident-reporting data
* Volunteer and resource data
* Licensing, privacy, and data-quality limitations

The current MVP demo uses sample / mock data to verify the workflow.
In production, these data sources can be replaced with real open data or authorized datasets.

---

### [`ai_usage.md`](./ai_usage.md)

Explains the role of AI in this project.

It covers:

* How AI supports risk analysis
* How AI supports task summarization and dispatch recommendations
* Why AI does not make final decisions
* How AI outputs are kept reviewable and traceable
* How generative AI was used during design and development

---

### [`ai_governance.md`](./ai_governance.md)

Explains AI boundaries, risks, and governance principles.

It covers:

* AI does not automatically issue evacuation orders
* AI does not automatically determine official disaster severity
* AI does not automatically execute dispatch commands
* Human review and human override are preserved
* Fallback principles for insufficient data, uncertainty, or service failure
* Design considerations to prevent incorrect recommendations, over-automation, and misuse

---

## Specifications and Code Locations

| Type                  | Path                                                                 | Description                                             |
| --------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| Integration demo      | [`../examples/integration_demo.py`](../examples/integration_demo.py) | Executable MVP integration demo                         |
| Sample input data     | [`../examples/sample_input/`](../examples/sample_input/)             | Sample input used by the demo                           |
| Sample output data    | [`../examples/sample_output/`](../examples/sample_output/)           | Sample output generated or referenced by the demo       |
| JSON Schema           | [`../schemas/`](../schemas/)                                         | Standardized data-exchange formats                      |
| OpenAPI specification | [`../openapi/`](../openapi/)                                         | Swagger / OpenAPI contract for API components           |
| Component directory   | [`../components/`](../components/)                                   | Guide and links to the two disaster-response components |

---

## Mapping to Competition Requirements

| Competition Requirement                 | Corresponding Location                                                                                                               |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| GitHub project link                     | [`../README.en.md`](../README.en.md)                                                                                                 |
| Component role and problem statement    | [`../README.en.md`](../README.en.md), [`architecture.md`](./architecture.md)                                                         |
| Input / Process / Output                | [`api_contract.md`](./api_contract.md)                                                                                               |
| JSON Schema                             | [`../schemas/integrated_task.schema.json`](../schemas/integrated_task.schema.json)                                                   |
| System flow or architecture diagram     | [`diagrams.md`](./diagrams.md), [`architecture.md`](./architecture.md)                                                               |
| AI technical architecture and usage     | [`ai_usage.md`](./ai_usage.md)                                                                                                       |
| AI risks and limitations                | [`ai_governance.md`](./ai_governance.md)                                                                                             |
| Real-world disaster-data sources        | [`data_sources.md`](./data_sources.md)                                                                                               |
| Client sample code                      | [`../examples/integration_demo.py`](../examples/integration_demo.py)                                                                 |
| README guide and dependency description | [`../README.en.md`](../README.en.md), [`quickstart.md`](./quickstart.md), [`../components/README.en.md`](../components/README.en.md) |
| OpenAPI / Swagger specification         | [`../openapi/integrated-flow-api.yaml`](../openapi/integrated-flow-api.yaml)                                                         |

---

## MVP Verification

Run the following command from the repository root:

```bash
python3 examples/integration_demo.py
```

The demo shows how to:

1. Receive silent-disaster-zone detection results
2. Convert high-risk low-reporting areas into field-verification tasks
3. Call the volunteer-dispatch logic
4. Output recommended volunteers and task-assignment results

This verifies that the two components are not only conceptual modules, but can also be connected through standardized JSON formats into a testable disaster-response decision-support workflow.

---

## Notes

This project is currently an MVP and prototype.
Its purpose is to demonstrate:

* Modular component design
* Standardized data exchange
* Verifiable core functionality
* Extensible disaster-data integration
* AI-assisted decision support with human oversight

The demo uses sample / mock data and should not be interpreted as an official disaster assessment.
For production deployment, the system should connect to real authorized data sources and include review by qualified disaster-response professionals.
