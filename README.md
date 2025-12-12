# OntoCodex: Multi-agent Biomedical Ontology Enrichment Framework

OntoCodex GPT built with this framework as a showcase: https://chatgpt.com/g/g-6734e1cd43008190b7245d756c8e75ef-ontocodex

# OntoCodex Framework

OntoCodex is a **multi-agent, LLM-enabled framework for semi-automated ontology enrichment**. It integrates large language models, biomedical ontologies, curated knowledge bases, and standard terminologies to support scalable, reproducible, and human-in-the-loop ontology development for real-world biomedical and clinical research.

This repository provides the core framework, agent design, and example workflows for enriching OWL/RDF ontologies with new concepts, relationships, provenance, and standardized codes (e.g., ICD, SNOMED CT, RxNorm, LOINC).

---

## 🚀 Key Features

- **Multi-agent architecture** for ontology enrichment
  - Decision Agent
  - Ontology Reading Agent
  - Knowledge Base Agent
  - Terminology Agent
  - Script Generation Agent
- **Ontology-aware parsing** of user-provided OWL/TTL ontologies
- **Automated concept extraction** from trusted biomedical sources
- **Terminology normalization** to standard vocabularies (ICD, SNOMED CT, RxNorm, ATC, LOINC)
- **Provenance annotation** and confidence scoring
- **Executable Python code generation** for OWL-compliant ontology updates
- **Human-in-the-loop design** for expert review and validation
- **Extensible and modular**, suitable for new domains and data sources

---

## 🧠 Motivation

Ontology enrichment is essential for semantic interoperability but remains labor-intensive and error-prone. OntoCodex addresses this challenge by:

- Reducing manual curation burden
- Improving consistency of concept definitions and mappings
- Supporting downstream analytics using EHR, claims, and clinical trial data
- Enabling rapid iteration and reuse across biomedical domains

---

## 🏗️ Architecture Overview

OntoCodex follows a coordinated, agent-based workflow:

1. **Decision Agent**  
   Interprets enrichment goals and orchestrates agent interactions.

2. **Ontology Reader Agent**  
   Parses OWL/TTL ontologies to identify existing classes, properties, and gaps.

3. **Knowledge Base Agent**  
   Retrieves candidate concepts and relationships from curated sources such as:
   - MedlinePlus (API / cached TTL)
   - PubMed
   - NIH / CDC / ADA / ACC / AHA resources
   - Disease Ontology (DOID)

4. **Terminology Agent**  
   Normalizes extracted concepts to standard vocabularies using CSV, OWL, or TTL datasets.

5. **Script Generation Agent**  
   Generates executable Python scripts to update ontologies with new classes, axioms, annotations, and provenance.


## 🔍 Supported Standards & Vocabularies

- ICD-9 / ICD-10
- SNOMED CT
- RxNorm
- ATC
- LOINC
- DOID
- Custom CSV / OWL / TTL vocabularies

---

## 🧾 Provenance & Transparency

OntoCodex supports:

- Source attribution for extracted concepts
- Timestamped annotations
- Confidence scores (LLM-estimated or heuristic-based)
- Reproducible enrichment scripts

This design supports auditability and regulatory-aligned research workflows.

---

## 📊 Use Cases

- Multiple Chronic Conditions (MCC)
- Alzheimer’s Disease / ADRD
- Opioid and substance use research
- Clinical trial Common Data Elements (CDEs)
- EHR and claims-based phenotyping

---

## 🛡️ Limitations

- Outputs require **expert review** before production use
- LLM-generated content may reflect source bias or incompleteness
- Not intended for direct clinical decision-making

---

## 📄 License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Add tests and documentation
4. Submit a pull request

---

## 📚 Citation

If you use OntoCodex in your research, please cite:

> Feng J, et al. *OntoCodex: A Multi-Agent LLM Framework for Biomedical Ontology Enrichment*. (Manuscript under review).

---

## 📬 Contact

**Tao AI Group**  
Mayo Clinic, AI&Informatics

For questions or collaboration inquiries, please open an issue or contact the maintainers via GitHub.

---

*OntoCodex is a research framework designed to augment—not replace—domain expertise.*




## License
MIT © 2025 Jingna Feng
