from typing import List, Dict, Any
class TinyLLM:
    def __init__(self, model:str='stub'): self.model=model
    def invoke(self, messages:List[Dict[str,Any]])->Dict[str,Any]:
        t=' '.join([m.get('content','') for m in messages]).lower()
        if any(k in t for k in ['rxnorm','drug','treatment','medication','dose','med']): return {'role':'assistant','content':'ACTION: MAP table=rxnorm'}
        if any(k in t for k in ['loinc','lab','test','assay']): return {'role':'assistant','content':'ACTION: MAP table=loinc'}
        if any(k in t for k in ['snomed','symptom','phenotype','sign']): return {'role':'assistant','content':'ACTION: MAP table=snomed'}
        return {'role':'assistant','content':'ACTION: PHENOTYPE'}
