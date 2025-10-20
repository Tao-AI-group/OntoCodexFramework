OntoCodex v1.0 Multi-Agent + LLM Planner Router Patch

This patch wires the existing LLM planner (OpenAI/Anthropic/local FT/stub) into the multi-agent orchestrator.
Use CodexOrchestratorPlanned to run planner-driven multi-agent turns.

Usage:
  export ONTOCODEX_DATA_DIR=./data
  # (optional) set planner backend:
  # export ONTOCODEX_PLANNER_LOCAL_PATH=planner_local_ft   # local classifier
  # export OPENAI_API_KEY=sk-...                             # or Anthropic key
  python examples/run_multi_agent_with_planner.py
