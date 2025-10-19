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
python -m venv .venv && source .venv/bin/activate  # or your preferred env
pip install -e .
```

## Quickstart
```bash
python examples/01_basic_rag.py
```

> The default example uses a **SimpleEmbedder** and **SimpleVectorStore** so it runs without extra deps or API keys.
> To use OpenAI or FAISS, install those deps and set env vars per comments in code.

## License
MIT © 2025 Jingna Feng
