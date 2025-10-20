# OntoCodex v1.2 Guidelines Patch

Adds a real **GuidelineTool** and a **GuidelineToolAgent**, plus planner routing for guideline intent.

## Install
Unzip into your OntoCodex v1.1 repo:
```bash
unzip ontocodex_v1_2_guidelines_patch.zip -d your_ontocodex_repo/
```

## Use
```bash
export ONTOCODEX_DATA_DIR=./data
python examples/run_multi_agent_guidelines.py
```

The planner router detects guideline intent (e.g., "guideline", "ADA", "AHA", "NIH", "CDC") and routes the task to the `guideline_tool` agent, which queries PubMed E-utilities (JSON) for recent titles and returns `{source, title, url, year}` items.
