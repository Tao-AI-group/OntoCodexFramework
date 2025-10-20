# OntoCodex v1.1 — Multi-Agent LLM Ontology Framework

Aligned to your Source Priority Tree, evidence rules, and mapping constraints.

Install:
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run API:
```
export ONTOCODEX_DATA_DIR=./data
uvicorn api.api_server:app --reload
```
