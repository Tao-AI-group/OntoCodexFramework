# OntoCodex: Multi-agent Biomedical Ontology Enrichment Framework

Ontology-first, LangChain-aligned framework for building agentic, KG-aware AI apps.

OntoCodex GPT built with this framework as a showcase: https://chatgpt.com/g/g-6734e1cd43008190b7245d756c8e75ef-ontocodex

## Features
- LCEL-style pipelines (`a | b | c`) with `Runnable`
- Hybrid retrieval (vector + KG/SPARQL)
- Ontology-aware planner and semantic critic
- Config-driven pipelines (YAML + Pydantic)
- Provenance/tracing hooks

## Install (editable)
```bash
pip install -r requirements.txt
pip install -e .
```

## Quickstart
```bash
python examples/01_basic_rag.py
```

> The default example uses a **SimpleEmbedder** and **SimpleVectorStore** so it runs without extra deps or API keys.
> To use OpenAI or FAISS, install those deps and set env vars per comments in code.


## Set your data folder (DOID.owl, MEDLINEPLUS.ttl, HP.csv, OMOP CSVs)
```bash
export ONTOCODEX_DATA_DIR=./data
```

## Run the agent demo
```bash
python examples/run_agent.py
```
## Run LLM agent as planner
```bash
pip install openai anthropic
export OPENAI_API_KEY=sk-yourkey
# or export ANTHROPIC_API_KEY=sk-ant-yourkey
python examples/run_agent_with_llm_planner.py
```

## License
MIT © 2025 Jingna Feng
