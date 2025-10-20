from pydantic import BaseModel
from typing import List
import os
from .fuzzy import fuzzy_map, load_mapping_csv
from ..core.base import Runnable

class MappingArgs(BaseModel):
    term: str
    table: str  # rxnorm | loinc | snomed
    limit: int = 5
    data_dir: str = "data"

class MappingTool(Runnable):
    name = "ontology_mapping"
    description = "Map text to target vocabulary (RxNorm, LOINC, SNOMED) with fuzzy re-ranking."
    def invoke(self, args: MappingArgs | dict):
        if isinstance(args, dict):
            args = MappingArgs(**args)
        table_map = {
            "rxnorm": ("rxnorm_omop.csv", "concept_name", "concept_code", 1),
            "loinc": ("loinc_omop.csv", "concept_name", "concept_code", 3),
            "snomed": ("snomed_omop.csv", "concept_name", "concept_code", 2),
        }
        key = args.table.lower()
        if key not in table_map:
            return {"error": f"Unknown table '{args.table}'"}
        fname, label_col, code_col, pr = table_map[key]
        path = os.path.join(args.data_dir, fname)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return {"error": f"Mapping file not found or empty: {path}"}
        tables = [load_mapping_csv(path, key.upper(), label_col, code_col, pr)]
        ranked = fuzzy_map(args.term, tables, limit=args.limit)
        top = ranked[0] if ranked else None
        return {"ranked": ranked, "top": top}
