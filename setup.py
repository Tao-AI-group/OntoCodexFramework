from setuptools import setup, find_packages
setup(
  name="ontocodex",
  version="0.4.0",
  description="OntoCodex — ontology-first agent framework (memory + planner)",
  author="You",
  license="MIT",
  packages=find_packages(exclude=("examples","data",".github","tests")),
  install_requires=[
    "pydantic>=2.5.0",
    "pyyaml>=6.0.1",
    "rdflib>=6.3.2",
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "rapidfuzz>=3.6.1",
  ],
  python_requires=">=3.10",
)
