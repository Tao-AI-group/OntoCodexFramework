from setuptools import setup, find_packages
setup(
  name="ontocodex",
  version="1.1.0",
  description="OntoCodex — ontology-first, evidence-grounded, multi-agent LLM framework",
  author="OntoCodex Team",
  license="MIT",
  packages=find_packages(exclude=("examples","data",".github","tests")),
  install_requires=[
    "fastapi>=0.112.0","uvicorn>=0.30.0","pydantic>=2.5.0","pyyaml>=6.0.1",
    "rdflib>=6.3.2","numpy>=1.24.0","pandas>=2.0.0","rapidfuzz>=3.6.1",
    "openai>=1.40.0","anthropic>=0.34.1","transformers>=4.43.0",
    "datasets>=2.20.0","accelerate>=0.30.0"
  ],
  python_requires=">=3.10",
)
