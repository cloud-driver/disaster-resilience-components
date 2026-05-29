<p align="right">
<a href="./quickstart.md">繁體中文</a> | English
</p>

# Quickstart

This document explains how to run the integration demo for the dual disaster-response component chain.

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd disaster-resilience-components
````

## 2. Check Python Version

Python 3.9 or later is recommended.

```bash
python3 --version
```

## 3. Run the Integration Demo

```bash
python3 examples/integration_demo.py
```

The demo will:

1. Convert silent disaster zone detection results into field-check tasks
2. Match each task with suitable volunteers
3. Output dispatch recommendations in JSON
4. Generate `examples/sample_dispatch_output.json`

## 4. Demo Flow

```text
Silent Disaster Zone API Output
        ↓
High-risk Low-report Areas
        ↓
Field-check / Rescue Tasks
        ↓
Volunteer Dispatch Logic
        ↓
Dispatch Recommendations
```

## 5. Notes

This demo uses sample data and does not represent actual emergency dispatch decisions.
In real deployment, algorithmic or AI-generated recommendations must be reviewed by emergency coordinators or responsible authorities.
EOF