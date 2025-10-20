# OntoCodex Chat API (v0.8)

FastAPI microservice exposing a **/chat** endpoint that runs the OntoCodex **agent with memory + LLM planner**.

> Requires OntoCodex framework (v0.7+ recommended) to be installed separately.

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# In the same environment, install OntoCodex (v0.7+)
# pip install -e ../ontocodex_v0_7_self_training_patch (plus prior versions you merged)
```

## Run
```bash
export ONTOCODEX_DATA_DIR=../your_data_dir   # must contain DOID.owl, MEDLINEPLUS.ttl, HP.csv, OMOP CSVs
uvicorn api_server:app --reload
```

## Endpoints
- `GET /ping` — healthcheck
- `POST /chat` — run one turn with memory + planner + tools
- `POST /reset` — reset a session
- `GET /session/{session_id}/history` — inspect memory state
- `GET /config` — peek planner backend (OpenAI / Anthropic / local-ft / stub)

### POST /chat
**Request:**
```json
{
  "session_id": "optional-session-id",
  "user_text": "Map TSH to LOINC"
}
```
**Response:**
```json
{
  "session_id": "generated-or-reused",
  "plan": {"action":"MAP","table":"loinc","backend":"openai","raw":"ACTION: MAP table=loinc"},
  "result": {"ranked":[...], "top": {...}},
  "memory_last": [{"role":"user","content":"..."}, {"role":"agent","content":{...}}]
}
```

## Notes
- Planner backend autodetect order (from OntoCodex v0.7):
  1. Local fine-tuned HF model (`ONTOCODEX_PLANNER_LOCAL_PATH`)
  2. OpenAI (`OPENAI_API_KEY`)
  3. Anthropic (`ANTHROPIC_API_KEY`)
  4. Stub (offline)
