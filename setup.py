from setuptools import setup, find_packages

setup(
    name="ontocodex",
    version="0.2.0",
    description="Ontology-first, LangChain-aligned framework for agentic, KG-aware AI",
    author="You",
    license="MIT",
    packages=find_packages(exclude=("examples", "data")),
    install_requires=[
        "pydantic>=2.5.0",
        "pyyaml>=6.0.1",
        "rdflib>=6.3.2",
        "numpy>=1.24.0",
    ],
    extras_require={
        "faiss": ["faiss-cpu>=1.7.4"],
        "openai": ["openai>=1.30.0"],
        "st": ["sentence-transformers>=2.5.1"],
        "otel": ["opentelemetry-api>=1.24.0", "opentelemetry-sdk>=1.24.0"],
    },
    python_requires=">=3.10",
)
