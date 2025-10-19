# OntoCodex API (v0.2)

JSON-only FastAPI service mirroring OntoCodex GPT behavior.

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Also install your OntoCodex framework locally:
# pip install -e ../ontocodex_gpt_update_v0_2  (or your package path)
```

## Run
```bash
export ONTOCODEX_DATA_DIR=../ontocodex_gpt_update_v0_2/data
uvicorn api_server:app --reload
```

## Endpoints
- `GET /ping`
- `GET /phenotype?disease=<label>`
- `GET /map/lab?term=<text>`
- `GET /map/treatment?term=<text>`
- `GET /map/symptom?term=<text>`
- `GET /guidelines?disease=<label>`
